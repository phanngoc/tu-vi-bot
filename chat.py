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
from llama_index.core import Settings
from llama_index.core.tools import FunctionTool
from llama_index.core.agent import ReActAgent
from llama_index.core.memory import ChatMemoryBuffer, ChatSummaryMemoryBuffer
import json
import tiktoken
from models import ChatHistory, UserSession, Session as DBSession

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

# Dynamic conversation states
class ConversationState(Enum):
    GREETING = "greeting"
    COLLECTING_INFO = "collecting_info"  # Dynamic info collection
    ANALYZING = "analyzing"  # When enough info is detected
    CONSULTING = "consulting"  # Post-analysis consultation
    RESET = "reset"  # When user wants to start over

# Database session management
db_session = DBSession()

def get_or_create_session(user_id="default"):
    """Get or create user session from database"""
    session_record = db_session.query(UserSession).filter(UserSession.session_id == user_id).first()
    
    if not session_record:
        # Create new session
        session_record = UserSession(
            session_id=user_id,
            current_step=ConversationState.GREETING.value,
            collected_info=json.dumps({}),
            memory_summary=""
        )
        db_session.add(session_record)
        db_session.commit()
    
    return {
        'state': ConversationState(session_record.current_step),
        'collected_info': json.loads(session_record.collected_info or '{}'),
        'memory_summary': session_record.memory_summary or ""
    }

def update_session(user_id="default", state=None, collected_info=None, memory_summary=None):
    """Update user session in database"""
    session_record = db_session.query(UserSession).filter(UserSession.session_id == user_id).first()
    
    if session_record:
        if state:
            session_record.current_step = state.value if isinstance(state, ConversationState) else state
        if collected_info is not None:
            session_record.collected_info = json.dumps(collected_info)
        if memory_summary is not None:
            session_record.memory_summary = memory_summary
        
        db_session.commit()

def reset_session(user_id="default"):
    """Reset user session in database"""
    session_record = db_session.query(UserSession).filter(UserSession.session_id == user_id).first()
    
    if session_record:
        session_record.current_step = ConversationState.GREETING.value
        session_record.collected_info = json.dumps({})
        session_record.memory_summary = ""
        db_session.commit()
    
    # Also clear chat history for this session
    db_session.query(ChatHistory).filter(ChatHistory.user_id == user_id).delete()
    db_session.commit()

def save_chat_message(user_id="default", message="", role="user", state=None, extracted_info=None):
    """Save chat message to database"""
    chat_record = ChatHistory(
        user_id=user_id,
        message=message,
        role=role,
        step=state.value if isinstance(state, ConversationState) else state,
        extracted_info=json.dumps(extracted_info) if extracted_info else None
    )
    db_session.add(chat_record)
    db_session.commit()

def get_chat_history(user_id="default", limit=50):
    """Get chat history from database"""
    history = db_session.query(ChatHistory).filter(
        ChatHistory.user_id == user_id
    ).order_by(ChatHistory.created_at.desc()).limit(limit).all()
    
    return [{
        'message': h.message,
        'role': h.role,
        'step': h.step,
        'extracted_info': json.loads(h.extracted_info) if h.extracted_info else None,
        'created_at': h.created_at
    } for h in reversed(history)]

def create_memory_buffer(user_id="default"):
    """Create ChatSummaryMemoryBuffer for user session"""
    # Get chat history from database
    chat_history = get_chat_history(user_id)
    
    # Convert to ChatMessage format
    from llama_index.core.llms import ChatMessage, MessageRole
    messages = []
    for chat in chat_history:
        role = MessageRole.USER if chat['role'] == 'user' else MessageRole.ASSISTANT
        messages.append(ChatMessage(role=role, content=chat['message']))
    
    # Create memory buffer with summarization
    tokenizer_fn = tiktoken.encoding_for_model(MODEL_NAME).encode
    memory = ChatSummaryMemoryBuffer.from_defaults(
        chat_history=messages,
        llm=llm,
        token_limit=2000,  # Limit token để tối ưu
        tokenizer_fn=tokenizer_fn,
    )
    
    return memory

