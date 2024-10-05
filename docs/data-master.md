```sql
-- Cung
INSERT INTO Zodiac (name, description) VALUES 
('Mệnh', 'Cung Mệnh chỉ về bản chất và tính cách con người'),
('Tài Bạch', 'Cung Tài Bạch chủ về tiền bạc, tài sản...');

-- Sao
INSERT INTO Stars (name, type, element, description) VALUES 
('Tử Vi', 'Chính Tinh', 'Thổ', 'Sao Tử Vi chủ về quyền uy, đứng đầu trong các sao'),
('Thiên Phủ', 'Chính Tinh', 'Thổ', 'Sao Thiên Phủ chủ về bảo vệ, che chở...');

-- Thiên Can và Địa Chi
INSERT INTO CanChi (type, name, element, description) VALUES 
('Thiên Can', 'Giáp', 'Mộc', 'Thiên Can Giáp thuộc Mộc, chủ về sinh khí, khởi đầu.'),
('Địa Chi', 'Tý', 'Thủy', 'Địa Chi Tý thuộc Thủy, chủ về trí tuệ, sự linh hoạt.');

-- Quy tắc an sao
INSERT INTO MasterData (can_chi_id, zodiac_id, star_id, rule) VALUES 
(1, 1, 1, 'Sao Tử Vi an ở cung Dần nếu sinh năm Giáp Tý'),
(2, 2, 2, 'Sao Thiên Phủ an ở cung Thìn nếu sinh năm Ất Sửu');

```

Trong Tử Vi, Thiên Can và Địa Chi là hai thành phần quan trọng để tạo nên Can Chi (thiên can kết hợp với địa chi để tạo ra năm âm lịch). Dưới đây là danh sách đầy đủ của Thiên Can và Địa Chi:

1. Thiên Can (10 Can)
Thiên Can là một hệ thống gồm 10 đơn vị, biểu thị sự tương tác của các yếu tố ngũ hành và âm dương.

| Thứ tự | Thiên Can | Ngũ Hành | Âm Dương |
|--------|------------|----------|----------|
| 1      | Giáp       | Mộc      | Dương    |
| 2      | Ất         | Mộc      | Âm       |
| 3      | Bính       | Hỏa      | Dương    |
| 4      | Đinh       | Hỏa      | Âm       |
| 5      | Mậu        | Thổ      | Dương    |
| 6      | Kỷ         | Thổ      | Âm       |
| 7      | Canh       | Kim      | Dương    |
| 8      | Tân        | Kim      | Âm       |
| 9      | Nhâm       | Thủy     | Dương    |
| 10     | Quý        | Thủy     | Âm       |

2. Địa Chi (12 Chi)
Địa Chi là một hệ thống gồm 12 đơn vị, tương ứng với 12 con giáp và đại diện cho các giai đoạn trong chu kỳ của thời gian.

| Thứ tự | Địa Chi | Con giáp | Ngũ Hành | Âm Dương |
|--------|---------|----------|----------|----------|
| 1      | Tý      | Chuột    | Thủy     | Dương    |
| 2      | Sửu     | Trâu     | Thổ      | Âm       |
| 3      | Dần     | Hổ       | Mộc      | Dương    |
| 4      | Mão     | Mèo (Thỏ)| Mộc      | Âm       |
| 5      | Thìn    | Rồng     | Thổ      | Dương    |
| 6      | Tỵ      | Rắn      | Hỏa      | Âm       |
| 7      | Ngọ     | Ngựa     | Hỏa      | Dương    |
| 8      | Mùi     | Dê       | Thổ      | Âm       |
| 9      | Thân    | Khỉ      | Kim      | Dương    |
| 10     | Dậu     | Gà       | Kim      | Âm       |
| 11     | Tuất    | Chó      | Thổ      | Dương    |
| 12     | Hợi     | Lợn      | Thủy     | Âm       |

3. Sự kết hợp giữa Thiên Can và Địa Chi
Khi kết hợp 10 Thiên Can và 12 Địa Chi, ta tạo ra 60 cặp Can Chi, tương ứng với chu kỳ 60 năm (mỗi năm có một cặp Can Chi duy nhất). Ví dụ:

- Năm Giáp Tý (Thiên Can Giáp + Địa Chi Tý) thuộc hành Mộc, mang tính chất dương.
- Năm Ất Sửu (Thiên Can Ất + Địa Chi Sửu) thuộc hành Mộc, nhưng mang tính chất âm.

Mỗi năm sẽ được định danh bởi một cặp Can Chi, ví dụ:

- 2024 là năm Giáp Thìn (Giáp thuộc Mộc, Thìn thuộc Thổ).

Các Can Chi này còn được dùng trong tử vi để tính toán an sao, luận đoán vận mệnh theo năm sinh, giờ sinh.
