"""
Tu Vi Calculator Component

Component chuyên trách tính toán lá số tử vi theo phương pháp truyền thống.
Có thể dễ dàng thay thế bằng các thuật toán tính toán khác.
"""

from typing import Dict, List, Any
from datetime import datetime
from lunarcalendar import Converter, Solar

from .interfaces import ITuviCalculator, UserInfo, TuviResult


class TuviCalculator(ITuviCalculator):
    """Engine tính toán tử vi chính"""
    
    def __init__(self):
        self.cung_names = ['Mệnh', 'Phụ Mẫu', 'Phúc Đức', 'Điền Trạch', 'Quan Lộc', 'Nô Bộc', 
                          'Thiên Di', 'Tật Ách', 'Tài Bạch', 'Tử Tức', 'Phu Thê', 'Huynh Đệ']
        
        self.chi_positions = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
        
        # Mapping độ mạnh sao
        self.star_strength_map = self._init_star_strength_map()
        
        # Mapping trọng số sao
        self.star_weights = self._init_star_weights()
    
    def calculate_tuvi(self, user_info: UserInfo) -> TuviResult:
        """Tính toán lá số tử vi toàn diện"""
        # Parse thông tin
        date_obj = datetime.strptime(user_info.birthday, "%d/%m/%Y")
        hour_int = int(user_info.birth_time.split(':')[0])
        
        # Convert sang âm lịch
        lunar_date = self._convert_to_lunar(date_obj.year, date_obj.month, date_obj.day)
        
        # Tính toán cơ bản
        thien_can, dia_chi = self._get_thien_can_dia_chi(date_obj.year)
        cuc = self._get_cuc(thien_can)
        gio_sinh = self._get_gio_sinh(hour_int)
        menh_cung_chi = self._determine_menh_cung_position(hour_int, date_obj.month)
        
        # An sao
        sao_cung = self._an_sao_comprehensive(
            lunar_date.day, lunar_date.month, lunar_date.year, 
            hour_int, user_info.gender, thien_can, menh_cung_chi
        )
        
        # Tính vận hạn
        fortune = self._calculate_fortune_periods(
            date_obj.year, user_info.gender, menh_cung_chi, thien_can
        )
        
        # Phân tích và khuyến nghị
        analysis = self._generate_fortune_analysis(sao_cung, fortune, date_obj.year)
        guidance = self._generate_guidance_recommendations(analysis)
        
        # Tạo kết quả
        basic_info = {
            'birth_info': f"{user_info.birthday} giờ {gio_sinh}",
            'thien_can': thien_can,
            'dia_chi': dia_chi,
            'cuc': cuc,
            'gender': user_info.gender,
            'menh_cung': menh_cung_chi,
            'current_age': datetime.now().year - date_obj.year + 1
        }
        
        return TuviResult(
            basic_info=basic_info,
            sao_cung=sao_cung,
            fortune=fortune,
            analysis=analysis,
            guidance=guidance
        )
    
    def get_star_strength(self, star_name: str, chi_position: str) -> str:
        """Lấy độ mạnh của sao tại vị trí địa chi"""
        return self.star_strength_map.get(star_name, {}).get(chi_position, 'bình')
    
    def _convert_to_lunar(self, year: int, month: int, day: int):
        """Convert dương lịch sang âm lịch"""
        solar = Solar(year, month, day)
        return Converter.Solar2Lunar(solar)
    
    def _get_thien_can_dia_chi(self, year: int):
        """Lấy thiên can địa chi của năm"""
        can = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý']
        chi = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
        can_index = year % 10
        chi_index = year % 12
        return can[can_index], chi[chi_index]
    
    def _get_cuc(self, thien_can: str) -> str:
        """Lấy cục từ thiên can"""
        cuc_mapping = {
            'Kim': ['Canh', 'Tân'],
            'Mộc': ['Giáp', 'Ất'],
            'Thủy': ['Nhâm', 'Quý'],
            'Hỏa': ['Bính', 'Đinh'],
            'Thổ': ['Mậu', 'Kỷ']
        }
        for key, values in cuc_mapping.items():
            if thien_can in values:
                return key
        return 'Thổ'  # Default
    
    def _get_gio_sinh(self, hour: int) -> str:
        """Lấy giờ sinh theo địa chi"""
        gio_mapping = {
            'Tý': 0, 'Sửu': 1, 'Dần': 2, 'Mão': 3,
            'Thìn': 4, 'Tỵ': 5, 'Ngọ': 6, 'Mùi': 7,
            'Thân': 8, 'Dậu': 9, 'Tuất': 10, 'Hợi': 11
        }
        return list(gio_mapping.keys())[hour % 12]
    
    def _determine_menh_cung_position(self, birth_hour: int, birth_month: int) -> str:
        """Xác định vị trí cung Mệnh"""
        hour_chi = self.chi_positions[birth_hour % 12]
        hour_index = self.chi_positions.index(hour_chi)
        menh_index = (hour_index + birth_month - 1) % 12
        return self.chi_positions[menh_index]
    
    def _an_sao_comprehensive(self, day: int, month: int, year: int, hour: int, 
                            gender: str, thien_can: str, menh_cung_chi: str) -> Dict[str, List[str]]:
        """An sao toàn diện"""
        # Tính vị trí các cung
        menh_index = self.chi_positions.index(menh_cung_chi)
        cung_chi_mapping = {}
        for i, cung in enumerate(self.cung_names):
            chi_index = (menh_index + i) % 12
            cung_chi_mapping[self.chi_positions[chi_index]] = cung
        
        # An 14 chính tinh theo ngày sinh âm lịch
        chinh_tinh_14 = {
            'Tử Vi': day % 12, 
            'Thiên Phủ': (day + 6) % 12, 
            'Thiên Cơ': (day + 1) % 12, 
            'Thiên Đồng': (day + 11) % 12, 
            'Thái Dương': (day + month) % 12, 
            'Thái Âm': (15 - day) % 12,
            'Thiên Lương': (day + 7) % 12,
            'Vũ Khúc': (day - 1) % 12, 
            'Thất Sát': (day + 5) % 12, 
            'Phá Quân': (day + 4) % 12,
            'Liêm Trinh': (day + 8) % 12,
            'Tham Lang': (day + 3) % 12, 
            'Cự Môn': (day + 2) % 12, 
            'Thiên Tướng': (day + 9) % 12
        }
        
        # An cát tinh
        cat_tinh = {
            # Tả Phụ Hữu Bật - theo tháng sinh
            'Tả Phụ': (month + 1) % 12,
            'Hữu Bật': (month - 1) % 12,
            # Văn Xương Văn Khúc - theo giờ sinh  
            'Văn Xương': (hour + 2) % 12,
            'Văn Khúc': (hour + 8) % 12,
            # Thiên Khôi Thiên Việt - theo năm sinh
            'Thiên Khôi': (year + 3) % 12,
            'Thiên Việt': (year + 9) % 12,
            # Lộc Tồn - theo can năm sinh
            'Lộc Tồn': self._get_loc_ton_position(thien_can),
            # Thiên Mã - theo chi năm sinh
            'Thiên Mã': self._get_thien_ma_position(year)
        }
        
        # An sát tinh
        sat_tinh = {
            # Kình Dương Đà La - theo giờ và ngày sinh
            'Kình Dương': (hour + day) % 12,
            'Đà La': (hour - day) % 12,
            # Địa Không Địa Kiếp - theo năm sinh
            'Địa Không': (year + 2) % 12,
            'Địa Kiếp': (year + 8) % 12,
            # Hỏa Tinh Linh Tinh - theo giờ sinh
            'Hỏa Tinh': self._get_hoa_tinh_position(hour),
            'Linh Tinh': self._get_linh_tinh_position(hour),
            # Thiên Hình - theo tháng sinh
            'Thiên Hình': self._get_thien_hinh_position(month),
            # Thiên Riêu - theo tháng sinh
            'Thiên Riêu': self._get_thien_rieu_position(month)
        }
        
        # An tứ hóa
        tu_hoa_tinh = self._get_tu_hoa_stars(thien_can)
        
        # Gán sao vào cung
        sao_cung = {cung: [] for cung in self.cung_names}
        
        # Gán chính tinh
        for sao, chi_index in chinh_tinh_14.items():
            chi_name = self.chi_positions[chi_index % 12]
            if chi_name in cung_chi_mapping:
                cung = cung_chi_mapping[chi_name]
                sao_cung[cung].append(sao)
        
        # Gán cát tinh
        for sao, chi_index in cat_tinh.items():
            if isinstance(chi_index, list):
                for idx in chi_index:
                    chi_name = self.chi_positions[idx % 12]
                    if chi_name in cung_chi_mapping:
                        cung = cung_chi_mapping[chi_name]
                        sao_cung[cung].append(sao)
            else:
                chi_name = self.chi_positions[chi_index % 12]
                if chi_name in cung_chi_mapping:
                    cung = cung_chi_mapping[chi_name]
                    sao_cung[cung].append(sao)
        
        # Gán sát tinh
        for sao, chi_index in sat_tinh.items():
            if isinstance(chi_index, list):
                for idx in chi_index:
                    chi_name = self.chi_positions[idx % 12]
                    if chi_name in cung_chi_mapping:
                        cung = cung_chi_mapping[chi_name]
                        sao_cung[cung].append(sao)
            else:
                chi_name = self.chi_positions[chi_index % 12]
                if chi_name in cung_chi_mapping:
                    cung = cung_chi_mapping[chi_name]
                    sao_cung[cung].append(sao)
        
        # Gán tứ hóa
        for sao, cung_name in tu_hoa_tinh.items():
            if cung_name in sao_cung:
                sao_cung[cung_name].append(sao)
        
        return sao_cung
    
    def _get_tu_hoa_stars(self, thien_can: str) -> Dict[str, str]:
        """Lấy 4 hóa tinh theo Thiên Can"""
        tu_hoa_mapping = {
            'Giáp': {'Hóa Lộc': 'Tài Bạch', 'Hóa Quyền': 'Quan Lộc', 'Hóa Khoa': 'Phúc Đức', 'Hóa Kỵ': 'Tật Ách'},
            'Ất': {'Hóa Lộc': 'Thiên Di', 'Hóa Quyền': 'Tử Tức', 'Hóa Khoa': 'Nô Bộc', 'Hóa Kỵ': 'Huynh Đệ'},
            'Bính': {'Hóa Lộc': 'Phu Thê', 'Hóa Quyền': 'Mệnh', 'Hóa Khoa': 'Thiên Di', 'Hóa Kỵ': 'Phụ Mẫu'},
            'Đinh': {'Hóa Lộc': 'Tật Ách', 'Hóa Quyền': 'Phụ Mẫu', 'Hóa Khoa': 'Huynh Đệ', 'Hóa Kỵ': 'Quan Lộc'},
            'Mậu': {'Hóa Lộc': 'Huynh Đệ', 'Hóa Quyền': 'Thiên Di', 'Hóa Khoa': 'Quan Lộc', 'Hóa Kỵ': 'Tài Bạch'},
            'Kỷ': {'Hóa Lộc': 'Phúc Đức', 'Hóa Quyền': 'Tài Bạch', 'Hóa Khoa': 'Tật Ách', 'Hóa Kỵ': 'Phu Thê'},
            'Canh': {'Hóa Lộc': 'Nô Bộc', 'Hóa Quyền': 'Phúc Đức', 'Hóa Khoa': 'Mệnh', 'Hóa Kỵ': 'Thiên Di'},
            'Tân': {'Hóa Lộc': 'Quan Lộc', 'Hóa Quyền': 'Tật Ách', 'Hóa Khoa': 'Tử Tức', 'Hóa Kỵ': 'Phúc Đức'},
            'Nhâm': {'Hóa Lộc': 'Mệnh', 'Hóa Quyền': 'Huynh Đệ', 'Hóa Khoa': 'Tài Bạch', 'Hóa Kỵ': 'Nô Bộc'},
            'Quý': {'Hóa Lộc': 'Phụ Mẫu', 'Hóa Quyền': 'Phu Thê', 'Hóa Khoa': 'Điền Trạch', 'Hóa Kỵ': 'Tử Tức'}
        }
        return tu_hoa_mapping.get(thien_can, {})
    
    def _get_loc_ton_position(self, thien_can: str) -> int:
        """Tính vị trí Lộc Tồn theo thiên can"""
        loc_ton_mapping = {
            'Giáp': 0, 'Ất': 1, 'Bính': 2, 'Đinh': 3, 'Mậu': 4, 'Kỷ': 5,
            'Canh': 6, 'Tân': 7, 'Nhâm': 8, 'Quý': 9
        }
        return loc_ton_mapping.get(thien_can, 0)
    
    def _get_thien_ma_position(self, year: int) -> int:
        """Tính vị trí Thiên Mã theo chi năm sinh"""
        chi_index = year % 12
        # Thiên Mã theo tam hợp: Dần Ngọ Tuất -> Thân, Thân Tý Thìn -> Dần, Tỵ Dậu Sửu -> Hợi, Hợi Mão Mùi -> Tỵ
        ma_mapping = {
            1: 8,  # Sửu -> Thân
            2: 8,  # Dần -> Thân  
            3: 11, # Mão -> Hợi
            4: 2,  # Thìn -> Dần
            5: 11, # Tỵ -> Hợi
            6: 8,  # Ngọ -> Thân
            7: 11, # Mùi -> Hợi
            8: 2,  # Thân -> Dần
            9: 11, # Dậu -> Hợi
            10: 8, # Tuất -> Thân
            11: 5, # Hợi -> Tỵ
            0: 2   # Tý -> Dần
        }
        return ma_mapping.get(chi_index, 0)
    
    def _get_hoa_tinh_position(self, hour: int) -> int:
        """Tính vị trí Hỏa Tinh theo giờ sinh"""
        # Hỏa Tinh: Tý Dần Thìn Ngọ Thân Tuất
        hoa_positions = [0, 2, 4, 6, 8, 10]
        return hoa_positions[hour % 6]
    
    def _get_linh_tinh_position(self, hour: int) -> int:
        """Tính vị trí Linh Tinh theo giờ sinh"""
        # Linh Tinh: Sửu Mão Tỵ Mùi Dậu Hợi
        linh_positions = [1, 3, 5, 7, 9, 11]
        return linh_positions[hour % 6]
    
    def _get_thien_hinh_position(self, month: int) -> int:
        """Tính vị trí Thiên Hình theo tháng sinh"""
        # Thiên Hình khởi từ cung Tỵ theo tháng sinh
        return (4 + month) % 12  # Tỵ = 5, index 4
    
    def _get_thien_rieu_position(self, month: int) -> int:
        """Tính vị trí Thiên Riêu theo tháng sinh"""
        # Thiên Riêu khởi từ cung Dậu theo tháng sinh
        return (8 + month) % 12  # Dậu = 9, index 8
    
    def get_star_category(self, star_name: str) -> str:
        """Lấy phân loại sao (Nam Đẩu/Bắc Đẩu/Trung tinh/Phụ tinh)"""
        nam_dau = ['Thái Dương', 'Thiên Cơ', 'Thiên Đồng', 'Thiên Lương', 'Thiên Tướng', 'Thất Sát']
        bac_dau = ['Thái Âm', 'Vũ Khúc', 'Tham Lang', 'Liêm Trinh', 'Phá Quân', 'Cự Môn']
        nam_bac_dau = ['Tử Vi', 'Thiên Phủ']
        trung_tinh = ['Văn Xương', 'Văn Khúc', 'Tả Phụ', 'Hữu Bật', 'Thiên Khôi', 'Thiên Việt', 'Lộc Tồn', 'Thiên Mã']
        phu_tinh = ['Kình Dương', 'Đà La', 'Hỏa Tinh', 'Linh Tinh', 'Địa Không', 'Địa Kiếp', 'Thiên Hình', 'Thiên Riêu']
        
        if star_name in nam_dau:
            return 'Nam Đẩu'
        elif star_name in bac_dau:
            return 'Bắc Đẩu'
        elif star_name in nam_bac_dau:
            return 'Nam Bắc Đẩu'
        elif star_name in trung_tinh:
            return 'Trung tinh'
        elif star_name in phu_tinh:
            return 'Phụ tinh'
        else:
            return 'Khác'
    
    def get_star_element(self, star_name: str) -> str:
        """Lấy ngũ hành của sao"""
        star_elements = {
            'Tử Vi': 'Thổ', 'Thiên Phủ': 'Thổ', 'Thiên Cơ': 'Mộc', 'Thiên Đồng': 'Thủy',
            'Thái Dương': 'Hỏa', 'Thái Âm': 'Thủy', 'Thiên Lương': 'Mộc', 'Vũ Khúc': 'Kim',
            'Thất Sát': 'Kim', 'Phá Quân': 'Thủy', 'Liêm Trinh': 'Hỏa', 'Tham Lang': 'Thủy',
            'Cự Môn': 'Thủy', 'Thiên Tướng': 'Thủy', 'Văn Xương': 'Kim', 'Văn Khúc': 'Thủy',
            'Tả Phụ': 'Thổ', 'Hữu Bật': 'Thổ', 'Thiên Khôi': 'Hỏa', 'Thiên Việt': 'Hỏa',
            'Lộc Tồn': 'Thổ', 'Thiên Mã': 'Hỏa', 'Kình Dương': 'Hỏa', 'Đà La': 'Kim',
            'Hỏa Tinh': 'Hỏa', 'Linh Tinh': 'Hỏa', 'Địa Không': 'Hỏa', 'Địa Kiếp': 'Hỏa',
            'Thiên Hình': 'Kim', 'Thiên Riêu': 'Thủy'
        }
        return star_elements.get(star_name, 'Thổ')
    
    def get_star_characteristics(self, star_name: str) -> Dict[str, str]:
        """Lấy đặc tính và ý nghĩa của sao"""
        characteristics = {
            'Tử Vi': {
                'nature': 'Chủ tinh, Đế tinh',
                'meaning': 'Thống lĩnh, quyền quý, danh vọng, lãnh đạo',
                'personality': 'Cao quý, có khí chất lãnh đạo, tự tin, kiêu hãnh'
            },
            'Thiên Phủ': {
                'nature': 'Nam Đẩu chủ tinh',
                'meaning': 'Tài chính, bảo thủ, ổn định, quản lý',
                'personality': 'Thận trọng, có tài quản lý, yêu thích sự ổn định'
            },
            'Thiên Cơ': {
                'nature': 'Nam Đẩu thiện tinh',
                'meaning': 'Thông minh, linh hoạt, biến động, sáng tạo',
                'personality': 'Lanh lợi, thích biến đổi, có óc sáng tạo'
            },
            'Thiên Đồng': {
                'nature': 'Nam Đẩu phúc tinh',
                'meaning': 'An nhàn, hưởng thụ, phúc khí, tình cảm',
                'personality': 'Hiền hòa, thích hưởng thụ, có phúc khí'
            },
            'Thái Dương': {
                'nature': 'Nam Đẩu quý tinh',
                'meaning': 'Công danh, quyền lực, nam tính, cha',
                'personality': 'Mạnh mẽ, có khí phách, thích giúp đỡ người khác'
            },
            'Thái Âm': {
                'nature': 'Bắc Đẩu phúc tinh',
                'meaning': 'Tài lộc, nữ tính, mẹ, dịu dàng',
                'personality': 'Dịu dàng, có tài quản lý tài chính, nội tâm'
            },
            'Thiên Lương': {
                'nature': 'Nam Đẩu ấn tinh',
                'meaning': 'Chính trực, công lý, y học, luật pháp',
                'personality': 'Ngay thẳng, có lòng công lý, thích giúp đỡ'
            },
            'Vũ Khúc': {
                'nature': 'Bắc Đẩu tướng tinh',
                'meaning': 'Võ lực, quyết đoán, cương nghị, quân sự',
                'personality': 'Quyết đoán, có tính cách mạnh mẽ, thích võ'
            },
            'Thất Sát': {
                'nature': 'Nam Đẩu tướng tinh',
                'meaning': 'Cô độc, quyền lực, kiên cường, binh quyền',
                'personality': 'Độc lập, có tính lãnh đạo, đôi khi cô đơn'
            },
            'Phá Quân': {
                'nature': 'Bắc Đẩu sát tinh',
                'meaning': 'Phá hoại, đổi mới, biến động, cách mạng',
                'personality': 'Thích đổi mới, có tính phá cách, năng động'
            },
            'Liêm Trinh': {
                'nature': 'Bắc Đẩu sát tinh',
                'meaning': 'Tình dục, quan hệ, nghệ thuật, hoa nguyệt',
                'personality': 'Có khí chất nghệ sỹ, quan tâm đến tình cảm'
            },
            'Tham Lang': {
                'nature': 'Bắc Đẩu sát tinh',
                'meaning': 'Ham muốn, nghệ thuật, tài năng, đa dạng',
                'personality': 'Đa tài, thích khám phá, có nhiều sở thích'
            },
            'Cự Môn': {
                'nature': 'Bắc Đẩu ám tinh',
                'meaning': 'Tranh luận, khẩu thiệt, pháp luật, biện luận',
                'personality': 'Giỏi nói, thích tranh luận, có lý lẽ'
            },
            'Thiên Tướng': {
                'nature': 'Nam Đẩu ấn tinh',
                'meaning': 'Phò tá, giúp đỡ, tổ chức, quản lý',
                'personality': 'Tốt bụng, thích giúp đỡ, có tài tổ chức'
            }
        }
        return characteristics.get(star_name, {
            'nature': 'Chưa xác định',
            'meaning': 'Chưa có thông tin',
            'personality': 'Chưa có thông tin'
        })
    
    def _calculate_fortune_periods(self, birth_year: int, gender: str, menh_cung_chi: str, thien_can: str) -> Dict[str, Any]:
        """Tính toán các vận hạn"""
        current_year = datetime.now().year
        current_month = datetime.now().month
        current_day = datetime.now().day
        
        # Tính đại vận
        dai_van = self._calculate_dai_van(birth_year, gender, menh_cung_chi)
        
        # Tính tiểu vận
        tieu_van = self._calculate_tieu_van(current_year, birth_year, thien_can)
        
        # Tính lưu tháng
        luu_thang = self._calculate_luu_thang(current_year, current_month, 1)  # birth_month = 1 default
        
        # Tính lưu ngày
        luu_ngay = self._calculate_luu_ngay(current_day, 1)  # birth_day = 1 default
        
        return {
            'dai_van': dai_van,
            'tieu_van': tieu_van,
            'luu_thang': luu_thang,
            'luu_ngay': luu_ngay
        }
    
    def _calculate_dai_van(self, birth_year: int, gender: str, menh_cung_chi: str) -> List[Dict[str, Any]]:
        """Tính đại vận (10 năm/cung)"""
        menh_index = self.chi_positions.index(menh_cung_chi)
        is_forward = (gender == 'Nam')
        
        dai_van = []
        current_age = 10
        
        for i in range(12):
            if is_forward:
                cung_index = (menh_index + i) % 12
            else:
                cung_index = (menh_index - i) % 12
            
            cung_name = self.cung_names[cung_index]
            chi_name = self.chi_positions[cung_index]
            
            dai_van.append({
                'age_range': f"{current_age}-{current_age + 9}",
                'cung': cung_name,
                'chi': chi_name,
                'start_age': current_age,
                'end_age': current_age + 9
            })
            
            current_age += 10
        
        return dai_van
    
    def _calculate_tieu_van(self, current_year: int, birth_year: int, thien_can_year: str) -> Dict[str, Any]:
        """Tính tiểu vận (lưu niên)"""
        age = current_year - birth_year + 1
        
        can_names = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý']
        can_index = current_year % 10
        current_can = can_names[can_index]
        
        chi_index = current_year % 12
        current_chi = self.chi_positions[chi_index]
        
        current_tu_hoa = self._get_tu_hoa_stars(current_can)
        
        return {
            'year': current_year,
            'age': age,
            'can_chi': f"{current_can} {current_chi}",
            'tu_hoa': current_tu_hoa,
            'description': f"Lưu niên {current_year} ({current_can} {current_chi})"
        }
    
    def _calculate_luu_thang(self, current_year: int, current_month: int, birth_month: int) -> Dict[str, Any]:
        """Tính lưu tháng"""
        luu_thang = (current_month - birth_month + 1) % 12
        if luu_thang == 0:
            luu_thang = 12
        
        chi_index = (current_month - 1) % 12
        current_chi = self.chi_positions[chi_index]
        
        return {
            'month': current_month,
            'luu_thang': luu_thang,
            'chi': current_chi,
            'description': f"Lưu tháng {luu_thang} ({current_chi})"
        }
    
    def _calculate_luu_ngay(self, current_day: int, birth_day: int) -> Dict[str, Any]:
        """Tính lưu ngày"""
        luu_ngay = (current_day - birth_day + 1) % 30
        if luu_ngay == 0:
            luu_ngay = 30
        
        chi_index = (current_day - 1) % 12
        current_chi = self.chi_positions[chi_index]
        
        return {
            'day': current_day,
            'luu_ngay': luu_ngay,
            'chi': current_chi,
            'description': f"Lưu ngày {luu_ngay} ({current_chi})"
        }
    
    def _generate_fortune_analysis(self, sao_cung: Dict[str, List[str]], fortune: Dict[str, Any], birth_year: int) -> Dict[str, Any]:
        """Tạo phân tích vận mệnh"""
        current_age = datetime.now().year - birth_year + 1
        
        # Tìm đại vận hiện tại
        current_dai_van = None
        for van in fortune['dai_van']:
            if van['start_age'] <= current_age <= van['end_age']:
                current_dai_van = van
                break
        
        # Tính điểm 4 trụ chính (simplified)
        four_pillars = {
            'cong_viec': 0.5,  # Simplified scoring
            'tai_chinh': 0.5,
            'tinh_cam': 0.5,
            'suc_khoe': 0.5
        }
        
        return {
            'four_pillars': four_pillars,
            'current_dai_van': current_dai_van,
            'tieu_van': fortune['tieu_van'],
            'cung_scores': {}  # Simplified
        }
    
    def _generate_guidance_recommendations(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo khuyến nghị"""
        four_pillars = analysis['four_pillars']
        overall_score = sum(four_pillars.values()) / 4
        
        if overall_score >= 1.5:
            kim_chi_nam = "Năm nay là thời điểm rất thuận lợi. Nên chủ động nắm bắt cơ hội."
        elif overall_score >= 0.5:
            kim_chi_nam = "Năm nay có xu hướng tích cực. Nên tập trung vào việc cải thiện."
        elif overall_score <= -0.5:
            kim_chi_nam = "Năm nay cần thận trọng. Nên tập trung vào việc ổn định."
        else:
            kim_chi_nam = "Năm nay ở mức ổn định. Nên duy trì hiện trạng."
        
        return {
            'recommendations': [],
            'kim_chi_nam': kim_chi_nam,
            'overall_score': round(overall_score, 1)
        }
    
    def _init_star_strength_map(self) -> Dict[str, Dict[str, str]]:
        """Khởi tạo mapping độ mạnh sao theo 12 cung"""
        return {
            # 14 Sao Chính
            'Tử Vi': {
                'Tý': 'hãm', 'Sửu': 'hãm', 'Dần': 'vượng', 'Mão': 'vượng', 
                'Thìn': 'miếu', 'Tỵ': 'miếu', 'Ngọ': 'miếu', 'Mùi': 'miếu', 
                'Thân': 'bình', 'Dậu': 'bình', 'Tuất': 'nhược', 'Hợi': 'nhược'
            },
            'Thiên Phủ': {
                'Tý': 'miếu', 'Sửu': 'miếu', 'Dần': 'bình', 'Mão': 'bình', 
                'Thìn': 'vượng', 'Tỵ': 'vượng', 'Ngọ': 'vượng', 'Mùi': 'vượng', 
                'Thân': 'hãm', 'Dậu': 'hãm', 'Tuất': 'nhược', 'Hợi': 'nhược'
            },
            'Thiên Cơ': {
                'Tý': 'bình', 'Sửu': 'vượng', 'Dần': 'miếu', 'Mão': 'miếu', 
                'Thìn': 'bình', 'Tỵ': 'hãm', 'Ngọ': 'hãm', 'Mùi': 'nhược', 
                'Thân': 'nhược', 'Dậu': 'bình', 'Tuất': 'vượng', 'Hợi': 'miếu'
            },
            'Thiên Đồng': {
                'Tý': 'miếu', 'Sửu': 'vượng', 'Dần': 'bình', 'Mão': 'hãm', 
                'Thìn': 'nhược', 'Tỵ': 'hãm', 'Ngọ': 'miếu', 'Mùi': 'vượng', 
                'Thân': 'bình', 'Dậu': 'hãm', 'Tuất': 'nhược', 'Hợi': 'miếu'
            },
            'Thái Dương': {
                'Tý': 'hãm', 'Sửu': 'nhược', 'Dần': 'vượng', 'Mão': 'miếu', 
                'Thìn': 'miếu', 'Tỵ': 'miếu', 'Ngọ': 'vượng', 'Mùi': 'bình', 
                'Thân': 'hãm', 'Dậu': 'nhược', 'Tuất': 'hãm', 'Hợi': 'hãm'
            },
            'Thái Âm': {
                'Tý': 'miếu', 'Sửu': 'vượng', 'Dần': 'bình', 'Mão': 'hãm', 
                'Thìn': 'nhược', 'Tỵ': 'hãm', 'Ngọ': 'hãm', 'Mùi': 'nhược', 
                'Thân': 'bình', 'Dậu': 'vượng', 'Tuất': 'miếu', 'Hợi': 'miếu'
            },
            'Thiên Lương': {
                'Tý': 'bình', 'Sửu': 'hãm', 'Dần': 'vượng', 'Mão': 'miếu', 
                'Thìn': 'bình', 'Tỵ': 'nhược', 'Ngọ': 'miếu', 'Mùi': 'vượng', 
                'Thân': 'bình', 'Dậu': 'hãm', 'Tuất': 'nhược', 'Hợi': 'bình'
            },
            'Vũ Khúc': {
                'Tý': 'bình', 'Sửu': 'miếu', 'Dần': 'nhược', 'Mão': 'hãm', 
                'Thìn': 'vượng', 'Tỵ': 'bình', 'Ngọ': 'hãm', 'Mùi': 'nhược', 
                'Thân': 'vượng', 'Dậu': 'bình', 'Tuất': 'miếu', 'Hợi': 'bình'
            },
            'Thất Sát': {
                'Tý': 'miếu', 'Sửu': 'vượng', 'Dần': 'bình', 'Mão': 'hãm', 
                'Thìn': 'bình', 'Tỵ': 'nhược', 'Ngọ': 'miếu', 'Mùi': 'vượng', 
                'Thân': 'bình', 'Dậu': 'hãm', 'Tuất': 'bình', 'Hợi': 'nhược'
            },
            'Phá Quân': {
                'Tý': 'bình', 'Sửu': 'hãm', 'Dần': 'vượng', 'Mão': 'miếu', 
                'Thìn': 'bình', 'Tỵ': 'hãm', 'Ngọ': 'bình', 'Mùi': 'nhược', 
                'Thân': 'vượng', 'Dậu': 'hãm', 'Tuất': 'bình', 'Hợi': 'miếu'
            },
            'Liêm Trinh': {
                'Tý': 'vượng', 'Sửu': 'miếu', 'Dần': 'bình', 'Mão': 'bình', 
                'Thìn': 'vượng', 'Tỵ': 'hãm', 'Ngọ': 'bình', 'Mùi': 'miếu', 
                'Thân': 'bình', 'Dậu': 'bình', 'Tuất': 'vượng', 'Hợi': 'hãm'
            },
            'Tham Lang': {
                'Tý': 'bình', 'Sửu': 'nhược', 'Dần': 'miếu', 'Mão': 'vượng', 
                'Thìn': 'bình', 'Tỵ': 'bình', 'Ngọ': 'miếu', 'Mùi': 'vượng', 
                'Thân': 'bình', 'Dậu': 'nhược', 'Tuất': 'bình', 'Hợi': 'hãm'
            },
            'Cự Môn': {
                'Tý': 'bình', 'Sửu': 'hãm', 'Dần': 'vượng', 'Mão': 'miếu', 
                'Thìn': 'miếu', 'Tỵ': 'bình', 'Ngọ': 'hãm', 'Mùi': 'nhược', 
                'Thân': 'vượng', 'Dậu': 'bình', 'Tuất': 'nhược', 'Hợi': 'bình'
            },
            'Thiên Tướng': {
                'Tý': 'vượng', 'Sửu': 'miếu', 'Dần': 'bình', 'Mão': 'miếu', 
                'Thìn': 'vượng', 'Tỵ': 'bình', 'Ngọ': 'miếu', 'Mùi': 'vượng', 
                'Thân': 'bình', 'Dậu': 'bình', 'Tuất': 'hãm', 'Hợi': 'nhược'
            },
            # Văn tinh
            'Văn Xương': {
                'Tý': 'hãm', 'Sửu': 'miếu', 'Dần': 'vượng', 'Mão': 'miếu', 
                'Thìn': 'bình', 'Tỵ': 'miếu', 'Ngọ': 'hãm', 'Mùi': 'vượng', 
                'Thân': 'bình', 'Dậu': 'miếu', 'Tuất': 'hãm', 'Hợi': 'bình'
            },
            'Văn Khúc': {
                'Tý': 'bình', 'Sửu': 'miếu', 'Dần': 'hãm', 'Mão': 'vượng', 
                'Thìn': 'bình', 'Tỵ': 'miếu', 'Ngọ': 'hãm', 'Mùi': 'bình', 
                'Thân': 'vượng', 'Dậu': 'miếu', 'Tuất': 'hãm', 'Hợi': 'miếu'
            },
            # Tả Hữu
            'Tả Phụ': {
                'Tý': 'miếu', 'Sửu': 'miếu', 'Dần': 'miếu', 'Mão': 'miếu', 
                'Thìn': 'miếu', 'Tỵ': 'miếu', 'Ngọ': 'miếu', 'Mùi': 'miếu', 
                'Thân': 'miếu', 'Dậu': 'miếu', 'Tuất': 'miếu', 'Hợi': 'miếu'
            },
            'Hữu Bật': {
                'Tý': 'miếu', 'Sửu': 'miếu', 'Dần': 'miếu', 'Mão': 'miếu', 
                'Thìn': 'miếu', 'Tỵ': 'miếu', 'Ngọ': 'miếu', 'Mùi': 'miếu', 
                'Thân': 'miếu', 'Dậu': 'miếu', 'Tuất': 'miếu', 'Hợi': 'miếu'
            },
            # Khôi Việt
            'Thiên Khôi': {
                'Tý': 'miếu', 'Sửu': 'miếu', 'Dần': 'miếu', 'Mão': 'miếu', 
                'Thìn': 'miếu', 'Tỵ': 'miếu', 'Ngọ': 'miếu', 'Mùi': 'miếu', 
                'Thân': 'miếu', 'Dậu': 'miếu', 'Tuất': 'miếu', 'Hợi': 'miếu'
            },
            'Thiên Việt': {
                'Tý': 'miếu', 'Sửu': 'miếu', 'Dần': 'miếu', 'Mão': 'miếu', 
                'Thìn': 'miếu', 'Tỵ': 'miếu', 'Ngọ': 'miếu', 'Mùi': 'miếu', 
                'Thân': 'miếu', 'Dậu': 'miếu', 'Tuất': 'miếu', 'Hợi': 'miếu'
            }
        }
    
    def _init_star_weights(self) -> Dict[str, Dict[str, int]]:
        """Khởi tạo mapping trọng số sao theo cung - ảnh hưởng đến từng cung"""
        return {
            # 14 Sao Chính - trọng số cao
            'Tử Vi': {
                'Mệnh': 5, 'Quan Lộc': 4, 'Tài Bạch': 3, 'Phúc Đức': 3, 
                'Phu Thê': 2, 'Tử Tức': 2, 'Điền Trạch': 2, 'Phụ Mẫu': 1
            },
            'Thiên Phủ': {
                'Tài Bạch': 5, 'Mệnh': 4, 'Điền Trạch': 3, 'Quan Lộc': 3, 
                'Phúc Đức': 2, 'Phu Thê': 2, 'Tử Tức': 2, 'Phụ Mẫu': 1
            },
            'Thiên Cơ': {
                'Mệnh': 4, 'Huynh Đệ': 4, 'Quan Lộc': 3, 'Thiên Di': 3, 
                'Tài Bạch': 2, 'Phu Thê': 2, 'Phúc Đức': 2, 'Nô Bộc': 1
            },
            'Thiên Đồng': {
                'Phúc Đức': 5, 'Mệnh': 4, 'Phu Thê': 3, 'Tử Tức': 3, 
                'Phụ Mẫu': 2, 'Huynh Đệ': 2, 'Nô Bộc': 2, 'Tài Bạch': 1
            },
            'Thái Dương': {
                'Quan Lộc': 5, 'Mệnh': 4, 'Phụ Mẫu': 4, 'Phu Thê': 3, 
                'Tài Bạch': 2, 'Phúc Đức': 2, 'Huynh Đệ': 2, 'Tử Tức': 1
            },
            'Thái Âm': {
                'Tài Bạch': 5, 'Mệnh': 4, 'Phụ Mẫu': 4, 'Phu Thê': 3, 
                'Tử Tức': 3, 'Điền Trạch': 2, 'Phúc Đức': 2, 'Quan Lộc': 1
            },
            'Thiên Lương': {
                'Phụ Mẫu': 5, 'Mệnh': 4, 'Phúc Đức': 4, 'Quan Lộc': 3, 
                'Tật Ách': 3, 'Huynh Đệ': 2, 'Phu Thê': 2, 'Tài Bạch': 1
            },
            'Vũ Khúc': {
                'Quan Lộc': 5, 'Mệnh': 4, 'Tài Bạch': 3, 'Huynh Đệ': 3, 
                'Phúc Đức': 2, 'Phu Thê': 2, 'Tử Tức': 2, 'Phụ Mẫu': 1
            },
            'Thất Sát': {
                'Quan Lộc': 5, 'Mệnh': 4, 'Thiên Di': 4, 'Huynh Đệ': 3, 
                'Tài Bạch': 2, 'Phu Thê': 2, 'Nô Bộc': 2, 'Phúc Đức': 1
            },
            'Phá Quân': {
                'Mệnh': 5, 'Thiên Di': 4, 'Tài Bạch': 3, 'Quan Lộc': 3, 
                'Phu Thê': 3, 'Huynh Đệ': 2, 'Tử Tức': 2, 'Phúc Đức': 1
            },
            'Liêm Trinh': {
                'Mệnh': 4, 'Quan Lộc': 4, 'Phu Thê': 4, 'Tài Bạch': 3, 
                'Phúc Đức': 2, 'Tử Tức': 2, 'Huynh Đệ': 2, 'Phụ Mẫu': 1
            },
            'Tham Lang': {
                'Mệnh': 4, 'Phu Thê': 4, 'Tài Bạch': 4, 'Phúc Đức': 3, 
                'Tử Tức': 2, 'Thiên Di': 2, 'Huynh Đệ': 2, 'Quan Lộc': 1
            },
            'Cự Môn': {
                'Mệnh': 4, 'Huynh Đệ': 4, 'Quan Lộc': 3, 'Tật Ách': 3, 
                'Phu Thê': 3, 'Tài Bạch': 2, 'Phúc Đức': 2, 'Phụ Mẫu': 1
            },
            'Thiên Tướng': {
                'Mệnh': 4, 'Quan Lộc': 4, 'Phúc Đức': 3, 'Tài Bạch': 3, 
                'Phu Thê': 2, 'Tử Tức': 2, 'Phụ Mẫu': 2, 'Huynh Đệ': 1
            },
            # Văn tinh - trọng số trung bình
            'Văn Xương': {
                'Quan Lộc': 3, 'Mệnh': 2, 'Phúc Đức': 2, 'Tử Tức': 2, 
                'Huynh Đệ': 1, 'Tài Bạch': 1, 'Phu Thê': 1, 'Phụ Mẫu': 1
            },
            'Văn Khúc': {
                'Quan Lộc': 3, 'Mệnh': 2, 'Phúc Đức': 2, 'Tử Tức': 2, 
                'Huynh Đệ': 1, 'Tài Bạch': 1, 'Phu Thê': 1, 'Phụ Mẫu': 1
            },
            # Tả Hữu - trọng số cao
            'Tả Phụ': {
                'Mệnh': 3, 'Quan Lộc': 3, 'Tài Bạch': 2, 'Phúc Đức': 2, 
                'Phu Thê': 2, 'Tử Tức': 2, 'Phụ Mẫu': 1, 'Huynh Đệ': 1
            },
            'Hữu Bật': {
                'Mệnh': 3, 'Quan Lộc': 3, 'Tài Bạch': 2, 'Phúc Đức': 2, 
                'Phu Thê': 2, 'Tử Tức': 2, 'Phụ Mẫu': 1, 'Huynh Đệ': 1
            },
            # Khôi Việt - trọng số trung bình
            'Thiên Khôi': {
                'Quan Lộc': 2, 'Mệnh': 2, 'Phúc Đức': 2, 'Tử Tức': 1, 
                'Tài Bạch': 1, 'Phu Thê': 1, 'Phụ Mẫu': 1, 'Huynh Đệ': 1
            },
            'Thiên Việt': {
                'Quan Lộc': 2, 'Mệnh': 2, 'Phúc Đức': 2, 'Tử Tức': 1, 
                'Tài Bạch': 1, 'Phu Thê': 1, 'Phụ Mẫu': 1, 'Huynh Đệ': 1
            }
        }