# Intelligent conversation management functions

def get_conversation_context(user_id="default", limit=10):
    """Get recent conversation context for LLM analysis"""
    history = get_chat_history(user_id, limit)
    context = []
    for chat in history:
        context.append(f"{chat['role']}: {chat['message']}")
    return "\n".join(context)

def analyze_conversation_intelligence(message: str, user_id: str = "default"):
    """Use LLM to analyze conversation and determine next action"""
    session = get_or_create_session(user_id)
    context = get_conversation_context(user_id)
    
    try:
        analysis = conversation_analysis_program(
            message=message,
            current_state=session['state'].value,
            collected_info=json.dumps(session['collected_info']),
            context=context
        )
        return analysis
    except Exception as e:
        # Fallback to basic analysis
        return ConversationAnalysis(
            current_state=session['state'].value,
            user_intent="unknown",
            information_status=InfoCompletenessCheck(
                has_name=bool(session['collected_info'].get('name')),
                has_birthday=bool(session['collected_info'].get('birthday')),
                has_birth_time=bool(session['collected_info'].get('birth_time')),
                has_gender=bool(session['collected_info'].get('gender')),
                is_complete=False,
                missing_fields=[],
                confidence="thấp"
            ),
            suggested_response="Xin lỗi, tôi gặp khó khăn trong việc hiểu tin nhắn của bạn. Bạn có thể nói rõ hơn không?",
            should_extract_info=True,
            should_analyze=False,
            conversation_tone="friendly"
        )

def extract_information_intelligently(message: str, user_id: str = "default"):
    """Use LLM to intelligently extract information from conversation context"""
    context = get_conversation_context(user_id)
    
    try:
        extraction = smart_info_extraction_program(
            message=message,
            context=context
        )
        return extraction
    except Exception as e:
        # Fallback to individual extraction functions
        name_result = extract_name_from_message(message)
        date_result = extract_birth_date_from_message(message)
        time_result = extract_birth_time_from_message(message)
        gender_result = extract_gender_from_message(message)
        
        return SmartInfoExtraction(
            extracted_name=name_result.split(": ")[1] if "được xác nhận" in name_result else "",
            extracted_birthday=date_result.split(": ")[1] if "được xác nhận" in date_result else "",
            extracted_birth_time=time_result.split(": ")[1] if "được xác nhận" in time_result else "",
            extracted_gender=gender_result.split(": ")[1] if "được xác nhận" in gender_result else "",
            is_name_valid="được xác nhận" in name_result,
            is_birthday_valid="được xác nhận" in date_result,
            is_birth_time_valid="được xác nhận" in time_result,
            is_gender_valid="được xác nhận" in gender_result,
            overall_confidence="trung bình",
            should_proceed_to_analysis=False
        )

def update_collected_info_from_extraction(extraction, user_id: str = "default"):
    """Update collected info based on intelligent extraction"""
    session = get_or_create_session(user_id)
    collected_info = session['collected_info'].copy()
    
    if extraction.is_name_valid and extraction.extracted_name:
        collected_info['name'] = extraction.extracted_name
    
    if extraction.is_birthday_valid and extraction.extracted_birthday:
        collected_info['birthday'] = extraction.extracted_birthday
    
    if extraction.is_birth_time_valid and extraction.extracted_birth_time:
        collected_info['birth_time'] = extraction.extracted_birth_time
    
    if extraction.is_gender_valid and extraction.extracted_gender:
        collected_info['gender'] = extraction.extracted_gender
    
    # Update session
    update_session(user_id, collected_info=collected_info)
    
    return collected_info

