from sqlalchemy import Enum, create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Zodiac, Star, CanChi, MasterData

# Replace with your actual database URL
DATABASE_URL = "sqlite:///./tuvi.db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

class CanChiType(Enum.Enum):
    ThienCan = "Thiên Can"
    DiaChi = "Địa Chi"

# Seed data for Zodiac
zodiacs = [
    Zodiac(name='Mệnh', description='Cung Mệnh chỉ về bản chất và tính cách con người'),
    Zodiac(name='Tài Bạch', description='Cung Tài Bạch chủ về tiền bạc, tài sản...'),
    Zodiac(name='Quan Lộc', description='Cung Quan Lộc chủ về sự nghiệp, công danh'),
    Zodiac(name='Điền Trạch', description='Cung Điền Trạch chủ về nhà cửa, đất đai'),
    Zodiac(name='Phúc Đức', description='Cung Phúc Đức chủ về phúc đức, may mắn'),
    Zodiac(name='Phu Thê', description='Cung Phu Thê chủ về hôn nhân, vợ chồng'),
    Zodiac(name='Tử Tức', description='Cung Tử Tức chủ về con cái, hậu duệ'),
    Zodiac(name='Huynh Đệ', description='Cung Huynh Đệ chủ về anh chị em, bạn bè'),
    Zodiac(name='Nô Bộc', description='Cung Nô Bộc chủ về người giúp việc, thuộc hạ'),
    Zodiac(name='Thiên Di', description='Cung Thiên Di chủ về sự di chuyển, thay đổi chỗ ở'),
    Zodiac(name='Tật Ách', description='Cung Tật Ách chủ về bệnh tật, tai nạn'),
    Zodiac(name='Phụ Mẫu', description='Cung Phụ Mẫu chủ về cha mẹ, gia đình')
]
session.add_all(zodiacs)

