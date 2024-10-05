# Thiết kế cấu trúc Database cho hệ thống bản đồ tử vi

Để xây dựng một hệ thống tử vi hoàn chỉnh, cơ sở dữ liệu (database) cần được thiết kế theo hướng có thể lưu trữ thông tin về các cung, sao và quy tắc an sao, đồng thời cho phép tính toán vận mệnh dựa trên các yếu tố năm sinh, tháng sinh, ngày sinh và giờ sinh. Dưới đây là cấu trúc database bao gồm các bảng và mối quan hệ giữa chúng.

## 1. Cấu trúc bảng dữ liệu

### a. Bảng Zodiac (12 cung địa bàn)
Bảng này chứa thông tin về 12 cung trong tử vi.

```sql
CREATE TABLE Zodiac (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL, -- Tên của cung (Mệnh, Phúc Đức, Tài Bạch...)
    description TEXT           -- Mô tả chi tiết về cung này
);
```

| id  | name      | description         |
|-----|-----------|---------------------|
| 1   | Mệnh      | Mô tả cung Mệnh     |
| 2   | Tài Bạch  | Mô tả cung Tài Bạch |
| ... | ...       | ...                 |

### b. Bảng Stars (Các sao trong tử vi)
Bảng này lưu trữ thông tin về các sao trong tử vi.

```sql
CREATE TABLE Stars (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,    -- Tên của sao (Tử Vi, Thiên Phủ...)
    type VARCHAR(50),             -- Loại sao (Chính tinh, Phụ tinh...)
    element VARCHAR(50),          -- Ngũ hành của sao (Kim, Mộc, Thủy, Hỏa, Thổ)
    description TEXT              -- Mô tả chi tiết về sao này
);
```

| id  | name      | type       | element | description           |
|-----|-----------|------------|---------|-----------------------|
| 1   | Tử Vi     | Chính Tinh | Thổ     | Mô tả về sao Tử Vi    |
| 2   | Thiên Phủ | Chính Tinh | Thổ     | Mô tả về sao Thiên Phủ|
| ... | ...       | ...        | ...     | ...                   |

### c. Bảng Zodiac_Stars (Sao trong từng cung)
Bảng này liên kết các sao với từng cung dựa trên quy tắc an sao.

```sql
CREATE TABLE Zodiac_Stars (
    id INT PRIMARY KEY AUTO_INCREMENT,
    zodiac_id INT,    -- Liên kết tới bảng Zodiac
    star_id INT,      -- Liên kết tới bảng Stars
    position INT,     -- Vị trí (an sao tại cung nào)
    FOREIGN KEY (zodiac_id) REFERENCES Zodiac(id),
    FOREIGN KEY (star_id) REFERENCES Stars(id)
);
```

| id  | zodiac_id | star_id | position |
|-----|-----------|---------|----------|
| 1   | 1         | 1       | 5        |
| 2   | 2         | 2       | 9        |

### d. Bảng CanChi (Thiên Can và Địa Chi)
Bảng này lưu trữ thông tin về 10 thiên can và 12 địa chi.

```sql
CREATE TABLE CanChi (
    id INT PRIMARY KEY AUTO_INCREMENT,
    type ENUM('Thiên Can', 'Địa Chi'), -- Loại: Thiên Can hoặc Địa Chi
    name VARCHAR(50) NOT NULL,         -- Tên (Giáp, Ất, Bính...)
    element VARCHAR(50),               -- Ngũ hành tương ứng
    description TEXT                   -- Mô tả chi tiết
);
```

| id  | type      | name | element | description       |
|-----|-----------|------|---------|-------------------|
| 1   | Thiên Can | Giáp | Mộc     | Mô tả về Giáp     |
| 2   | Địa Chi   | Tý   | Thủy    | Mô tả về Tý       |
| ... | ...       | ...  | ...     | ...               |

