# MAM Conversion Design Memo

## Goal

Help restaurant owners understand MAM in under 10 seconds and convert them into partner leads.

Primary conversion: owner submits the partner form.

Secondary conversions:
- Click phone or Zalo contact.
- Scroll to ROI calculator.
- Interact with ROI calculator.
- Click primary CTA from hero.

## Audience

Restaurant owners and operators in Hanoi, especially mid-to-high-end restaurants with empty weekday seats.

They are busy, skeptical, and operationally focused. They do not want a startup pitch. They want to know:
- What exactly happens?
- Does it bring real guests?
- How much money can I make?
- What does it cost?
- How much work will my team need to do?

## Core Message

MAM fills empty restaurant seats during slow hours. Restaurants only pay when real guests show up.

Short version:
"Turn empty weekday tables into paid guests. No setup fee. Pay only when guests arrive."

Vietnamese direction:
"Biến bàn trống giữa tuần thành khách thật. Không phí cố định. Chỉ trả khi khách đến ăn."

## Current Problem

The current page explains the idea, but it still asks owners to read too much before they can picture the product.

The website should become more visual and concrete:
- Show empty tables becoming booked tables.
- Show a simple owner dashboard / reservation card.
- Show the guest flow in a few visual steps.
- Show money impact with a clear before/after.
- Make pricing feel low-risk and transparent.

## Design Principle

Visual first, text second.

Every major section should answer one question with one strong visual:
- Hero: "What is this?"
- Problem: "Why should I care?"
- Flow: "How does it work?"
- ROI: "How much can I gain?"
- Trust: "Why should I believe this?"
- Form: "What happens after I sign up?"

Avoid long paragraphs. Use short labels, numbers, cards, timelines, icons, mock screens, and before/after comparisons.

## Recommended Page Structure

### 1. Hero: Instant Product Understanding

Goal: In 5-10 seconds, owner understands MAM.

Recommended layout:
- Left: short headline, one sentence, CTA.
- Right: visual mockup showing a restaurant schedule.

Hero visual concept:
- A weekly calendar/table map.
- Slow slots are empty and grey.
- MAM fills them with green "Booked" chips.
- Revenue counter increases.

Suggested copy:
- Headline: "Lấp đầy bàn trống giữa tuần."
- Subhead: "MAM mang khách thật đến vào những khung giờ bạn đang vắng. Không phí cố định, chỉ trả khi khách đến ăn."
- CTA: "Đăng ký nhận khách thử"
- Secondary CTA: "Xem cách hoạt động"

### 2. Problem: Empty Tables Are Lost Revenue

Goal: Make the pain obvious.

Visual concept:
- Before/after revenue strip.
- Monday-Wednesday dinner has many empty seats.
- Each empty table has a small "0đ" marker.
- MAM version shows booked guests and extra revenue.

Keep text minimal:
- "Bàn trống không chỉ là chỗ ngồi. Đó là doanh thu bị mất."

### 3. How MAM Works: 3-Step Visual Flow

Goal: Reduce operational anxiety.

Recommended steps:
1. You choose slow hours.
2. MAM brings verified guests.
3. Guests arrive, you serve, MAM reports.

Visual concept:
- Three connected panels.
- Panel 1: owner toggles available slots.
- Panel 2: guest books a table.
- Panel 3: restaurant receives confirmed booking and monthly report.

Avoid saying the restaurant needs to learn a complex system. Emphasize low lift.

### 4. ROI Calculator: Main Interactive Conversion Tool

Goal: Let owners see their own upside.

Current ROI calculator is valuable. Make it more visually central.

Recommended changes:
- Move ROI higher, before detailed pricing.
- Show output as "Doanh thu thêm / tháng" first.
- Add a small comparison: "Bàn trống: 0đ" vs "Qua MAM: +X VND".
- Keep sliders, but simplify labels.

Default assumptions should feel conservative.

### 5. Pricing: Risk Reversal

Goal: Make the owner feel there is little downside.

Visual concept:
- Two columns:
  - You pay 0đ for setup, monthly fee, listing.
  - You pay only per guest who arrives.

Suggested language:
- "Không khách, không phí."
- "Không hợp đồng dài hạn."
- "Thử trước với vài khung giờ vắng."

### 6. Trust and Proof

Goal: Reduce skepticism.

If there are no live partner logos yet, do not fake social proof.

Use operational proof instead:
- Confirmation flow.
- No-show protection explanation.
- Real sample booking card.
- Sample monthly report.
- "Team MAM đến setup trong 30 phút."

Later, add:
- Partner restaurant logos.
- Before/after occupancy numbers.
- Owner quotes.
- Photos from real restaurant visits.

### 7. Form: Make the Next Step Feel Small

Goal: Convert without feeling like a big commitment.

Current form is okay, but frame it as a low-pressure consultation.

Recommended form headline:
"Nhận đề xuất khung giờ có thể lấp đầy"

Button:
"Gửi thông tin để MAM gọi lại"

Add small reassurance near form:
- "Không cần ký hợp đồng ngay."
- "Team MAM chỉ gọi để hiểu tình trạng bàn trống của bạn."

## Visual Style Direction

Should feel:
- Premium enough for restaurant owners.
- Operational and clear, not startup-cute.
- Warm hospitality tone, but data-backed.

Use:
- Realistic restaurant/table imagery where possible.
- Clean product mockups.
- Green for confirmed/active revenue.
- Muted grey for empty/unused capacity.
- Gold only as accent, not dominant.

Avoid:
- Too much decorative illustration.
- Too many emojis.
- Long text blocks.
- Abstract startup language like "platform ecosystem".
- Generic food stock photography that does not explain the product.

## Conversion Events To Track

Current GA events:
- `generate_lead`
- `partner_form_success`
- `partner_form_error`

Add later:
- `hero_cta_click`
- `nav_cta_click`
- `roi_interaction`
- `phone_click`
- `email_click`
- `zalo_click`
- `pricing_view`
- `form_view`

## Implementation Priority

Phase 1:
- Redesign hero with visual product mockup.
- Move ROI calculator higher.
- Rewrite sections with shorter copy.
- Improve form framing and CTA.

Phase 2:
- Add richer booking/dashboard visuals.
- Add GA event tracking for key CTAs.
- Add lightweight A/B test variants manually if traffic is enough.

Phase 3:
- Add partner proof, real numbers, and case studies.
- Add dedicated owner-specific landing pages by cuisine or district.

## Design North Star

The owner should not need to read the full page to understand MAM.

They should see:
Empty tables -> MAM bookings -> guests arrive -> extra revenue -> low-risk signup.
