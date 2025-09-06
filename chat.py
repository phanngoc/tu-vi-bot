from llama_index.core import VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from lunarcalendar import Converter, Solar
from datetime import datetime

import os
from dotenv import load_dotenv
from llama_index.core import Settings

from llama_index.core.tools import FunctionTool
from enum import Enum
from pydantic import BaseModel, Field
from typing import List
from llama_index.core.program import FunctionCallingProgram
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
)

MODEL_NAME = "gpt-4o-mini"
MODEL_EMBEDDING_NAME = "text-embedding-3-small"

load_dotenv()  # take environment variables from .env.
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

embed_model = OpenAIEmbedding(model=MODEL_EMBEDDING_NAME, dimensions=1536)
llm = OpenAI(model=MODEL_NAME)


def convert_to_lunar(year, month, day):
    solar = Solar(year, month, day)
    lunar = Converter.Solar2Lunar(solar)
    return lunar


def get_thien_can_dia_chi(year):
    can = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý']
    chi = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
    can_index = year % 10
    chi_index = year % 12
    return can[can_index], chi[chi_index]


def get_cuc(thien_can):
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
    return None

def determine_menh_cung_position(birth_hour, birth_month):
    """Xác định vị trí cung Mệnh dựa vào giờ sinh và tháng sinh"""
    chi_positions = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
    
    hour_chi = chi_positions[birth_hour % 12]
    hour_index = chi_positions.index(hour_chi)
    
    menh_index = (hour_index + birth_month - 1) % 12
    return chi_positions[menh_index]

def get_trang_sinh_cycle(cuc_type, gender):
    """Lấy vòng Tràng Sinh theo cục và giới tính"""
    trang_sinh_positions = {
        'Kim': {'Nam': ['Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi', 'Tý', 'Sửu', 'Dần', 'Mão', 'Thìn'],
               'Nữ': ['Thìn', 'Mão', 'Dần', 'Sửu', 'Tý', 'Hợi', 'Tuất', 'Dậu', 'Thân', 'Mùi', 'Ngọ', 'Tỵ']},
        'Mộc': {'Nam': ['Hợi', 'Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất'],
               'Nữ': ['Tuất', 'Dậu', 'Thân', 'Mùi', 'Ngọ', 'Tỵ', 'Thìn', 'Mão', 'Dần', 'Sửu', 'Tý', 'Hợi']},
        'Thủy': {'Nam': ['Thân', 'Dậu', 'Tuất', 'Hợi', 'Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi'],
                'Nữ': ['Mùi', 'Ngọ', 'Tỵ', 'Thìn', 'Mão', 'Dần', 'Sửu', 'Tý', 'Hợi', 'Tuất', 'Dậu', 'Thân']},
        'Hỏa': {'Nam': ['Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi', 'Tý', 'Sửu'],
               'Nữ': ['Sửu', 'Tý', 'Hợi', 'Tuất', 'Dậu', 'Thân', 'Mùi', 'Ngọ', 'Tỵ', 'Thìn', 'Mão', 'Dần']},
        'Thổ': {'Nam': ['Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi', 'Tý', 'Sửu'],
               'Nữ': ['Sửu', 'Tý', 'Hợi', 'Tuất', 'Dậu', 'Thân', 'Mùi', 'Ngọ', 'Tỵ', 'Thìn', 'Mão', 'Dần']}
    }
    return trang_sinh_positions.get(cuc_type, {}).get(gender, [])


def get_gio_sinh(hour):
    gio_mapping = {
        'Tý': 0, 'Sửu': 1, 'Dần': 2, 'Mão': 3,
        'Thìn': 4, 'Tỵ': 5, 'Ngọ': 6, 'Mùi': 7,
        'Thân': 8, 'Dậu': 9, 'Tuất': 10, 'Hợi': 11
    }
    return list(gio_mapping.keys())[hour % 12]