# Seed data for Stars
stars = [
    Star(name='Tử Vi', type='Chính Tinh', element='Thổ', description='Sao Tử Vi chủ về quyền uy, đứng đầu trong các sao'),
    Star(name='Thiên Phủ', type='Chính Tinh', element='Thổ', description='Sao Thiên Phủ chủ về bảo vệ, che chở...'),
    Star(name='Vũ Khúc', type='Chính Tinh', element='Kim', description='Sao Vũ Khúc chủ về tài lộc, tiền bạc'),
    Star(name='Thiên Tướng', type='Chính Tinh', element='Thủy', description='Sao Thiên Tướng chủ về quyền uy, sự nghiệp'),
    Star(name='Liêm Trinh', type='Chính Tinh', element='Hỏa', description='Sao Liêm Trinh chủ về sự chính trực, ngay thẳng'),
    Star(name='Thiên Đồng', type='Chính Tinh', element='Thủy', description='Sao Thiên Đồng chủ về phúc đức, may mắn'),
    Star(name='Thiên Cơ', type='Chính Tinh', element='Mộc', description='Sao Thiên Cơ chủ về trí tuệ, sự thông minh'),
    Star(name='Thái Dương', type='Chính Tinh', element='Hỏa', description='Sao Thái Dương chủ về sự sáng suốt, minh mẫn'),
    Star(name='Thái Âm', type='Chính Tinh', element='Thủy', description='Sao Thái Âm chủ về sự dịu dàng, mềm mại'),
    Star(name='Tham Lang', type='Chính Tinh', element='Thủy', description='Sao Tham Lang chủ về sự tham vọng, ham muốn'),
    Star(name='Cự Môn', type='Chính Tinh', element='Thủy', description='Sao Cự Môn chủ về sự tranh đấu, cãi vã'),
    Star(name='Thiên Lương', type='Chính Tinh', element='Thổ', description='Sao Thiên Lương chủ về sự bảo vệ, che chở'),
    Star(name='Thất Sát', type='Chính Tinh', element='Kim', description='Sao Thất Sát chủ về sự quyết đoán, mạnh mẽ'),
    Star(name='Phá Quân', type='Chính Tinh', element='Thủy', description='Sao Phá Quân chủ về sự phá hoại, thay đổi'),
    Star(name='Văn Xương', type='Phụ Tinh', element='Kim', description='Sao Văn Xương chủ về học vấn, văn chương'),
    Star(name='Văn Khúc', type='Phụ Tinh', element='Thủy', description='Sao Văn Khúc chủ về nghệ thuật, tài năng'),
    Star(name='Thiên Khôi', type='Phụ Tinh', element='Hỏa', description='Sao Thiên Khôi chủ về sự thông minh, sáng suốt'),
    Star(name='Thiên Việt', type='Phụ Tinh', element='Thủy', description='Sao Thiên Việt chủ về sự giúp đỡ, quý nhân phù trợ'),
    Star(name='Tả Phụ', type='Phụ Tinh', element='Thổ', description='Sao Tả Phụ chủ về sự hỗ trợ, giúp đỡ'),
    Star(name='Hữu Bật', type='Phụ Tinh', element='Thổ', description='Sao Hữu Bật chủ về sự hỗ trợ, giúp đỡ'),
    Star(name='Thiên Hình', type='Phụ Tinh', element='Hỏa', description='Sao Thiên Hình chủ về sự hình phạt, kỷ luật'),
    Star(name='Thiên Riêu', type='Phụ Tinh', element='Thủy', description='Sao Thiên Riêu chủ về sự rối ren, phức tạp'),
    Star(name='Thiên Y', type='Phụ Tinh', element='Thủy', description='Sao Thiên Y chủ về sức khỏe, chữa bệnh'),
    Star(name='Thiên Mã', type='Phụ Tinh', element='Hỏa', description='Sao Thiên Mã chủ về sự di chuyển, thay đổi'),
    Star(name='Thiên Khốc', type='Phụ Tinh', element='Kim', description='Sao Thiên Khốc chủ về sự buồn bã, khóc lóc'),
    Star(name='Thiên Hư', type='Phụ Tinh', element='Thủy', description='Sao Thiên Hư chủ về sự hư hỏng, thất bại'),
    Star(name='Thiên Đức', type='Phụ Tinh', element='Thổ', description='Sao Thiên Đức chủ về sự đức độ, nhân từ'),
    Star(name='Nguyệt Đức', type='Phụ Tinh', element='Thủy', description='Sao Nguyệt Đức chủ về sự đức độ, nhân từ'),
    Star(name='Hóa Lộc', type='Phụ Tinh', element='Thủy', description='Sao Hóa Lộc chủ về tài lộc, tiền bạc'),
    Star(name='Hóa Quyền', type='Phụ Tinh', element='Hỏa', description='Sao Hóa Quyền chủ về quyền lực, uy quyền'),
    Star(name='Hóa Khoa', type='Phụ Tinh', element='Mộc', description='Sao Hóa Khoa chủ về học vấn, khoa bảng'),
    Star(name='Hóa Kỵ', type='Phụ Tinh', element='Thủy', description='Sao Hóa Kỵ chủ về sự cản trở, khó khăn'),
    Star(name='Long Trì', type='Phụ Tinh', element='Thủy', description='Sao Long Trì chủ về sự uyển chuyển, linh hoạt'),
    Star(name='Phượng Các', type='Phụ Tinh', element='Thủy', description='Sao Phượng Các chủ về sự cao quý, thanh tao'),
    Star(name='Hoa Cái', type='Phụ Tinh', element='Kim', description='Sao Hoa Cái chủ về sự trang nghiêm, uy nghi'),
    Star(name='Thiên Quan', type='Phụ Tinh', element='Thủy', description='Sao Thiên Quan chủ về sự giúp đỡ, quý nhân phù trợ'),
    Star(name='Thiên Phúc', type='Phụ Tinh', element='Hỏa', description='Sao Thiên Phúc chủ về sự may mắn, phúc đức'),
    Star(name='Thiên Tài', type='Phụ Tinh', element='Thổ', description='Sao Thiên Tài chủ về tài năng, sự khéo léo'),
    Star(name='Thiên Thọ', type='Phụ Tinh', element='Kim', description='Sao Thiên Thọ chủ về sự trường thọ, bền vững'),
    Star(name='Địa Kiếp', type='Phụ Tinh', element='Hỏa', description='Sao Địa Kiếp chủ về sự nguy hiểm, khó khăn'),
    Star(name='Địa Không', type='Phụ Tinh', element='Hỏa', description='Sao Địa Không chủ về sự nguy hiểm, khó khăn'),
    Star(name='Kình Dương', type='Phụ Tinh', element='Kim', description='Sao Kình Dương chủ về sự mạnh mẽ, quyết đoán'),
    Star(name='Đà La', type='Phụ Tinh', element='Kim', description='Sao Đà La chủ về sự cản trở, khó khăn'),
    Star(name='Hồng Loan', type='Phụ Tinh', element='Thủy', description='Sao Hồng Loan chủ về tình duyên, hôn nhân'),
    Star(name='Thiên Hỷ', type='Phụ Tinh', element='Hỏa', description='Sao Thiên Hỷ chủ về niềm vui, hạnh phúc'),
    Star(name='Ân Quang', type='Phụ Tinh', element='Hỏa', description='Sao Ân Quang chủ về sự giúp đỡ, quý nhân phù trợ'),
    Star(name='Thiên Quý', type='Phụ Tinh', element='Hỏa', description='Sao Thiên Quý chủ về sự giúp đỡ, quý nhân phù trợ'),
    Star(name='Cô Thần', type='Phụ Tinh', element='Thổ', description='Sao Cô Thần chủ về sự cô đơn, lẻ loi'),
    Star(name='Quả Tú', type='Phụ Tinh', element='Thổ', description='Sao Quả Tú chủ về sự cô đơn, lẻ loi'),
    Star(name='Thiên La', type='Phụ Tinh', element='Thổ', description='Sao Thiên La chủ về sự ràng buộc, khó khăn'),
    Star(name='Địa Võng', type='Phụ Tinh', element='Thổ', description='Sao Địa Võng chủ về sự ràng buộc, khó khăn'),
    Star(name='Thiên Giải', type='Phụ Tinh', element='Mộc', description='Sao Thiên Giải chủ về sự giải thoát, cứu giúp'),
    Star(name='Địa Giải', type='Phụ Tinh', element='Mộc', description='Sao Địa Giải chủ về sự giải thoát, cứu giúp'),
    Star(name='Thiên Sứ', type='Phụ Tinh', element='Thổ', description='Sao Thiên Sứ chủ về sự ràng buộc, khó khăn'),
    Star(name='Thiên Thương', type='Phụ Tinh', element='Thủy', description='Sao Thiên Thương chủ về sự thương xót, đau buồn'),
]
session.add_all(stars)

