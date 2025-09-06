from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI
from lunarcalendar import Converter, Solar
from datetime import datetime

import os
from dotenv import load_dotenv
import chromadb
from llama_index.core import Settings

from llama_index.core.agent import ReActAgent
from llama_index.agent.openai import OpenAIAssistantAgent
from llama_index.core.output_parsers import PydanticOutputParser
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

def create_consultation_session():
    """Tạo session tư vấn tử vi mới"""
    return {
        'stage': ConversationStage.GREETING,
        'user_info': None,
        'chart_data': None,
        'consultation_history': []
    }

def process_user_message(message: str, session: dict):
    """Xử lý tin nhắn người dùng theo từng giai đoạn"""
    
    if session['stage'] == ConversationStage.GREETING:
        return handle_greeting(message, session)
    elif session['stage'] == ConversationStage.COLLECTING_INFO:
        return handle_info_collection(message, session) 
    elif session['stage'] == ConversationStage.ANALYZING:
        return handle_analysis(session)
    elif session['stage'] == ConversationStage.CONSULTING:
        return handle_consultation(message, session)

def handle_greeting(message: str, session: dict):
    """Xử lý lời chào và hướng dẫn thu thập thông tin"""
    session['stage'] = ConversationStage.COLLECTING_INFO
    return """Chào mừng bạn đến với dịch vụ tư vấn tử vi!

Để có thể lập lá số chính xác và tư vấn vận mệnh, tôi cần bạn cung cấp:
1. **Họ tên** của bạn
2. **Ngày sinh** (DD/MM/YYYY) 
3. **Giờ sinh** chính xác (HH:MM) - rất quan trọng cho việc xác định cung Mệnh
4. **Giới tính** (Nam/Nữ) - ảnh hưởng đến cách an sao và luận vận

Ví dụ: "Tôi tên Nguyễn Văn A, sinh ngày 15/03/1990, 14:30, giới tính Nam"

Bạn có thể cung cấp thông tin này không?"""

def handle_info_collection(message: str, session: dict):
    """Thu thập và xác thực thông tin sinh học"""
    try:
        user_info = programInfoUser(query=message)
        
        if not all([user_info.name, user_info.birthday, user_info.birth_time, user_info.gender]):
            missing_fields = []
            if not user_info.name: missing_fields.append("họ tên")
            if not user_info.birthday: missing_fields.append("ngày sinh")
            if not user_info.birth_time: missing_fields.append("giờ sinh")
            if not user_info.gender: missing_fields.append("giới tính")
            
            return f"Tôi cần thêm thông tin: {', '.join(missing_fields)}. Vui lòng cung cấp đầy đủ để có thể lập lá số chính xác."
        
        session['user_info'] = user_info
        session['stage'] = ConversationStage.ANALYZING
        
        return f"""Cảm ơn {user_info.name}! Tôi đã ghi nhận thông tin:
- Ngày sinh: {user_info.birthday}  
- Giờ sinh: {user_info.birth_time}
- Giới tính: {user_info.gender}

Đang tiến hành lập lá số và phân tích vận mệnh... ⏳"""
        
    except Exception as e:
        return "Xin lỗi, tôi chưa hiểu đầy đủ thông tin. Vui lòng cung cấp theo định dạng: Tên, ngày sinh (DD/MM/YYYY), giờ sinh (HH:MM), giới tính (Nam/Nữ)"

def handle_analysis(session: dict):
    """Thực hiện phân tích lá số tử vi"""
    user_info = session['user_info']
    
    chart_data = fn_an_sao_comprehensive(
        user_info.birthday, 
        user_info.birth_time, 
        user_info.gender
    )
    
    session['chart_data'] = chart_data
    session['stage'] = ConversationStage.CONSULTING
    
    query_text = f"""
    Phân tích tử vi cho {user_info.name}:
    - Sinh: {user_info.birthday} lúc {user_info.birth_time}
    - Giới tính: {user_info.gender}
    - Thiên Can: {chart_data['basic_info']['thien_can']}
    - Địa Chi: {chart_data['basic_info']['dia_chi']}
    - Cục: {chart_data['basic_info']['cuc']}
    - Cung Mệnh: {chart_data['basic_info']['menh_cung']}
    
    Các sao trong 12 cung:
    """ + "\n".join([f"Cung {cung}: {', '.join(sao_list) if sao_list else 'Trống'}" 
                    for cung, sao_list in chart_data['sao_cung'].items()])
    
    response = query_engine.query(query_text)
    session['consultation_history'].append(('analysis', str(response)))
    
    return str(response) + "\n\n💬 **Bạn có muốn hỏi thêm về khía cạnh nào khác không?** (sự nghiệp, tình cảm, sức khỏe, tài chính, gia đình...)"

def handle_consultation(message: str, session: dict):
    """Xử lý các câu hỏi tư vấn chi tiết"""
    chart_data = session['chart_data']
    user_info = session['user_info']
    
    context_info = f"""
    Lá số của {user_info.name}:
    Cục {chart_data['basic_info']['cuc']}, Cung Mệnh tại {chart_data['basic_info']['menh_cung']}
    Các sao: {chart_data['sao_cung']}
    
    Câu hỏi: {message}
    """
    
    response = query_engine.query(context_info)
    session['consultation_history'].append(('question', message))
    session['consultation_history'].append(('answer', str(response)))
    
    return str(response)

def prompt_to_predict(questionMessage=''):
    """Entry point chính cho chatbot tử vi"""
    if not hasattr(prompt_to_predict, 'session'):
        prompt_to_predict.session = create_consultation_session()
    
    return process_user_message(questionMessage, prompt_to_predict.session)
