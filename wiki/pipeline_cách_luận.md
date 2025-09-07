Dưới đây là **đặc tả kỹ thuật + thuật toán/logic** để hiện thực MVP “Tử vi Đẩu Số” (lá số Việt) ở mức sản phẩm chạy được, dễ mở rộng.

# 1) Tổng quan pipeline

1. **Input**: họ tên (tuỳ), giới tính, ngày–giờ–phút sinh (dương lịch), nơi sinh (múi giờ).
2. **Tiền xử lý**

   * Chuyển **dương → âm** (âm lịch VN) + **can–chi năm/tháng/ngày/giờ** (có lệch múi giờ).
   * Xác định **múi giờ lịch sử** (GMT+7; VN không có DST).
3. **Dựng lá số**

   * An **12 cung** (Mệnh, Phụ Mẫu, …, Huynh Đệ).
   * An **cục** (Kim/Mộc/Thủy/Hỏa/Thổ cục) theo ngũ hành Mệnh & năm sinh.
   * An **sao chính/tá** theo bộ quy tắc (bảng tra).
4. **Vận hạn**

   * Tính **Đại vận** (10 năm/cung), **Tiểu vận** (lưu niên), có thể thêm lưu tháng/nhật.
5. **Suy luận & xuất bản**

   * Rule engine → 4 trụ đề xuất: **Công việc – Tài chính – Tình cảm – Sức khỏe** + “Kim chỉ nam”.
   * Sinh ngôn ngữ tự nhiên (template + LLM để diễn giải mượt).

---

# 2) Dữ liệu nền (schemas)

## 2.1. Kiểu dữ liệu

```json
{
  "profile": {
    "gender": "male|female",
    "birth": {"gregorian": "YYYY-MM-DDTHH:mm", "tz": "Asia/Ho_Chi_Minh", "place": "Da Nang, VN"}
  },
  "lunar": {
    "date": "YYYY-MM-DD",
    "year_can_chi": "Ất Hợi",
    "month_can_chi": "Giáp Thân",
    "day_can_chi": "Quý Mão",
    "hour_branch": "Tý"
  },
  "chart": {
    "menh_cung": "Mệnh",
    "cuc": "Thổ cục",
    "houses": {
      "Mệnh": {"branch": "Dần", "stars": ["Tử Vi", "Thiên Tướng", "Hữu Bật", "..."]},
      "Phụ Mẫu": {"branch": "Mão", "stars": ["..."]},
      "...": {}
    }
  },
  "fortune": {
    "dai_van": [{"age_range":"22-31","house":"Quan Lộc","score":"+2"}, "..."],
    "tieu_van": [{"year":2026,"focus":"Tài Bạch","score":"+1"}, "..."]
  }
}
```

## 2.2. Bảng tham chiếu (data-driven)

* `CAN`, `CHI`, `HOUR_TO_BRANCH` (giờ→địa chi).
* **Bảng an cung Mệnh/Thân** theo **tháng âm + giờ sinh** (quen thuộc trong Tử Vi VN).
* **Ngũ hành nạp âm** năm sinh; ánh xạ ra **Cục** (Kim/Mộc/Thủy/Hỏa/Thổ).
* **Catalog sao**:

```json
{
  "Tử Vi": {"tier":"chinh_tinh","weights":{"Quan Lộc":2,"Mệnh":3,"Tài Bạch":1},"polar":"dương"},
  "Thiên Phủ": {"tier":"chinh_tinh","weights":{"Tài Bạch":2,"Mệnh":2},"polar":"âm"},
  "Kình Dương": {"tier":"sat_tinh","weights":{"all":-2}},
  "Hóa Lộc": {"tier":"hoa_tinh","weights":{"Tài Bạch":2,"Phu Thê":1}}
}
```

> Toàn bộ **cách an sao** nên tách thành **bảng JSON** (tra cứu), giúp cập nhật trường phái dễ dàng.

---

# 3) Thuật toán từng bước

## 3.1. Chuyển lịch & Can–Chi