def check_info_completeness(collected_info: dict):
    """Check if we have enough information for analysis"""
    required_fields = ['name', 'birthday', 'birth_time', 'gender']
    has_fields = {
        'name': bool(collected_info.get('name')),
        'birthday': bool(collected_info.get('birthday')),
        'birth_time': bool(collected_info.get('birth_time')),
        'gender': bool(collected_info.get('gender'))
    }
    
    missing_fields = [field for field in required_fields if not has_fields[field]]
    is_complete = len(missing_fields) == 0
    
    return InfoCompletenessCheck(
        has_name=has_fields['name'],
        has_birthday=has_fields['birthday'],
        has_birth_time=has_fields['birth_time'],
        has_gender=has_fields['gender'],
        is_complete=is_complete,
        missing_fields=missing_fields,
        confidence="cao" if is_complete else "trung bình"
    )

def generate_smart_response(analysis, user_id: str = "default") -> str:
    """Generate intelligent response based on conversation analysis"""
    session = get_or_create_session(user_id)
    
    # If LLM provided a suggested response, use it
    if analysis.suggested_response and len(analysis.suggested_response) > 10:
        return analysis.suggested_response
    
    # Generate response based on analysis
    if analysis.user_intent == "greeting":
        return """🔮 **Chào mừng bạn đến với dịch vụ tư vấn tử vi thông minh!**

Tôi là trợ lý AI chuyên về tử vi, có thể giúp bạn:
- Phân tích lá số tử vi chi tiết
- Tư vấn về vận mệnh, tình duyên, sự nghiệp
- Dự báo vận hạn và đưa ra lời khuyên

Để bắt đầu, tôi cần biết một số thông tin cơ bản về bạn. Bạn có thể chia sẻ tên, ngày sinh, giờ sinh và giới tính của mình không?

*Ví dụ: "Tôi tên Nguyễn Văn A, sinh ngày 15/03/1990, 14:30, giới tính Nam"*"""
    
    elif analysis.user_intent == "providing_info":
        if analysis.information_status.is_complete:
            return "✅ **Tuyệt vời! Tôi đã có đủ thông tin để tiến hành phân tích tử vi cho bạn.**"
        else:
            missing_text = {
                'name': 'tên',
                'birthday': 'ngày sinh', 
                'birth_time': 'giờ sinh',
                'gender': 'giới tính'
            }
            missing_list = [missing_text[field] for field in analysis.information_status.missing_fields]
            return f"""📝 **Cảm ơn bạn đã cung cấp thông tin!**

Tôi vẫn cần thêm: **{', '.join(missing_list)}**

Bạn có thể cung cấp thông tin còn thiếu để tôi có thể tiến hành phân tích tử vi chính xác."""
    
    elif analysis.user_intent == "asking_question":
        if session['state'] == ConversationState.CONSULTING:
            return "Tôi sẽ trả lời câu hỏi của bạn dựa trên lá số tử vi đã phân tích."
        else:
            return "Tôi sẽ trả lời câu hỏi của bạn sau khi hoàn thành phân tích tử vi. Trước tiên, tôi cần thu thập đủ thông tin cơ bản."
    
    elif analysis.user_intent == "reset":
        return "🔄 **Đã khởi tạo lại phiên tư vấn!** Bạn có thể bắt đầu lại từ đầu."
    
    else:
        return "Tôi hiểu bạn muốn tư vấn tử vi. Hãy chia sẻ thông tin cơ bản về bạn để tôi có thể giúp đỡ tốt nhất."

# Legacy functions removed - using intelligent conversation flow instead

# Legacy step-by-step functions removed - using intelligent conversation flow instead

# Keep individual extraction functions for fallback
def extract_name_from_message(message: str) -> str:
    """Extract name from message using FunctionCallingProgram"""
    try:
        result = name_extraction_program(message=message)
        if result.is_valid and result.confidence in ['cao', 'trung bình']:
            return f"Tên được xác nhận: {result.name}"
        else:
            return "Chưa thể xác định tên. Vui lòng cung cấp tên của bạn rõ ràng."
    except Exception as e:
        return "Chưa thể xác định tên. Vui lòng cung cấp tên của bạn rõ ràng."

