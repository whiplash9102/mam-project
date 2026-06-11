# MAM Partner Outreach

This directory keeps BD/outreach work separate from the public website code.

## Structure

- `data/`: researched prospect CSV files.
- `templates/`: reusable email copy.
- `scripts/`: automation scripts.
- `output/`: generated drafts, summaries, and future send logs.

## Current Flow

1. Research prospects.
2. Store enriched rows in `data/tay-ho-prospect-enrichment.csv`.
3. Generate Zoho-ready drafts:

```bash
python3 outreach/scripts/generate_zoho_drafts.py
```

4. Review `output/zoho_drafts_summary.csv`.
5. Create `.env` from `outreach/.env.example`.
6. Run a dry-run:

```bash
python3 outreach/scripts/send_zoho_smtp.py --limit 1
```

7. Send a test email to yourself:

```bash
python3 outreach/scripts/send_zoho_smtp.py --limit 1 --to your-email@mamji.vn --include-low-confidence --send
```

8. Send reviewed emails only after the test looks right:

```bash
python3 outreach/scripts/send_zoho_smtp.py --limit 15 --include-low-confidence --send
```

By default, low-confidence emails are skipped. Use `--include-low-confidence` only after manual review.

## What Thanh Should Provide

To keep outreach professional, useful, and low-spam, provide:

- Sender identity:
  - From name
  - Zoho sender email
  - Reply-to email
  - Signature line
- Outreach rules:
  - Max emails per day: 15
  - Tone: Vietnamese only
  - Follow-up: 3 days after first email
- Business proof:
  - Any early partner names, even informal
  - Any pilot numbers once available
  - Photos/screenshots we are allowed to use
- Offer details:
  - Trial duration: first month has no MAM fee
  - Fee after first month: 10k VND per guest who arrives
  - Setup: in-person at the restaurant
  - No fixed monthly fee
  - No long-term contract
- Contact quality:
  - Confirmed owner/manager names when known
  - Verified emails or Zalo numbers
  - Notes from walk-ins or DMs

## Professional Guardrails

- Do not guess private emails.
- Do not send to rows where `email_found` is `Not found`.
- Prefer Instagram DM, phone/Zalo, or walk-in when no public email exists.
- Keep links hidden behind clean CTA text in HTML email.
- Include a simple opt-out sentence.
- Log every sent email before sending follow-ups.
- Do not fabricate testimonials, partner logos, or claims from third-party companies.