def an_sao_tuvi_comprehensive(day, month, year, hour, gender):
    """Hệ thống an sao toàn diện theo phương pháp tử vi truyền thống"""
    cung_names = ['Mệnh', 'Phụ Mẫu', 'Phúc Đức', 'Điền Trạch', 'Quan Lộc', 'Nô Bộc', 
                  'Thiên Di', 'Tật Ách', 'Tài Bạch', 'Tử Tức', 'Phu Thê', 'Huynh Đệ']
    
    thien_can, dia_chi = get_thien_can_dia_chi(year)
    cuc = get_cuc(thien_can)
    gio_sinh = get_gio_sinh(hour)
    
    menh_cung_chi = determine_menh_cung_position(hour, month)
    trang_sinh_cycle = get_trang_sinh_cycle(cuc, gender)
    
    chi_positions = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
    menh_index = chi_positions.index(menh_cung_chi)
    
    cung_chi_mapping = {}
    for i, cung in enumerate(cung_names):
        chi_index = (menh_index + i) % 12
        cung_chi_mapping[chi_positions[chi_index]] = cung
    
    chinh_tinh_14 = {
        'Tử Vi': day % 12, 'Thiên Phủ': (day + 6) % 12, 
        'Thái Dương': (day + month) % 12, 'Thái Âm': (15 - day) % 12,
        'Thiên Cơ': (day + 1) % 12, 'Thiên Lương': (day + 7) % 12,
        'Vũ Khúc': (day - 1) % 12, 'Thiên Đồng': (day + 11) % 12,
        'Cự Môn': (day + 2) % 12, 'Liêm Trinh': (day + 8) % 12,
        'Thất Sát': (day + 5) % 12, 'Phá Quân': (day + 4) % 12,
        'Tham Lang': (day + 3) % 12, 'Thiên Tướng': (day + 9) % 12
    }
    
    cat_tinh = {
        'Tả Hữu': [(day + 1) % 12, (day - 1) % 12],
        'Khôi Việt': [(month + 3) % 12, (month + 9) % 12],
        'Xương Khúc': [(hour + 2) % 12, (hour + 8) % 12]
    }
    
    sat_tinh = {
        'Kình Dương': (hour + day) % 12,
        'Đà La': (hour - day) % 12,
        'Không Kiếp': [(year + 2) % 12, (year + 8) % 12]
    }
    
    tu_hoa_tinh = get_tu_hoa_stars(thien_can)
    
    sao_cung = {cung: [] for cung in cung_names}
    
    for sao, chi_index in chinh_tinh_14.items():
        chi_name = chi_positions[chi_index % 12]
        if chi_name in cung_chi_mapping:
            cung = cung_chi_mapping[chi_name]
            sao_cung[cung].append(sao)
    
    for sao, chi_indices in cat_tinh.items():
        for chi_index in chi_indices:
            chi_name = chi_positions[chi_index % 12]
            if chi_name in cung_chi_mapping:
                cung = cung_chi_mapping[chi_name]
                sao_cung[cung].append(sao)
    
    for sao, chi_index in sat_tinh.items():
        if isinstance(chi_index, list):
            for idx in chi_index:
                chi_name = chi_positions[idx % 12]
                if chi_name in cung_chi_mapping:
                    cung = cung_chi_mapping[chi_name]
                    sao_cung[cung].append(sao)
        else:
            chi_name = chi_positions[chi_index % 12]
            if chi_name in cung_chi_mapping:
                cung = cung_chi_mapping[chi_name]
                sao_cung[cung].append(sao)
    
    for sao, cung_name in tu_hoa_tinh.items():
        if cung_name in sao_cung:
            sao_cung[cung_name].append(sao)
    
    return {
        'basic_info': {
            'birth_info': f"{day}/{month}/{year} giờ {gio_sinh}",
            'thien_can': thien_can,
            'dia_chi': dia_chi, 
            'cuc': cuc,
            'gender': gender,
            'menh_cung': menh_cung_chi
        },
        'sao_cung': sao_cung,
        'trang_sinh': trang_sinh_cycle
    }

def get_tu_hoa_stars(thien_can):
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

# Session-based step-by-step information collection
class CollectionStep(Enum):
    GREETING = "greeting"
    COLLECT_NAME = "collect_name"
    COLLECT_BIRTHDAY = "collect_birthday" 
    COLLECT_BIRTH_TIME = "collect_birth_time"
    COLLECT_GENDER = "collect_gender"
    ANALYSIS = "analysis"
    COMPLETED = "completed"

# Global session storage (in production, use Redis or database)
user_sessions = {}