```sql
INSERT INTO CanChi (type, name, element, description) VALUES
('Thiên Can', 'Giáp', 'Mộc', 'Mô tả về Giáp'),
('Thiên Can', 'Ất', 'Mộc', 'Mô tả về Ất'),
('Thiên Can', 'Bính', 'Hỏa', 'Mô tả về Bính'),
('Thiên Can', 'Đinh', 'Hỏa', 'Mô tả về Đinh'),
('Thiên Can', 'Mậu', 'Thổ', 'Mô tả về Mậu'),
('Thiên Can', 'Kỷ', 'Thổ', 'Mô tả về Kỷ'),
('Thiên Can', 'Canh', 'Kim', 'Mô tả về Canh'),
('Thiên Can', 'Tân', 'Kim', 'Mô tả về Tân'),
('Thiên Can', 'Nhâm', 'Thủy', 'Mô tả về Nhâm'),
('Thiên Can', 'Quý', 'Thủy', 'Mô tả về Quý'),
('Địa Chi', 'Tý', 'Thủy', 'Mô tả về Tý'),
('Địa Chi', 'Sửu', 'Thổ', 'Mô tả về Sửu'),
('Địa Chi', 'Dần', 'Mộc', 'Mô tả về Dần'),
('Địa Chi', 'Mão', 'Mộc', 'Mô tả về Mão'),
('Địa Chi', 'Thìn', 'Thổ', 'Mô tả về Thìn'),
('Địa Chi', 'Tỵ', 'Hỏa', 'Mô tả về Tỵ'),
('Địa Chi', 'Ngọ', 'Hỏa', 'Mô tả về Ngọ'),
('Địa Chi', 'Mùi', 'Thổ', 'Mô tả về Mùi'),
('Địa Chi', 'Thân', 'Kim', 'Mô tả về Thân'),
('Địa Chi', 'Dậu', 'Kim', 'Mô tả về Dậu'),
('Địa Chi', 'Tuất', 'Thổ', 'Mô tả về Tuất'),
('Địa Chi', 'Hợi', 'Thủy', 'Mô tả về Hợi');
```

### e. Bảng MasterData (Dữ liệu quy tắc an sao)
Bảng này lưu trữ các quy tắc an sao dựa trên năm sinh, tháng sinh, giờ sinh và các điều kiện khác.

```sql
CREATE TABLE MasterData (
    id INT PRIMARY KEY AUTO_INCREMENT,
    can_chi_id INT,  -- Liên kết tới bảng CanChi (năm sinh theo Thiên Can/Địa Chi)
    zodiac_id INT,   -- Liên kết tới bảng Zodiac (cung)
    star_id INT,     -- Liên kết tới bảng Stars (sao tương ứng)
    rule TEXT,       -- Quy tắc để an sao (VD: Sao Tử Vi an ở Dần nếu sinh năm Giáp Tý)
    FOREIGN KEY (can_chi_id) REFERENCES CanChi(id),
    FOREIGN KEY (zodiac_id) REFERENCES Zodiac(id),
    FOREIGN KEY (star_id) REFERENCES Stars(id)
);
```

| id  | can_chi_id | zodiac_id | star_id | rule                                          |
|-----|------------|-----------|---------|-----------------------------------------------|
| 1   | 1          | 1         | 1       | "An sao Tử Vi ở cung Dần nếu sinh năm Giáp Tý"|
| 2   | 2          | 2         | 2       | "An sao Thiên Phủ ở cung Thìn nếu sinh năm Ất Sửu"|

### f. Bảng User (Người dùng)
Bảng này lưu trữ thông tin về người dùng và lá số tử vi của họ.

```sql
CREATE TABLE User (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,  -- Tên người dùng
    birth_date DATE,             -- Ngày sinh
    birth_hour TIME,             -- Giờ sinh
    gender ENUM('Nam', 'Nữ'),    -- Giới tính
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Thời gian tạo lá số
);
```

| id  | name         | birth_date | birth_hour | gender | created_at          |
|-----|--------------|------------|------------|--------|---------------------|
| 1   | Nguyễn Văn A | 1980-03-15 | 08:30:00   | Nam    | 2024-10-04 10:00:00 |

### g. Bảng User_Zodiac (Lá số tử vi của người dùng)
Bảng này lưu trữ thông tin về các cung và sao của từng người dùng.

```sql
CREATE TABLE User_Zodiac (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,      -- Liên kết tới bảng User
    zodiac_id INT,    -- Liên kết tới bảng Zodiac
    star_id INT,      -- Liên kết tới bảng Stars
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (zodiac_id) REFERENCES Zodiac(id),
    FOREIGN KEY (star_id) REFERENCES Stars(id)
);
```

| id  | user_id | zodiac_id | star_id |
|-----|---------|-----------|---------|
| 1   | 1       | 1         | 1       |
| 2   | 1       | 2         | 3       |
```