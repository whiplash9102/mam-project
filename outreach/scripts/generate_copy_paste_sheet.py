#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "tay-ho-prospect-enrichment.csv"
OUTPUT_FILE = ROOT / "output" / "copy_paste_outreach.csv"


def subject(row):
    return f"{row['restaurant_name']} có muốn thử lấp bàn trống giờ vắng không?"


def message(row):
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
0917 077 969"""


def dm_message(row):
    restaurant = row["restaurant_name"]
    return f"""Hi team {restaurant}, mình là Thanh từ MÂM.

{row["suggested_opening_line"]}

MÂM đang mở pilot nhỏ ở Tây Hồ để thử lấp bàn trống giờ vắng bằng khách đã đặt trước. Tháng đầu không lấy phí MÂM, team mình đến setup tại quán, sau đó chỉ tính 10k / khách thật sự đến ăn.

Nếu {restaurant} có vài khung giờ weekday chưa kín bàn, mình có thể gửi estimate nhanh xem mỗi tháng có thể thêm bao nhiêu covers. Không cần cam kết gì trước.

Thông tin nhanh: {row["utm_link"]}"""


def main():
    with DATA_FILE.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "restaurant_name",
        "district",
        "tier",
        "email_found",
        "phone_found",
        "best_contact_channel",
        "subject",
        "email_or_long_message",
        "short_dm_message",
        "utm_link",
        "personalized_angle",
        "notes",
    ]
    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({
                "restaurant_name": row["restaurant_name"],
                "district": row["district"],
                "tier": row["tier"],
                "email_found": row["email_found"],
                "phone_found": row["phone_found"],
                "best_contact_channel": row["best_contact_channel"],
                "subject": subject(row),
                "email_or_long_message": message(row),
                "short_dm_message": dm_message(row),
                "utm_link": row["utm_link"],
                "personalized_angle": row["personalized_angle"],
                "notes": row["notes"],
            })

    print(f"Wrote {len(rows)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