def extract_birth_date_from_message(message: str) -> str:
    """Extract birth date from message using FunctionCallingProgram"""
    try:
        result = date_extraction_program(message=message)
        if result.is_valid:
            # Validate date using datetime
            try:
                datetime.strptime(result.date, "%d/%m/%Y")
                return f"Ngày sinh được xác nhận: {result.date}"
            except:
                return "Ngày sinh không hợp lệ. Vui lòng cung cấp theo định dạng DD/MM/YYYY."
        else:
            return "Chưa thể xác định ngày sinh. Vui lòng cung cấp theo định dạng DD/MM/YYYY."
    except Exception as e:
        return "Chưa thể xác định ngày sinh. Vui lòng cung cấp theo định dạng DD/MM/YYYY."

def extract_birth_time_from_message(message: str) -> str:
    """Extract birth time from message using FunctionCallingProgram"""
    try:
        result = time_extraction_program(message=message)
        if result.is_valid:
            # Additional validation
            if 0 <= result.hour <= 23 and 0 <= result.minute <= 59:
                return f"Giờ sinh được xác nhận: {result.time}"
            else:
                return "Giờ sinh không hợp lệ. Vui lòng cung cấp giờ từ 00:00 đến 23:59."
        else:
            return "Chưa thể xác định giờ sinh. Vui lòng cung cấp theo định dạng HH:MM."
    except Exception as e:
        return "Chưa thể xác định giờ sinh. Vui lòng cung cấp theo định dạng HH:MM."

def extract_gender_from_message(message: str) -> str:
    """Extract gender from message using FunctionCallingProgram"""
    try:
        result = gender_extraction_program(message=message)
        if result.is_valid and result.gender in ['Nam', 'Nữ']:
            return f"Giới tính được xác nhận: {result.gender}"
        else:
            return "Chưa thể xác định giới tính. Vui lòng chọn Nam hoặc Nữ."
    except Exception as e:
        return "Chưa thể xác định giới tính. Vui lòng chọn Nam hoặc Nữ."


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

# Create FunctionCallingPrograms for structured extraction
class NameExtraction(BaseModel):
    """Data model for name extraction."""
    name: str = Field(description="Tên người dùng được trích xuất từ tin nhắn")
    is_valid: bool = Field(description="Tên có hợp lệ không (ít nhất 2 ký tự, không chứa số)")
    confidence: str = Field(description="Mức độ tin cậy: cao/trung bình/thấp")

class DateExtraction(BaseModel):
    """Data model for birth date extraction."""
    date: str = Field(description="Ngày sinh theo định dạng DD/MM/YYYY")
    is_valid: bool = Field(description="Ngày sinh có hợp lệ không")
    day: int = Field(description="Ngày")
    month: int = Field(description="Tháng") 
    year: int = Field(description="Năm")

class TimeExtraction(BaseModel):
    """Data model for birth time extraction."""
    time: str = Field(description="Giờ sinh theo định dạng HH:MM")
    is_valid: bool = Field(description="Giờ sinh có hợp lệ không")
    hour: int = Field(description="Giờ (0-23)")
    minute: int = Field(description="Phút (0-59)")

class GenderExtraction(BaseModel):
    """Data model for gender extraction."""
    gender: str = Field(description="Giới tính: Nam hoặc Nữ")
    is_valid: bool = Field(description="Giới tính có hợp lệ không")
    confidence: str = Field(description="Mức độ tin cậy: cao/trung bình/thấp")