def get_or_create_session(user_id="default"):
    """Get or create user session for step-by-step collection"""
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            'step': CollectionStep.GREETING,
            'collected_info': {},
            'conversation_history': []
        }
    return user_sessions[user_id]

def reset_session(user_id="default"):
    """Reset user session"""
    user_sessions[user_id] = {
        'step': CollectionStep.GREETING,
        'collected_info': {},
        'conversation_history': []
    }

# ReActAgent Tools for step-by-step information collection

def extract_name_from_message(message: str) -> str:
    """Extract name from message using simple pattern matching"""
    import re
    
    # Look for common patterns like "tôi tên", "tên tôi là", "tên là"
    patterns = [
        r'tôi tên\s+([A-Za-zÀ-ỹ\s]+?)(?:\s*,|\s*sinh|\s*ngày|$)',
        r'tên tôi là\s+([A-Za-zÀ-ỹ\s]+?)(?:\s*,|\s*sinh|\s*ngày|$)',
        r'tên là\s+([A-Za-zÀ-ỹ\s]+?)(?:\s*,|\s*sinh|\s*ngày|$)',
        r'tên:\s*([A-Za-zÀ-ỹ\s]+?)(?:\s*,|\s*sinh|\s*ngày|$)',
        r'^([A-Za-zÀ-ỹ]+(?:\s+[A-Za-zÀ-ỹ]+){0,3})(?:\s*,|\s*sinh|\s*ngày)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, message.strip(), re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            if len(name) >= 2 and not any(char.isdigit() for char in name):  # At least 2 characters and no numbers
                return f"Tên được xác nhận: {name}"
    
    return "Chưa thể xác định tên. Vui lòng cung cấp tên của bạn rõ ràng."

def extract_birth_date_from_message(message: str) -> str:
    """Extract birth date from message using regex"""
    import re
    
    # Look for DD/MM/YYYY pattern
    pattern = r'\b(\d{1,2})/(\d{1,2})/(\d{4})\b'
    match = re.search(pattern, message)
    
    if match:
        day, month, year = match.groups()
        try:
            # Validate date
            datetime.strptime(f"{day}/{month}/{year}", "%d/%m/%Y")
            return f"Ngày sinh được xác nhận: {day}/{month}/{year}"
        except:
            return "Ngày sinh không hợp lệ. Vui lòng cung cấp theo định dạng DD/MM/YYYY."
    
    return "Chưa thể xác định ngày sinh. Vui lòng cung cấp theo định dạng DD/MM/YYYY."

def extract_birth_time_from_message(message: str) -> str:
    """Extract birth time from message using regex"""
    import re
    
    # Look for HH:MM pattern
    pattern = r'\b(\d{1,2}):(\d{2})\b'
    match = re.search(pattern, message)
    
    if match:
        hour, minute = match.groups()
        try:
            hour_int = int(hour)
            minute_int = int(minute)
            if 0 <= hour_int <= 23 and 0 <= minute_int <= 59:
                return f"Giờ sinh được xác nhận: {hour.zfill(2)}:{minute}"
            else:
                return "Giờ sinh không hợp lệ. Vui lòng cung cấp giờ từ 00:00 đến 23:59."
        except:
            return "Giờ sinh không hợp lệ. Vui lòng cung cấp theo định dạng HH:MM."
    
    return "Chưa thể xác định giờ sinh. Vui lòng cung cấp theo định dạng HH:MM."

def extract_gender_from_message(message: str) -> str:
    """Extract gender from message"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['nam', 'male', 'boy', 'trai']):
        return "Giới tính được xác nhận: Nam"
    elif any(word in message_lower for word in ['nữ', 'female', 'girl', 'gái']):
        return "Giới tính được xác nhận: Nữ"
    else:
        return "Chưa thể xác định giới tính. Vui lòng chọn Nam hoặc Nữ."

def provide_guidance_for_missing_info(current_info: str) -> str:
    """Provide specific guidance based on what information is missing"""
    missing = []
    
    if "chưa thể xác định tên" in current_info.lower():
        missing.append("tên (ví dụ: Tôi tên Nguyễn Văn A)")
    if "chưa thể xác định ngày sinh" in current_info.lower():
        missing.append("ngày sinh (ví dụ: 15/03/1990)")
    if "chưa thể xác định giờ sinh" in current_info.lower():
        missing.append("giờ sinh (ví dụ: 14:30)")
    if "chưa thể xác định giới tính" in current_info.lower():
        missing.append("giới tính (Nam hoặc Nữ)")
    
    if missing:
        return f"Vui lòng cung cấp thêm: {', '.join(missing)}. Ví dụ đầy đủ: 'Tôi tên Nguyễn Văn A, sinh ngày 15/03/1990, 14:30, giới tính Nam'"
    else:
        return "Thông tin đã đầy đủ. Có thể tiến hành phân tích tử vi."

# Step-by-step collection tools for ReActAgent

def process_step_1_name(message: str, user_id: str = "default") -> str:
    """Step 1: Process and validate name input"""
    session = get_or_create_session(user_id)
    
    name_result = extract_name_from_message(message)
    
    if "được xác nhận" in name_result:
        # Extract name
        import re
        name = re.search(r'Tên được xác nhận: (.+)', name_result).group(1)
        session['collected_info']['name'] = name
        session['step'] = CollectionStep.COLLECT_BIRTHDAY
        
        return f"""✅ **Tên đã được ghi nhận: {name}**

📅 **Bước 2/4: Ngày và giờ sinh**
Bây giờ tôi cần biết ngày và giờ sinh của bạn để tính toán chính xác.

Vui lòng cho biết:
- **Ngày sinh** (định dạng DD/MM/YYYY)
- **Giờ sinh** (định dạng HH:MM - rất quan trọng cho việc xác định cung Mệnh)

*Ví dụ: "Tôi sinh ngày 15/03/1990, 14:30" hoặc "15/03/1990, 2:30 chiều"*"""
    else:
        return f"""🔮 **Chào mừng bạn đến với dịch vụ tư vấn tử vi!**

📝 **Bước 1/4: Tên của bạn**
{name_result}

*Ví dụ: "Tôi tên Nguyễn Văn A" hoặc "Tên tôi là Phan Ngọc"*"""

def process_step_2_birthday_time(message: str, user_id: str = "default") -> str:
    """Step 2: Process birthday and birth time"""
    session = get_or_create_session(user_id)
    
    date_result = extract_birth_date_from_message(message)
    time_result = extract_birth_time_from_message(message)
    
    name = session['collected_info'].get('name', 'bạn')
    
    date_confirmed = "được xác nhận" in date_result
    time_confirmed = "được xác nhận" in time_result
    
    if date_confirmed and time_confirmed:
        # Both confirmed
        import re
        birthday = re.search(r'Ngày sinh được xác nhận: (.+)', date_result).group(1)
        birth_time = re.search(r'Giờ sinh được xác nhận: (.+)', time_result).group(1)
        
        session['collected_info']['birthday'] = birthday
        session['collected_info']['birth_time'] = birth_time
        session['step'] = CollectionStep.COLLECT_GENDER
        
        return f"""✅ **Thông tin thời gian đã được ghi nhận:**
- 📅 Ngày sinh: {birthday}  
- 🕐 Giờ sinh: {birth_time}

⚥ **Bước 3/4: Giới tính**
Cuối cùng, tôi cần biết giới tính của {name} để tính toán vòng Tràng Sinh chính xác.

Vui lòng cho biết giới tính: **Nam** hoặc **Nữ**

*Ví dụ: "Nam", "Nữ", "Giới tính Nam", "Tôi là nữ"*"""
    
    elif date_confirmed:
        # Only date confirmed
        import re
        birthday = re.search(r'Ngày sinh được xác nhận: (.+)', date_result).group(1)
        session['collected_info']['birthday'] = birthday
        
        # Check if we already have birth_time from previous input
        if 'birth_time' in session['collected_info']:
            # We have both now, move to gender step
            birth_time = session['collected_info']['birth_time']
            session['step'] = CollectionStep.COLLECT_GENDER
            
            return f"""✅ **Thông tin thời gian đã được ghi nhận:**
- 📅 Ngày sinh: {birthday}  
- 🕐 Giờ sinh: {birth_time}

⚥ **Bước 3/4: Giới tính**
Cuối cùng, tôi cần biết giới tính của {name} để tính toán vòng Tràng Sinh chính xác.

Vui lòng cho biết giới tính: **Nam** hoặc **Nữ**

*Ví dụ: "Nam", "Nữ", "Giới tính Nam", "Tôi là nữ"*"""
        else:
            return f"""✅ **Ngày sinh đã được ghi nhận: {birthday}**

🕐 **Vẫn cần giờ sinh**
{time_result}

Giờ sinh rất quan trọng để xác định cung Mệnh chính xác. Vui lòng cung cấp thêm giờ sinh.

*Ví dụ: "14:30", "2:30 chiều", "8 giờ sáng"*"""
    
    elif time_confirmed:
        # Only time confirmed  
        import re
        birth_time = re.search(r'Giờ sinh được xác nhận: (.+)', time_result).group(1)
        session['collected_info']['birth_time'] = birth_time
        
        # Check if we already have birthday from previous input
        if 'birthday' in session['collected_info']:
            # We have both now, move to gender step
            birthday = session['collected_info']['birthday'] 
            session['step'] = CollectionStep.COLLECT_GENDER
            
            return f"""✅ **Thông tin thời gian đã được ghi nhận:**
- 📅 Ngày sinh: {birthday}  
- 🕐 Giờ sinh: {birth_time}

⚥ **Bước 3/4: Giới tính**
Cuối cùng, tôi cần biết giới tính của {name} để tính toán vòng Tràng Sinh chính xác.

Vui lòng cho biết giới tính: **Nam** hoặc **Nữ**

*Ví dụ: "Nam", "Nữ", "Giới tính Nam", "Tôi là nữ"*"""
        else:
            return f"""✅ **Giờ sinh đã được ghi nhận: {birth_time}**

📅 **Vẫn cần ngày sinh**
{date_result}

*Ví dụ: "15/03/1990", "ngày 5 tháng 10 năm 1992"*"""
    
    else:
        # Neither confirmed
        return f"""📅 **Bước 2/4: Ngày và giờ sinh**
Chào {name}! Tôi cần thêm thông tin về thời gian sinh:

**Trạng thái hiện tại:**
- {date_result}
- {time_result}

Vui lòng cung cấp cả ngày sinh và giờ sinh:
*Ví dụ: "15/03/1990, 14:30" hoặc "Tôi sinh ngày 5/10/1992, 2:30 chiều"*"""

def process_step_3_gender(message: str, user_id: str = "default") -> str:
    """Step 3: Process gender"""
    session = get_or_create_session(user_id)
    
    gender_result = extract_gender_from_message(message)
    name = session['collected_info'].get('name', 'bạn')
    
    if "được xác nhận" in gender_result:
        import re
        gender = re.search(r'Giới tính được xác nhận: (.+)', gender_result).group(1)
        session['collected_info']['gender'] = gender
        session['step'] = CollectionStep.ANALYSIS
        
        return f"""✅ **Giới tính đã được ghi nhận: {gender}**

🎉 **Thông tin đã đầy đủ! Bắt đầu phân tích...**

**Tóm tắt thông tin của {name}:**
- 📝 Tên: {session['collected_info']['name']}
- 📅 Ngày sinh: {session['collected_info']['birthday']}
- 🕐 Giờ sinh: {session['collected_info']['birth_time']}
- ⚥ Giới tính: {gender}

⏳ *Đang tính toán lá số tử vi...*"""
    else:
        return f"""⚥ **Bước 3/4: Giới tính**
Chào {name}! {gender_result}

*Ví dụ: "Nam", "Nữ", "Giới tính nam", "Tôi là nữ"*"""

def generate_final_tuvi_analysis(user_id: str = "default") -> str:
    """Generate final tuvi analysis with collected information"""
    session = get_or_create_session(user_id)
    info = session['collected_info']
    
    if all(key in info for key in ['name', 'birthday', 'birth_time', 'gender']):
        try:
            chart_data = fn_an_sao_comprehensive(info['birthday'], info['birth_time'], info['gender'])
            
            analysis = f"""🔮 **Phân tích tử vi cho {info['name']}**

✨ **Thông tin cơ bản:**
- 📅 Sinh: {info['birthday']} lúc {info['birth_time']}
- ⚥ Giới tính: {info['gender']}
- 🌟 Thiên Can: {chart_data['basic_info']['thien_can']}
- 🐉 Địa Chi: {chart_data['basic_info']['dia_chi']}
- ⭐ Cục: {chart_data['basic_info']['cuc']}
- 🏠 Cung Mệnh: {chart_data['basic_info']['menh_cung']}

🌌 **Các sao trong 12 cung:**
"""
            for cung, sao_list in chart_data['sao_cung'].items():
                sao_str = ', '.join(sao_list) if sao_list else 'Trống'
                analysis += f"• **{cung}**: {sao_str}\n"
            
            analysis += f"\n💫 **Phân tích hoàn tất!** Lá số của {info['name']} đã được tính toán theo phương pháp tử vi truyền thống.\n\n✨ Bạn có thể hỏi tôi thêm về các khía cạnh cụ thể như: vận mệnh, tình duyên, sự nghiệp, tài lộc, sức khỏe...\n\n💬 *Để bắt đầu phiên tư vấn mới, bạn có thể nói 'Xin chào' hoặc 'Tôi muốn xem tử vi'*"
            
            # Mark as completed
            session['step'] = CollectionStep.COMPLETED
            
            return analysis
        except Exception as e:
            return f"❌ Có lỗi xảy ra khi tính lá số: {str(e)}"
    else:
        return "⚠️ Thiếu thông tin cần thiết để tính lá số tử vi."


def fn_an_sao_comprehensive(birthday: str, birth_time: str, gender: str):
    """Tính lá số tử vi toàn diện với thông tin chi tiết"""
    date_obj = datetime.strptime(birthday, "%d/%m/%Y")
    hour_int = int(birth_time.split(':')[0])

    lunar_date = convert_to_lunar(date_obj.year, date_obj.month, date_obj.day)
    results = an_sao_tuvi_comprehensive(lunar_date.day, lunar_date.month, lunar_date.year, hour_int, gender)

    return results


prompt_template_str = """\
Trích xuất thông tin sinh học từ câu hỏi của người dùng:
Tên, ngày sinh (DD/MM/YYYY), giờ sinh (HH:MM), giới tính (Nam/Nữ)
Nếu thiếu thông tin, hãy yêu cầu bổ sung.

Câu hỏi: {query}
"""

class UserInfo(BaseModel):
    """Data model for user info."""
    name: str
    birthday: str = Field(description="Ngày sinh theo định dạng DD/MM/YYYY")
    birth_time: str = Field(description="Giờ sinh theo định dạng HH:MM")
    gender: str = Field(description="Giới tính: Nam hoặc Nữ")

class ConversationStage(Enum):
    GREETING = "greeting"
    COLLECTING_INFO = "collecting_info" 
    ANALYZING = "analyzing"
    CONSULTING = "consulting"


programInfoUser = FunctionCallingProgram.from_defaults(
    output_cls=UserInfo,
    prompt_template_str=prompt_template_str,
    verbose=True,
)

# [Optional] Add Context
context = """\
Bạn là một thầy tử vi hàng đầu với kiến thức sâu rộng về chiêm tinh học Việt Nam.
Phương pháp luận của bạn:

1. Phân tích căn cơ mệnh chủ qua Mệnh cung và các chính tinh
2. Xét tương quan cục-mệnh (Kim/Mộc/Thủy/Hỏa/Thổ cục với Thiên Can)
3. Luận tam hợp các cung: Mệnh-Tài-Quan, Mệnh-Phúc-Thiên Di
4. Phân tích 4 hóa tinh (Lộc-Quyền-Khoa-Kỵ) và ảnh hưởng
5. Xét vòng Tràng Sinh theo giới tính và cục số
6. Luận đại vận 10 năm và tiểu hạn hàng năm
7. Tổng hợp toàn cục để đưa ra lời khuyên thực tế

Bạn luôn giải thích dựa trên lý thuyết tử vi cổ truyền, tránh mê tín dị đoan.
"""

class CungMenh(Enum):
    MENH = "Mệnh"
    PHU_MAU = "Phụ Mẫu"
    PHUC_DUC = "Phúc Đức"
    DIEN_TRACH = "Điền Trạch"
    QUAN_LOC = "Quan Lộc"
    NO_BOC = "Nô Bộc"
    THIEN_DI = "Thiên Di"
    TAT_ACH = "Tật Ách"
    TAI_BACH = "Tài Bạch"
    TU_TUC = "Tử Tức"
    PHU_THE = "Phu Thê"
    HUYNH_DE = "Huynh Đệ"

class CungAnalysis(BaseModel):
    """Phân tích chi tiết từng cung"""
    cung: CungMenh
    stars: List[str] = Field(description="Các sao trong cung")
    element_harmony: str = Field(description="Tương sinh tương khắc với mệnh chủ")
    strength: str = Field(description="Mạnh/Yếu/Trung bình")
    summary: str = Field(description="Tóm tắt ý nghĩa cung")
    detailed_analysis: str = Field(description="Diễn giải chi tiết vận mệnh theo cung")

class LifePeriodAnalysis(BaseModel):
    """Phân tích đại vận và tiểu hạn"""
    dai_van: str = Field(description="Đại vận hiện tại (10 năm)")
    tieu_han: str = Field(description="Tiểu hạn năm hiện tại")
    fortune_trend: str = Field(description="Xu hướng vận khí: thăng/trầm/ổn định")
    advice: str = Field(description="Lời khuyên cho giai đoạn này")
    
class ComprehensiveTuviReading(BaseModel):
    """Lá số tử vi toàn diện"""
    name: str
    birthday: str = Field(description="Ngày/Tháng/Năm sinh")
    birth_time: str = Field(description="Giờ sinh")
    gender: str = Field(description="Giới tính")
    
    basic_destiny: str = Field(description="Căn cơ mệnh chủ - tính cách tổng quan")
    main_palaces_analysis: List[CungAnalysis] = Field(description="Phân tích 4 cung chính: Mệnh, Tài, Quan, Phu/Thê")
    family_relationships: str = Field(description="Quan hệ gia đình - Phụ Mẫu, Huynh Đệ, Tử Tức")
    health_fortune: str = Field(description="Sức khỏe và vận may - Tật Ách, Phúc Đức")
    career_wealth: str = Field(description="Sự nghiệp và tài chính - Quan Lộc, Tài Bạch, Điền Trạch") 
    current_period: LifePeriodAnalysis = Field(description="Vận hạn hiện tại")
    annual_forecast: str = Field(description="Dự báo năm hiện tại")
    life_guidance: str = Field(description="Hướng dẫn và lời khuyên tổng quan")

def create_and_load_index():
    persist_dir = "./storage/"
    try:
        storage_context = StorageContext.from_defaults(
            persist_dir=persist_dir,
        )
        index = load_index_from_storage(storage_context)
        index_loaded = True
    except:
        index_loaded = False
    
    if not index_loaded:
        docs = SimpleDirectoryReader(
            input_dir="./data_learning/",
        ).load_data()
        index = VectorStoreIndex.from_documents(docs)
        index.storage_context.persist(persist_dir)

    return index

tu_vi_index = create_and_load_index()

llm_4 = OpenAI(model="gpt-4o-mini")

query_engine = tu_vi_index.as_query_engine(
    output_cls=ComprehensiveTuviReading, response_mode="tree_summarize", llm=llm_4
)

# Create FunctionTool instances for ReActAgent
name_extraction_tool = FunctionTool.from_defaults(
    fn=extract_name_from_message,
    name="extract_name",
    description="Extract user name from a message"
)
date_extraction_tool = FunctionTool.from_defaults(
    fn=extract_birth_date_from_message,
    name="extract_birth_date", 
    description="Extract birth date from a message"
)
time_extraction_tool = FunctionTool.from_defaults(
    fn=extract_birth_time_from_message,
    name="extract_birth_time",
    description="Extract birth time from a message"
)
gender_extraction_tool = FunctionTool.from_defaults(
    fn=extract_gender_from_message,
    name="extract_gender",
    description="Extract gender from a message"
)
guidance_tool = FunctionTool.from_defaults(
    fn=provide_guidance_for_missing_info,
    name="provide_guidance",
    description="Provide guidance for missing information"
)
# Legacy analysis tool removed - now using step-by-step approach

# Create FunctionTool instances for step-by-step ReActAgent
step_1_tool = FunctionTool.from_defaults(
    fn=process_step_1_name,
    name="process_step_1_name",
    description="Process Step 1: Collect and validate user name"
)

step_2_tool = FunctionTool.from_defaults(
    fn=process_step_2_birthday_time,
    name="process_step_2_birthday_time",
    description="Process Step 2: Collect birthday and birth time"
)

step_3_tool = FunctionTool.from_defaults(
    fn=process_step_3_gender,
    name="process_step_3_gender", 
    description="Process Step 3: Collect gender information"
)

final_analysis_tool = FunctionTool.from_defaults(
    fn=generate_final_tuvi_analysis,
    name="generate_final_tuvi_analysis",
    description="Generate final tuvi analysis with all collected information"
)

reset_session_tool = FunctionTool.from_defaults(
    fn=lambda user_id="default": reset_session(user_id) or "✨ Phiên tư vấn mới đã được khởi tạo!",
    name="reset_session",
    description="Reset session to start a new consultation"
)

# Step-by-step tools for ReActAgent reasoning
step_tools_dict = {
    'step_1': process_step_1_name,
    'step_2': process_step_2_birthday_time,
    'step_3': process_step_3_gender,
    'final_analysis': generate_final_tuvi_analysis,
    'reset_session': reset_session
}

# Legacy conversation handling functions removed - now using ReActAgent

def prompt_to_predict(questionMessage='', user_id='default'):
    """Entry point for step-by-step progressive tử vi consultation"""
    
    # Get current session
    session = get_or_create_session(user_id)
    current_step = session['step']
    
    # Check for reset/restart commands
    reset_keywords = ['xin chào', 'hello', 'hi', 'chào', 'bắt đầu', 'start', 'reset', 'tư vấn mới', 'xem tử vi']
    if any(keyword in questionMessage.lower() for keyword in reset_keywords) and current_step == CollectionStep.COMPLETED:
        reset_session(user_id)
        session = get_or_create_session(user_id)
        current_step = session['step']
    
    # Progressive step-by-step collection with ReActAgent-style reasoning
    if current_step == CollectionStep.GREETING:
        # Step 1: Collect name
        return process_step_1_name(questionMessage, user_id)
        
    elif current_step == CollectionStep.COLLECT_NAME:
        # Still collecting name
        return process_step_1_name(questionMessage, user_id)
        
    elif current_step == CollectionStep.COLLECT_BIRTHDAY:
        # Step 2: Collect birthday and time
        return process_step_2_birthday_time(questionMessage, user_id)
        
    elif current_step == CollectionStep.COLLECT_BIRTH_TIME:
        # Still collecting birthday/time (fallback)
        return process_step_2_birthday_time(questionMessage, user_id)
        
    elif current_step == CollectionStep.COLLECT_GENDER:
        # Step 3: Collect gender
        return process_step_3_gender(questionMessage, user_id)
        
    elif current_step == CollectionStep.ANALYSIS:
        # Generate final analysis
        analysis_result = generate_final_tuvi_analysis(user_id)
        return analysis_result
        
    elif current_step == CollectionStep.COMPLETED:
        # Handle follow-up questions after analysis is complete
        # This could include detailed questions about specific aspects
        return f"""💫 **Phiên tư vấn đã hoàn tất!**

Lá số tử vi của {session['collected_info'].get('name', 'bạn')} đã được phân tích xong.

✨ **Bạn có thể hỏi tôi về:**
- Vận mệnh và tính cách tổng quan
- Tình duyên và hôn nhân  
- Sự nghiệp và công danh
- Tài lộc và đầu tư
- Sức khỏe và tuổi thọ
- Mối quan hệ gia đình

💬 **Hoặc bắt đầu phiên tư vấn mới:** Nói "Xin chào" hoặc "Tôi muốn xem tử vi"

*Ví dụ câu hỏi: "Vận mệnh của tôi như thế nào?", "Tình duyên ra sao?", "Năm nay tài lộc thế nào?"*"""
    
    else:
        # Default fallback
        reset_session(user_id)
        return """🔮 **Chào mừng bạn đến với dịch vụ tư vấn tử vi!**

📝 **Bước 1/4: Tên của bạn**
Để bắt đầu, vui lòng cho tôi biết tên của bạn.

*Ví dụ: "Tôi tên Nguyễn Văn A" hoặc "Tên tôi là Phan Ngọc"*"""
