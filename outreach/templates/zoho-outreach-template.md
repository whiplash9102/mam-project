# Zoho Outreach Email Template

Use this after `docs/tay-ho-prospect-enrichment.csv` has been reviewed.

## Subject Options

```text
{{restaurant_name}} có muốn thử lấp bàn trống giờ vắng không?
```

```text
Gợi ý nhỏ cho các slot vắng trong tuần của {{restaurant_name}}
```

## Plain Text Version

```text
Hi team {{restaurant_name}},

Mình là Thanh từ MÂM.

{{suggested_opening_line}}

MÂM đang mở pilot nhỏ cho một nhóm nhà hàng ở Tây Hồ để thử lấp bàn trống giờ vắng bằng khách đã đặt trước.

Cách làm khá đơn giản:

- {{restaurant_name}} chọn những khung giờ muốn có thêm khách
- MÂM đưa khách đã đặt trước đến đúng slot đó
- MÂM đến setup tại quán
- Tháng đầu không lấy phí MÂM
- Sau tháng đầu, chỉ tính 10k / khách thật sự đến ăn

Bên mình không muốn thêm việc cho team vận hành. Mục tiêu là giúp những bàn đang trống có cơ hội thành booking thật.

Nếu {{restaurant_name}} đang có một vài khung giờ vắng trong tuần, mình có thể gửi estimate nhanh xem mỗi tháng có thể thêm khoảng bao nhiêu covers.

Không cần cam kết gì trước. Nếu phù hợp thì mình ghé qua 15 phút để trao đổi thêm.

Xem nhanh MÂM Tây Hồ Pilot:
{{utm_link}}

Thanh
MÂM
0917 077 969
```

## HTML Version

Use the HTML version in Zoho so the UTM link is hidden behind a clean button.

```html
<p>Hi team {{restaurant_name}},</p>

<p>Mình là Thanh từ MÂM.</p>

<p>{{suggested_opening_line}}</p>

<p>
  MÂM đang mở pilot nhỏ cho một nhóm nhà hàng ở Tây Hồ để thử lấp bàn trống giờ vắng
  bằng khách đã đặt trước.
</p>

<p>Cách làm khá đơn giản:</p>

<ul>
  <li>{{restaurant_name}} chọn những khung giờ muốn có thêm khách</li>
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
  Nếu {{restaurant_name}} đang có một vài khung giờ vắng trong tuần, mình có thể gửi
  estimate nhanh xem mỗi tháng có thể thêm khoảng bao nhiêu covers.
</p>

<p>Không cần cam kết gì trước. Nếu phù hợp thì mình ghé qua 15 phút để trao đổi thêm.</p>

<p>
  <a href="{{utm_link}}" style="background:#214c3f;color:#ffffff;text-decoration:none;padding:12px 18px;border-radius:999px;display:inline-block;font-weight:700;">
    Xem MÂM Tây Hồ Pilot
  </a>
</p>

<p>
  Thanh<br>
  MÂM<br>
  0917 077 969
</p>

<p style="font-size:12px;color:#69746f;">
  Nếu email này không phù hợp, chỉ cần reply "không quan tâm", mình sẽ không liên hệ lại.
</p>
```

## Notes

- Use `utm_link` from `docs/tay-ho-prospect-enrichment.csv`.
- Do not send to rows where `email_found` is `Not found`.
- For rows without email, use the same opening line for Instagram DM, phone/Zalo, or walk-in.