class InfoCompletenessCheck(BaseModel):
    """Data model for checking if enough information is collected."""
    has_name: bool = Field(description="Có tên chưa")
    has_birthday: bool = Field(description="Có ngày sinh chưa")
    has_birth_time: bool = Field(description="Có giờ sinh chưa")
    has_gender: bool = Field(description="Có giới tính chưa")
    is_complete: bool = Field(description="Đã đủ thông tin để phân tích chưa")
    missing_fields: List[str] = Field(description="Danh sách thông tin còn thiếu")
    confidence: str = Field(description="Mức độ tin cậy: cao/trung bình/thấp")

class SmartInfoExtraction(BaseModel):
    """Data model for intelligent information extraction from conversation context."""
    extracted_name: str = Field(description="Tên được trích xuất", default="")
    extracted_birthday: str = Field(description="Ngày sinh được trích xuất (DD/MM/YYYY)", default="")
    extracted_birth_time: str = Field(description="Giờ sinh được trích xuất (HH:MM)", default="")
    extracted_gender: str = Field(description="Giới tính được trích xuất (Nam/Nữ)", default="")
    is_name_valid: bool = Field(description="Tên có hợp lệ không")
    is_birthday_valid: bool = Field(description="Ngày sinh có hợp lệ không")
    is_birth_time_valid: bool = Field(description="Giờ sinh có hợp lệ không")
    is_gender_valid: bool = Field(description="Giới tính có hợp lệ không")
    overall_confidence: str = Field(description="Mức độ tin cậy tổng thể: cao/trung bình/thấp")
    should_proceed_to_analysis: bool = Field(description="Có nên tiến hành phân tích không")

class ConversationAnalysis(BaseModel):
    """Data model for analyzing conversation context and determining next action."""
    current_state: str = Field(description="Trạng thái hiện tại của cuộc hội thoại")
    user_intent: str = Field(description="Ý định của người dùng")
    information_status: InfoCompletenessCheck = Field(description="Trạng thái thông tin")
    suggested_response: str = Field(description="Phản hồi gợi ý")
    should_extract_info: bool = Field(description="Có nên trích xuất thông tin không")
    should_analyze: bool = Field(description="Có nên tiến hành phân tích không")
    conversation_tone: str = Field(description="Tone của cuộc hội thoại: friendly/professional/urgent")

# FunctionCallingPrograms
name_extraction_program = FunctionCallingProgram.from_defaults(
    output_cls=NameExtraction,
    prompt_template_str="Từ tin nhắn '{message}', hãy trích xuất tên người dùng. Chỉ lấy phần tên thực sự, bỏ qua các từ như 'tôi tên', 'tên tôi là'. Tên phải có ít nhất 2 ký tự và không chứa số. Đánh giá độ tin cậy: cao (rất chắc chắn), trung bình (khá chắc), thấp (không chắc).",
    verbose=False,
    llm=llm
)

date_extraction_program = FunctionCallingProgram.from_defaults(
    output_cls=DateExtraction,
    prompt_template_str="Từ tin nhắn '{message}', hãy trích xuất ngày sinh. Tìm định dạng DD/MM/YYYY. Trả về date dưới dạng DD/MM/YYYY, và phân tách day, month, year thành các số riêng.",
    verbose=False,
    llm=llm
)

time_extraction_program = FunctionCallingProgram.from_defaults(
    output_cls=TimeExtraction,
    prompt_template_str="Từ tin nhắn '{message}', hãy trích xuất giờ sinh. Tìm định dạng HH:MM hoặc các biểu thức thời gian. Trả về time dưới dạng HH:MM (24h), và phân tách hour (0-23), minute (0-59).",
    verbose=False,
    llm=llm
)

gender_extraction_program = FunctionCallingProgram.from_defaults(
    output_cls=GenderExtraction,
    prompt_template_str="Từ tin nhắn '{message}', hãy xác định giới tính. Tìm các từ khóa về giới tính. Chỉ trả về 'Nam' hoặc 'Nữ' trong trường gender. Đánh giá độ tin cậy: cao/trung bình/thấp.",
    verbose=False,
    llm=llm
)

