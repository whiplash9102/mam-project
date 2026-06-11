#!/usr/bin/env python3
import argparse
import csv
import os
import smtplib
import ssl
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
SUMMARY_FILE = ROOT / "output" / "zoho_drafts_summary.csv"
SEND_LOG = ROOT / "output" / "send_log.csv"
ENV_FILE = PROJECT_ROOT / ".env"


def load_env():
    if not ENV_FILE.exists():
        return
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def required_env(name):
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Missing required env var: {name}")
    return value


def read_sent_keys():
    if not SEND_LOG.exists():
        return set()
    with SEND_LOG.open(newline="", encoding="utf-8") as f:
        return {
            (row["restaurant_name"], row["email"])
            for row in csv.DictReader(f)
            if row.get("status") == "sent"
        }


def append_log(row):
    SEND_LOG.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "sent_at",
        "restaurant_name",
        "email",
        "subject",
        "utm_link",
        "status",
        "error",
    ]
    exists = SEND_LOG.exists()
    with SEND_LOG.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def build_message(row, smtp_user, from_name, reply_to):
    html_path = ROOT / row["html_draft"]
    text_path = ROOT / row["text_draft"]
    html_body = html_path.read_text(encoding="utf-8")
    text_body = text_path.read_text(encoding="utf-8")

    msg = EmailMessage()
    msg["Subject"] = row["subject"]
    msg["From"] = f"{from_name} <{smtp_user}>"
    msg["To"] = row["email_found"]
    msg["Reply-To"] = reply_to
    msg.set_content(text_body)
    msg.add_alternative(html_body, subtype="html")
    return msg


def connect_smtp(host, port, user, password):
    context = ssl.create_default_context()
    server = smtplib.SMTP(host, port, timeout=30)
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login(user, password)
    return server


def load_rows():
    with SUMMARY_FILE.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    parser = argparse.ArgumentParser(description="Send reviewed Zoho SMTP outreach emails.")
    parser.add_argument("--send", action="store_true", help="Actually send emails. Omit for dry-run.")
    parser.add_argument("--limit", type=int, default=1, help="Max emails to process.")
    parser.add_argument("--to", help="Override recipient for test sends.")
    parser.add_argument("--include-low-confidence", action="store_true", help="Allow low-confidence emails.")
    args = parser.parse_args()

    load_env()

    rows = load_rows()
    sent_keys = read_sent_keys()

    candidates = []
    for row in rows:
        email = row["email_found"].strip()
        if row["ready_for_email"] != "yes" or email == "Not found":
            continue
        if not args.include_low_confidence and row["email_confidence"].lower() == "low":
            continue
        recipient = args.to or email
        if not args.to and (row["restaurant_name"], recipient) in sent_keys:
            continue
        row = dict(row)
        row["email_found"] = recipient
        candidates.append(row)

    candidates = candidates[: args.limit]

    if not candidates:
        print("No candidates to send. Use --include-low-confidence for low-confidence emails or add verified emails.")
        return

    print(f"{'SEND' if args.send else 'DRY RUN'}: {len(candidates)} email(s)")
    for row in candidates:
        print(f"- {row['restaurant_name']} -> {row['email_found']} | {row['subject']}")

    if not args.send:
        print("Dry-run only. Add --send to actually send.")
        return

    smtp_host = required_env("ZOHO_SMTP_HOST")
    smtp_port = int(os.environ.get("ZOHO_SMTP_PORT", "587"))
    smtp_user = required_env("ZOHO_SMTP_USER")
    smtp_password = required_env("ZOHO_SMTP_PASSWORD")
    from_name = os.environ.get("ZOHO_FROM_NAME", "Thanh | MÂM")
    reply_to = os.environ.get("ZOHO_REPLY_TO", smtp_user)

    server = connect_smtp(smtp_host, smtp_port, smtp_user, smtp_password)
    try:
        for row in candidates:
            now = datetime.now(timezone.utc).isoformat()
            try:
                msg = build_message(row, smtp_user, from_name, reply_to)
                server.send_message(msg)
                append_log({
                    "sent_at": now,
                    "restaurant_name": row["restaurant_name"],
                    "email": row["email_found"],
                    "subject": row["subject"],
                    "utm_link": row["utm_link"],
                    "status": "sent",
                    "error": "",
                })
                print(f"sent: {row['restaurant_name']} -> {row['email_found']}")
            except Exception as exc:
                append_log({
                    "sent_at": now,
                    "restaurant_name": row["restaurant_name"],
                    "email": row["email_found"],
                    "subject": row["subject"],
                    "utm_link": row["utm_link"],
                    "status": "failed",
                    "error": str(exc),
                })
                print(f"failed: {row['restaurant_name']} -> {row['email_found']}: {exc}")
    finally:
        server.quit()


if __name__ == "__main__":
    main()