* Dùng thuật toán âm dương lịch (VD: Ho Ngọc Đức) hoặc lib nội bộ.
* Từ ngày âm → tính **Thiên Can – Địa Chi** cho **năm/tháng/ngày/giờ**:

  * Giờ → 12 chi (Tý 23:00–00:59, Sửu 01:00–02:59, …).
  * Can giờ dựa trên **can ngày** (bảng quy tắc cổ điển).

## 3.2. An cung Mệnh & 12 cung

* Xác định **cung Mệnh** dựa **tháng âm + giờ sinh** (bảng tra 12 ô).
* Từ cung Mệnh, đi thuận **Địa Chi** để lấp 12 cung:
  `Mệnh → Phụ Mẫu → Phúc Đức → Điền Trạch → Quan Lộc → Nô Bộc → Thiên Di → Tật Ách → Tài Bạch → Tử Tức → Phu Thê → Huynh Đệ`.

## 3.3. Xác định **Cục**

* Lấy **ngũ hành Mệnh** (kết hợp mệnh nạp âm + vị trí cung Mệnh).
* Ánh xạ thành **Kim/Mộc/Thủy/Hỏa/Thổ cục** (bảng quy tắc). Cục ảnh hưởng mạnh tới an sao chính (Tử Vi/Thiên Phủ).

## 3.4. An sao

* **Sao chính tinh** (Tử Vi, Thiên Phủ, Thái Dương, Thái Âm, Vũ Khúc, Liêm Trinh, Thiên Tướng, Phá Quân, Tham Lang, Cự Môn, Thiên Đồng, Thiên Cơ…):

  * Vị trí phụ thuộc **cục + tháng/ngày/giờ** theo **bảng tra**.
* **Sao phụ, sát tinh, cát tinh, hoá tinh** (Kình Dương, Đà La, Hỏa Linh, Không Kiếp, Lộc Tồn, Hóa Lộc/Quyền/Khoa/Kỵ…):

  * Quy tắc theo **can năm, chi năm, can ngày**, hoặc **đếm thuận/nghịch** từ một mốc (ví dụ từ cung Dần/Tỵ).

> MVP: bắt đầu với **\~14 chính tinh + 4 hoá tinh + 6 sát/cát tinh phổ biến** để có kết quả đủ giàu.

## 3.5. Đại vận – Tiểu vận

* **Đại vận**: từ **10 tuổi** (hoặc theo phái), mỗi cung 10 năm; chiều thuận/nghịch tùy **âm/dương nam/nữ** (quy tắc cổ).
* **Tiểu vận** (lưu niên): năm hiện tại chiếu vào một cung nhất định; **sao lưu** (Hóa Lộc/Quyền/Khoa/Kỵ theo can năm hiện tại) nhập hạn.

---

# 4) Rule Engine suy luận (scoring → guidance)

## 4.1. Tính điểm cung theo sao

```
base_score(cung) = Σ weight(sao, cung)
điều chỉnh:
  + combo cát (Tử Vi + Thiên Phủ), (Hóa Lộc + Lộc Tồn) → +α
  + combo sát (Kình + Đà + Hỏa/Linh) tại Mệnh/Quan/Tài → -β
  + vị trí miếu/vượng/bình/nhược/hãm của sao → ±γ
normalize → [-3, +3]
```

## 4.2. Ánh xạ cung → miền khuyến nghị

* **Quan Lộc** → “Công việc”; **Tài Bạch** → “Tài chính”; **Phu Thê** → “Tình cảm”; **Tật Ách** → “Sức khỏe”; cộng hưởng **Phúc Đức/Điền Trạch/Thiên Di** làm modifiers.
* Tạo **tag định hướng**: “thăng tiến”, “học kỹ năng”, “thủ chắc tiền”, “giảm rủi ro”, “ưu tiên gia đình”,…

## 4.3. Sinh ngôn ngữ tự nhiên (NLG)