# Smart LLM-based programs for intelligent conversation
smart_info_extraction_program = FunctionCallingProgram.from_defaults(
    output_cls=SmartInfoExtraction,
    prompt_template_str="""Từ cuộc hội thoại sau, hãy trích xuất thông tin một cách thông minh:

Tin nhắn hiện tại: '{message}'
Lịch sử cuộc hội thoại: {context}

Hãy phân tích và trích xuất:
1. Tên người dùng (nếu có)
2. Ngày sinh (định dạng DD/MM/YYYY)
3. Giờ sinh (định dạng HH:MM)
4. Giới tính (Nam hoặc Nữ)

Đánh giá tính hợp lệ và mức độ tin cậy. Nếu đã có đủ 4 thông tin hợp lệ, đặt should_proceed_to_analysis = true.""",
    verbose=False,
    llm=llm
)

conversation_analysis_program = FunctionCallingProgram.from_defaults(
    output_cls=ConversationAnalysis,
    prompt_template_str="""Phân tích cuộc hội thoại và đưa ra quyết định thông minh:

Tin nhắn hiện tại: '{message}'
Trạng thái hiện tại: {current_state}
Thông tin đã thu thập: {collected_info}
Lịch sử cuộc hội thoại: {context}

Hãy phân tích:
1. Ý định của người dùng (greeting, providing_info, asking_question, reset, etc.)
2. Trạng thái thông tin hiện tại
3. Phản hồi phù hợp nhất
4. Có nên trích xuất thông tin không
5. Có nên tiến hành phân tích không
6. Tone phù hợp (friendly/professional/urgent)

Hãy hoạt động như một consultant tử vi thông minh, tự nhiên và hữu ích.""",
    verbose=False,
    llm=llm
)
# Legacy ReActAgent tools removed - using intelligent conversation flow instead

def intelligent_conversation_flow(message: str, user_id: str = "default") -> str:
    """Main intelligent conversation flow using LLM-based analysis"""
    
    # Save user message
    save_chat_message(user_id, message, "user", ConversationState.COLLECTING_INFO)
    
    # Analyze conversation intelligently
    analysis = analyze_conversation_intelligence(message, user_id)
    
    # Handle reset requests
    if analysis.user_intent == "reset":
        reset_session(user_id)
        response = generate_smart_response(analysis, user_id)
        save_chat_message(user_id, response, "assistant", ConversationState.GREETING)
        return response
    
    # Handle consulting questions first if we're in consulting state
    if analysis.user_intent == "asking_question":
        session = get_or_create_session(user_id)
        if session['state'] == ConversationState.CONSULTING:
            return handle_consulting_question(message, user_id)
    
    # Always try to extract information first
    extraction = extract_information_intelligently(message, user_id)
    collected_info = update_collected_info_from_extraction(extraction, user_id)
    
    # Check if we have enough information
    completeness = check_info_completeness(collected_info)
    
    if completeness.is_complete:
        # Proceed to analysis
        return perform_tuvi_analysis(user_id)
    elif analysis.should_extract_info:
        # Generate response asking for more info
        response = generate_smart_response(analysis, user_id)
        save_chat_message(user_id, response, "assistant", ConversationState.COLLECTING_INFO)
        return response
    
    # Handle consulting questions
    elif analysis.user_intent == "asking_question":
        session = get_or_create_session(user_id)
        # Check if we have enough info first
        completeness = check_info_completeness(session['collected_info'])
        
        if completeness.is_complete:
            # If we have enough info but not in consulting state, do analysis first
            if session['state'] != ConversationState.CONSULTING:
                return perform_tuvi_analysis(user_id)
            else:
                return handle_consulting_question(message, user_id)
        else:
            response = "Tôi sẽ trả lời câu hỏi của bạn sau khi hoàn thành phân tích tử vi. Trước tiên, tôi cần thu thập đủ thông tin cơ bản."
            save_chat_message(user_id, response, "assistant", ConversationState.COLLECTING_INFO)
            return response
    
    # Default response - check if we have enough info
    session = get_or_create_session(user_id)
    completeness = check_info_completeness(session['collected_info'])
    
    if completeness.is_complete and session['state'] != ConversationState.CONSULTING:
        # If we have enough info but not in consulting state, do analysis
        return perform_tuvi_analysis(user_id)
    elif session['state'] == ConversationState.CONSULTING:
        # Handle consulting questions
        return handle_consulting_question(message, user_id)
    else:
        # Generate normal response
        response = generate_smart_response(analysis, user_id)
        save_chat_message(user_id, response, "assistant", ConversationState.COLLECTING_INFO)
        return response

