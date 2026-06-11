#!/usr/bin/env python3
import csv
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "tay-ho-prospect-enrichment.csv"
OUTPUT_DIR = ROOT / "output" / "zoho_drafts"
SUMMARY_FILE = ROOT / "output" / "zoho_drafts_summary.csv"


def clean_slug(value):
    value = (value or "").strip().lower()
    value = re.sub(r"[^a-z0-9_]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value or "prospect"


def subject_for(row):
    return f"{row['restaurant_name']} có muốn thử lấp bàn trống giờ vắng không?"


def html_email(row):
    restaurant = html.escape(row["restaurant_name"])
    opening = html.escape(row["suggested_opening_line"])
    utm_link = html.escape(row["utm_link"], quote=True)

    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(subject_for(row))}</title>
</head>
<body style="margin:0;padding:0;background:#fbfaf8;color:#24312d;font-family:-apple-system,BlinkMacSystemFont,'SF Pro Text','Helvetica Neue',Arial,sans-serif;line-height:1.65;">
  <div style="max-width:640px;margin:0 auto;padding:28px 20px;">
    <p>Hi team {restaurant},</p>

    <p>Mình là Thanh từ MÂM.</p>

    <p>{opening}</p>

    <p>
      MÂM đang mở pilot nhỏ cho một nhóm nhà hàng ở Tây Hồ để thử lấp bàn trống giờ vắng
      bằng khách đã đặt trước.
    </p>

    <p>Cách làm khá đơn giản:</p>

    <ul>
      <li>{restaurant} chọn những khung giờ muốn có thêm khách</li>
      <li>MÂM đưa khách đã đặt trước đến đúng slot đó</li>
      <li>MÂM đến setup tại quán</li>
      <li>Tháng đầu không lấy phí MÂM</li>
      <li>Sau tháng đầu, chỉ tính 10k / khách thật sự đến ăn</li>
    </ul>

    <p>
      Bên mình không muốn thêm việc cho team vận hành. Mục tiêu là giúp những bàn đang trống
      có cơ hội thành booking thật.
    </p>

    <p>
      Nếu {restaurant} đang có một vài khung giờ vắng trong tuần, mình có thể gửi estimate nhanh
      xem mỗi tháng có thể thêm khoảng bao nhiêu covers.
    </p>

    <p>Không cần cam kết gì trước. Nếu phù hợp thì mình ghé qua 15 phút để trao đổi thêm.</p>

    <p style="margin:26px 0;">
      <a href="{utm_link}" style="background:#214c3f;color:#ffffff;text-decoration:none;padding:12px 18px;border-radius:999px;display:inline-block;font-weight:700;">
        Xem MÂM Tây Hồ Pilot
      </a>
    </p>

    <p>
      Thanh<br>
      MÂM<br>
      0917 077 969
    </p>

    <p style="font-size:12px;color:#69746f;margin-top:26px;">
      Nếu email này không phù hợp, chỉ cần reply "không quan tâm", mình sẽ không liên hệ lại.
    </p>
  </div>
</body>
</html>
"""


def plain_text_email(row):
    restaurant = row["restaurant_name"]
    return f"""Hi team {restaurant},

Mình là Thanh từ MÂM.

{row["suggested_opening_line"]}

MÂM đang mở pilot nhỏ cho một nhóm nhà hàng ở Tây Hồ để thử lấp bàn trống giờ vắng bằng khách đã đặt trước.

Cách làm khá đơn giản:

- {restaurant} chọn những khung giờ muốn có thêm khách
- MÂM đưa khách đã đặt trước đến đúng slot đó
- MÂM đến setup tại quán
- Tháng đầu không lấy phí MÂM
- Sau tháng đầu, chỉ tính 10k / khách thật sự đến ăn

Bên mình không muốn thêm việc cho team vận hành. Mục tiêu là giúp những bàn đang trống có cơ hội thành booking thật.

Nếu {restaurant} đang có một vài khung giờ vắng trong tuần, mình có thể gửi estimate nhanh xem mỗi tháng có thể thêm khoảng bao nhiêu covers.

Không cần cam kết gì trước. Nếu phù hợp thì mình ghé qua 15 phút để trao đổi thêm.

Xem MÂM Tây Hồ Pilot:
{row["utm_link"]}

Thanh
MÂM
0917 077 969

Nếu email này không phù hợp, chỉ cần reply "không quan tâm", mình sẽ không liên hệ lại.
"""


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with DATA_FILE.open(newline="", encoding="utf-8") as source:
        rows = list(csv.DictReader(source))

    summary_rows = []
    for row in rows:
        slug = clean_slug(row.get("utm_slug") or row["restaurant_name"])
        html_path = OUTPUT_DIR / f"{slug}.html"
        txt_path = OUTPUT_DIR / f"{slug}.txt"
        html_path.write_text(html_email(row), encoding="utf-8")
        txt_path.write_text(plain_text_email(row), encoding="utf-8")

        summary_rows.append({
            "restaurant_name": row["restaurant_name"],
            "email_found": row["email_found"],
            "email_confidence": row["email_confidence"],
            "best_contact_channel": row["best_contact_channel"],
            "subject": subject_for(row),
            "html_draft": str(html_path.relative_to(ROOT)),
            "text_draft": str(txt_path.relative_to(ROOT)),
            "utm_link": row["utm_link"],
            "ready_for_email": "yes" if row["email_found"] != "Not found" else "no",
            "notes": row["notes"],
        })

    with SUMMARY_FILE.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=summary_rows[0].keys())
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"Generated {len(summary_rows)} draft sets in {OUTPUT_DIR}")
    print(f"Summary: {SUMMARY_FILE}")


if __name__ == "__main__":
    main()