# Seed data for CanChi
can_chis = [
    CanChi(type=CanChiType.ThienCan, name='Giáp', element='Mộc', description='Thiên Can Giáp thuộc Mộc, chủ về sinh khí, khởi đầu.'),
    CanChi(type=CanChiType.ThienCan, name='Ất', element='Mộc', description='Thiên Can Ất thuộc Mộc, chủ về sự phát triển, sinh sôi.'),
    CanChi(type=CanChiType.ThienCan, name='Bính', element='Hỏa', description='Thiên Can Bính thuộc Hỏa, chủ về sự nhiệt huyết, năng động.'),
    CanChi(type=CanChiType.ThienCan, name='Đinh', element='Hỏa', description='Thiên Can Đinh thuộc Hỏa, chủ về sự ổn định, bền vững.'),
    CanChi(type=CanChiType.ThienCan, name='Mậu', element='Thổ', description='Thiên Can Mậu thuộc Thổ, chủ về sự kiên định, vững chắc.'),
    CanChi(type=CanChiType.ThienCan, name='Kỷ', element='Thổ', description='Thiên Can Kỷ thuộc Thổ, chủ về sự bảo vệ, che chở.'),
    CanChi(type=CanChiType.ThienCan, name='Canh', element='Kim', description='Thiên Can Canh thuộc Kim, chủ về sự sắc bén, quyết đoán.'),
    CanChi(type=CanChiType.ThienCan, name='Tân', element='Kim', description='Thiên Can Tân thuộc Kim, chủ về sự tinh tế, tỉ mỉ.'),
    CanChi(type=CanChiType.ThienCan, name='Nhâm', element='Thủy', description='Thiên Can Nhâm thuộc Thủy, chủ về sự linh hoạt, uyển chuyển.'),
    CanChi(type=CanChiType.ThienCan, name='Quý', element='Thủy', description='Thiên Can Quý thuộc Thủy, chủ về sự sâu sắc, thâm trầm.'),
    CanChi(type=CanChiType.DiaChi, name='Tý', element='Thủy', description='Địa Chi Tý thuộc Thủy, chủ về trí tuệ, sự linh hoạt.'),
    CanChi(type=CanChiType.DiaChi, name='Sửu', element='Thổ', description='Địa Chi Sửu thuộc Thổ, chủ về sự kiên định, vững chắc.'),
    CanChi(type=CanChiType.DiaChi, name='Dần', element='Mộc', description='Địa Chi Dần thuộc Mộc, chủ về sự phát triển, sinh sôi.'),
    CanChi(type=CanChiType.DiaChi, name='Mão', element='Mộc', description='Địa Chi Mão thuộc Mộc, chủ về sự mềm mại, uyển chuyển.'),
    CanChi(type=CanChiType.DiaChi, name='Thìn', element='Thổ', description='Địa Chi Thìn thuộc Thổ, chủ về sự bảo vệ, che chở.'),
    CanChi(type=CanChiType.DiaChi, name='Tỵ', element='Hỏa', description='Địa Chi Tỵ thuộc Hỏa, chủ về sự nhiệt huyết, năng động.'),
    CanChi(type=CanChiType.DiaChi, name='Ngọ', element='Hỏa', description='Địa Chi Ngọ thuộc Hỏa, chủ về sự ổn định, bền vững.'),
    CanChi(type=CanChiType.DiaChi, name='Mùi', element='Thổ', description='Địa Chi Mùi thuộc Thổ, chủ về sự kiên định, vững chắc.'),
    CanChi(type=CanChiType.DiaChi, name='Thân', element='Kim', description='Địa Chi Thân thuộc Kim, chủ về sự sắc bén, quyết đoán.'),
    CanChi(type=CanChiType.DiaChi, name='Dậu', element='Kim', description='Địa Chi Dậu thuộc Kim, chủ về sự tinh tế, tỉ mỉ.'),
    CanChi(type=CanChiType.DiaChi, name='Tuất', element='Thổ', description='Địa Chi Tuất thuộc Thổ, chủ về sự bảo vệ, che chở.'),
    CanChi(type=CanChiType.DiaChi, name='Hợi', element='Thủy', description='Địa Chi Hợi thuộc Thủy, chủ về sự linh hoạt, uyển chuyển.')
]
session.add_all(can_chis)