* Mẫu câu (template) theo điểm:

  * `score ≥ +2`: “Rất thuận: … Nên chủ động … Cơ hội …”
  * `score ≈ 0`: “Trung tính: … Tập trung vào … Tránh vội vàng …”
  * `score ≤ -2`: “Cẩn trọng: … Quản trị rủi ro … Hoãn quyết định lớn …”
* **Kim chỉ nam tháng/năm**: chọn 1–2 hành động then chốt (OKR cá nhân).

---

# 5) API/Module đề xuất

## 5.1. Python (pseudo-impl)

```python
def to_lunar(dt_utc, tz): ...
def can_chi(lunar_date): ...
def house_of_menh(lunar_month, hour_branch, gender): ...
def assign_12_houses(menh_idx): ...
def determine_cuc(menh_element, year_nap_am): ...
def place_major_stars(chart, cuc, lunar): ...
def place_aux_stars(chart, lunar, can_day, chi_year): ...
def compute_dai_van(chart, gender, chi_year): ...
def compute_scores(chart): ...
def generate_guidance(scores, context): ...

def build_chart(profile):
    lunar = to_lunar(profile.birth)
    cc = can_chi(lunar)
    menh_idx = house_of_menh(lunar.month, cc["hour_branch"], profile.gender)
    houses = assign_12_houses(menh_idx)
    cuc = determine_cuc(menh_element(...), cc["year_nap_am"])
    chart = {"houses": houses, "cuc": cuc}
    place_major_stars(chart, cuc, lunar)
    place_aux_stars(chart, lunar, cc["can_day"], cc["chi_year"])
    dai_van = compute_dai_van(chart, profile.gender, cc["chi_year"])
    scores = compute_scores(chart)
    guidance = generate_guidance(scores, {"year": 2025})
    return {"lunar": cc, "chart": chart, "fortune": {"dai_van": dai_van}, "advice": guidance}
```

## 5.2. REST endpoints

* `POST /api/horoscope/build` → trả `chart` + `advice`.
* `GET /api/horoscope/{id}/year/2026` → tính **lưu niên** năm 2026.

---

# 6) UX “3 bước”

1. Nhập ngày–giờ–nơi sinh → **Tự nhận dạng** âm lịch, can–chi.
2. Trang lá số rút gọn: vòng 12 cung, danh sách sao nổi bật, **điểm 4 trụ**.
3. Tab “Kim chỉ nam”: 3–5 gợi ý hành động + cảnh báo rủi ro.

---

# 7) Kiểm thử & biên giới

* **Sai số giờ sinh**: cho phép ±30 phút → flag “độ tin cậy”.
* **Sinh gần giao canh giờ**: hiển thị 2 phương án (A/B) với xác suất.
* **Không nhớ giờ**: bật **mode thống kê** (xét 12 giờ → chọn mẫu số đông).
* **Khác trường phái**: kiến trúc **bảng quy tắc tách rời** để cài preset (Bắc phái, Nam phái…).

---

# 8) Bảo mật & đạo đức

* Nêu rõ: đây là **công cụ định hướng**, **không thay thế** tư vấn y khoa/pháp lý/tài chính.
* Anonymize dữ liệu sinh, cho phép **xoá** hồ sơ.
* Tránh phát ngôn tuyệt đối (“chắc chắn”, “định mệnh không đổi”).

---

# 9) Demo output (rút gọn)

```
Công việc: +2  → 2025 thuận đề bạt, nên học quản trị dự án.
Tài chính: +1  → Ưu tiên tích lũy, tránh đòn bẩy Q2–Q3.
Tình cảm:  0  → Tập trung giao tiếp, tránh quyết định nóng.
Sức khỏe: -1  → Giảm thức khuya, kiểm tra mắt/cột sống.
Kim chỉ nam: “Kỷ luật tài chính – Học một kỹ năng tạo đòn bẩy thu nhập”.
```

---

Nếu bạn muốn, mình có thể:

* Xuất **bộ JSON bảng an sao khởi tạo** (bản rút gọn để cắm ngay vào code),
* Viết **module Python** mẫu `build_chart()` đầy đủ xương sống,
* Hoặc phác **wireframe UI** theo dữ liệu trên.
