"""
Interface definitions for Tu Vi Bot components.

Các interface này đảm bảo tính plug-in và dễ dàng thay thế component.
Tuân theo nguyên tắc "Keep it simple" - mỗi interface chỉ định nghĩa những method cần thiết.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass


class ConversationState(Enum):
    """Trạng thái cuộc hội thoại"""
    GREETING = "greeting"
    COLLECTING_INFO = "collecting_info"
    ANALYZING = "analyzing"
    CONSULTING = "consulting"
    RESET = "reset"


@dataclass
class UserInfo:
    """Thông tin người dùng"""
    name: str = ""
    birthday: str = ""
    birth_time: str = ""
    gender: str = ""


@dataclass
class TuviResult:
    """Kết quả tính toán tử vi"""
    basic_info: Dict[str, Any]
    sao_cung: Dict[str, List[str]]
    fortune: Dict[str, Any]
    analysis: Dict[str, Any]
    guidance: Dict[str, Any]


@dataclass
class ConversationContext:
    """Ngữ cảnh cuộc hội thoại"""
    user_id: str
    state: ConversationState
    collected_info: UserInfo
    message_history: List[Dict[str, str]]


class ITuviCalculator(ABC):
    """Interface cho engine tính toán tử vi"""
    
    @abstractmethod
    def calculate_tuvi(self, user_info: UserInfo) -> TuviResult:
        """Tính toán lá số tử vi từ thông tin người dùng"""
        pass
    
    @abstractmethod
    def get_star_strength(self, star_name: str, chi_position: str) -> str:
        """Lấy độ mạnh của sao tại vị trí địa chi"""
        pass


class IConversationManager(ABC):
    """Interface cho quản lý hội thoại thông minh"""
    
    @abstractmethod
    def process_message(self, message: str, user_id: str) -> str:
        """Xử lý tin nhắn và trả về phản hồi"""
        pass
    
    @abstractmethod
    def get_conversation_context(self, user_id: str) -> ConversationContext:
        """Lấy ngữ cảnh cuộc hội thoại"""
        pass
    
    @abstractmethod
    def reset_conversation(self, user_id: str) -> None:
        """Reset cuộc hội thoại"""
        pass


class IDatabaseManager(ABC):
    """Interface cho quản lý database"""
    
    @abstractmethod
    def save_user_session(self, user_id: str, context: ConversationContext) -> None:
        """Lưu session người dùng"""
        pass
    
    @abstractmethod
    def get_user_session(self, user_id: str) -> Optional[ConversationContext]:
        """Lấy session người dùng"""
        pass
    
    @abstractmethod
    def save_chat_message(self, user_id: str, message: str, role: str) -> None:
        """Lưu tin nhắn chat"""
        pass
    
    @abstractmethod
    def get_chat_history(self, user_id: str, limit: int = 50) -> List[Dict[str, str]]:
        """Lấy lịch sử chat"""
        pass


class IInformationExtractor(ABC):
    """Interface cho trích xuất thông tin từ tin nhắn"""
    
    @abstractmethod
    def extract_user_info(self, message: str, context: ConversationContext) -> UserInfo:
        """Trích xuất thông tin người dùng từ tin nhắn"""
        pass
    
    @abstractmethod
    def is_info_complete(self, user_info: UserInfo) -> bool:
        """Kiểm tra xem đã có đủ thông tin chưa"""
        pass
    
    @abstractmethod
    def get_missing_fields(self, user_info: UserInfo) -> List[str]:
        """Lấy danh sách thông tin còn thiếu"""
        pass


class IResponseGenerator(ABC):
    """Interface cho tạo phản hồi"""
    
    @abstractmethod
    def generate_greeting_response(self) -> str:
        """Tạo phản hồi chào hỏi"""
        pass
    
    @abstractmethod
    def generate_info_request_response(self, missing_fields: List[str]) -> str:
        """Tạo phản hồi yêu cầu thông tin"""
        pass
    
    @abstractmethod
    def generate_tuvi_analysis_response(self, user_info: UserInfo, tuvi_result: TuviResult) -> str:
        """Tạo phản hồi phân tích tử vi"""
        pass
    
    @abstractmethod
    def generate_consulting_response(self, question: str, user_info: UserInfo, tuvi_result: TuviResult) -> str:
        """Tạo phản hồi tư vấn"""
        pass


class ILLMProvider(ABC):
    """Interface cho LLM provider"""
    
    @abstractmethod
    def analyze_conversation(self, message: str, context: ConversationContext) -> Dict[str, Any]:
        """Phân tích cuộc hội thoại bằng LLM"""
        pass
    
    @abstractmethod
    def extract_information(self, message: str, context: ConversationContext) -> UserInfo:
        """Trích xuất thông tin bằng LLM"""
        pass
    
    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """Tạo phản hồi bằng LLM"""
        pass