# Seed data for MasterData
master_data = [
    MasterData(can_chi_id=1, zodiac_id=1, star_id=1, rule='Sao Tử Vi an ở cung Dần nếu sinh năm Giáp Tý'),
    MasterData(can_chi_id=2, zodiac_id=2, star_id=2, rule='Sao Thiên Phủ an ở cung Thìn nếu sinh năm Ất Sửu'),
    MasterData(can_chi_id=3, zodiac_id=3, star_id=3, rule='Sao Vũ Khúc an ở cung Tỵ nếu sinh năm Bính Dần'),
    MasterData(can_chi_id=4, zodiac_id=4, star_id=4, rule='Sao Thiên Tướng an ở cung Ngọ nếu sinh năm Đinh Mão'),
    MasterData(can_chi_id=5, zodiac_id=5, star_id=5, rule='Sao Liêm Trinh an ở cung Mùi nếu sinh năm Mậu Thìn'),
    MasterData(can_chi_id=6, zodiac_id=6, star_id=6, rule='Sao Thiên Đồng an ở cung Thân nếu sinh năm Kỷ Tỵ'),
    MasterData(can_chi_id=7, zodiac_id=7, star_id=7, rule='Sao Thiên Cơ an ở cung Dậu nếu sinh năm Canh Ngọ'),
    MasterData(can_chi_id=8, zodiac_id=8, star_id=8, rule='Sao Thái Dương an ở cung Tuất nếu sinh năm Tân Mùi'),
    MasterData(can_chi_id=9, zodiac_id=9, star_id=9, rule='Sao Thái Âm an ở cung Hợi nếu sinh năm Nhâm Thân'),
    MasterData(can_chi_id=10, zodiac_id=10, star_id=10, rule='Sao Tham Lang an ở cung Tý nếu sinh năm Quý Dậu'),
    MasterData(can_chi_id=11, zodiac_id=11, star_id=11, rule='Sao Cự Môn an ở cung Sửu nếu sinh năm Giáp Tuất'),
    MasterData(can_chi_id=12, zodiac_id=12, star_id=12, rule='Sao Thiên Lương an ở cung Dần nếu sinh năm Ất Hợi'),
    MasterData(can_chi_id=13, zodiac_id=1, star_id=13, rule='Sao Thất Sát an ở cung Mão nếu sinh năm Bính Tý'),
    MasterData(can_chi_id=14, zodiac_id=2, star_id=14, rule='Sao Phá Quân an ở cung Thìn nếu sinh năm Đinh Sửu'),
    MasterData(can_chi_id=1, zodiac_id=1, star_id=41, rule='Sao Long Trì an theo tháng sinh'),
    MasterData(can_chi_id=2, zodiac_id=2, star_id=42, rule='Sao Phượng Các an theo tháng sinh'),
    MasterData(can_chi_id=3, zodiac_id=3, star_id=43, rule='Sao Hoa Cái an theo tháng sinh'),
    MasterData(can_chi_id=4, zodiac_id=4, star_id=44, rule='Sao Thiên Quan an theo tháng sinh'),
    MasterData(can_chi_id=5, zodiac_id=5, star_id=45, rule='Sao Thiên Phúc an theo tháng sinh'),
    MasterData(can_chi_id=6, zodiac_id=6, star_id=46, rule='Sao Thiên Tài an theo tháng sinh'),
    MasterData(can_chi_id=7, zodiac_id=7, star_id=47, rule='Sao Thiên Thọ an theo tháng sinh')
]

session.add_all(master_data)

# Commit the session
session.commit()

print("Data seeded successfully!")