def perform_tuvi_analysis(user_id: str = "default") -> str:
    """Perform tuvi analysis when enough information is collected"""
    session = get_or_create_session(user_id)
    collected_info = session['collected_info']
    
    try:
        # Generate tuvi analysis
        chart_data = fn_an_sao_comprehensive(
            collected_info['birthday'], 
            collected_info['birth_time'], 
            collected_info['gender']
        )
        
        analysis = f"""🔮 **Phân tích tử vi cho {collected_info['name']}**

✨ **Thông tin cơ bản:**
- 📅 Sinh: {collected_info['birthday']} lúc {collected_info['birth_time']}
- ⚥ Giới tính: {collected_info['gender']}
- 🌟 Thiên Can: {chart_data['basic_info']['thien_can']}
- 🐉 Địa Chi: {chart_data['basic_info']['dia_chi']}
- ⭐ Cục: {chart_data['basic_info']['cuc']}
- 🏠 Cung Mệnh: {chart_data['basic_info']['menh_cung']}

🌌 **Các sao trong 12 cung:**
"""
        for cung, sao_list in chart_data['sao_cung'].items():
            sao_str = ', '.join(sao_list) if sao_list else 'Trống'
            analysis += f"• **{cung}**: {sao_str}\n"
        
        analysis += f"""

💫 **Phân tích hoàn tất!** Lá số của {collected_info['name']} đã được tính toán theo phương pháp tử vi truyền thống.

✨ **Bạn có thể hỏi tôi về:**
- Vận mệnh và tính cách tổng quan
- Tình duyên và hôn nhân  
- Sự nghiệp và công danh
- Tài lộc và đầu tư
- Sức khỏe và tuổi thọ
- Mối quan hệ gia đình

💬 *Để bắt đầu phiên tư vấn mới, bạn có thể nói 'Xin chào' hoặc 'Tôi muốn xem tử vi'*"""
        
        # Update session to consulting state
        update_session(user_id, state=ConversationState.CONSULTING)
        
        # Save analysis to chat history
        save_chat_message(user_id, analysis, "assistant", ConversationState.CONSULTING)
        
        return analysis
    except Exception as e:
        error_msg = f"❌ Có lỗi xảy ra khi tính lá số: {str(e)}"
        save_chat_message(user_id, error_msg, "assistant", ConversationState.COLLECTING_INFO)
        return error_msg

def handle_consulting_question(message: str, user_id: str = "default") -> str:
    """Handle follow-up questions after analysis is complete"""
    # Save user question
    save_chat_message(user_id, message, "user", ConversationState.CONSULTING)
    
    # Generate context-aware response using the tuvi query engine
    try:
        # Use the existing query engine for detailed questions
        response = query_engine.query(message)
        
        # Save assistant response
        save_chat_message(user_id, str(response), "assistant", ConversationState.CONSULTING)
        
        return str(response)
    except Exception as e:
        error_response = f"❌ Có lỗi xảy ra khi xử lý câu hỏi: {str(e)}"
        save_chat_message(user_id, error_response, "assistant", ConversationState.CONSULTING)
        return error_response

def prompt_to_predict(questionMessage='', user_id='default'):
    """Entry point for intelligent conversation flow"""
    return intelligent_conversation_flow(questionMessage, user_id)
