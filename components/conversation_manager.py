"""
Conversation Manager Component

Component quản lý hội thoại thông minh, điều phối các component khác.
"""

from typing import Optional
from .interfaces import (
    IConversationManager, ConversationContext, ConversationState, 
    UserInfo, TuviResult
)
from .database_manager import DatabaseManager
from .information_extractor import InformationExtractor
from .response_generator import ResponseGenerator
from .tuvi_calculator import TuviCalculator
from .llm_provider import LLMProvider


class ConversationManager(IConversationManager):
    """Quản lý hội thoại thông minh"""
    
    def __init__(self, 
                 database_manager: DatabaseManager = None,
                 information_extractor: InformationExtractor = None,
                 response_generator: ResponseGenerator = None,
                 tuvi_calculator: TuviCalculator = None,
                 llm_provider: LLMProvider = None):
        
        # Initialize components with dependency injection
        self.db_manager = database_manager or DatabaseManager()
        self.llm_provider = llm_provider or LLMProvider()
        self.info_extractor = information_extractor or InformationExtractor(self.llm_provider)
        self.response_generator = response_generator or ResponseGenerator()
        self.tuvi_calculator = tuvi_calculator or TuviCalculator()
    
    def process_message(self, message: str, user_id: str) -> str:
        """Xử lý tin nhắn và trả về phản hồi"""
        # Lưu tin nhắn người dùng
        self.db_manager.save_chat_message(user_id, message, "user")
        
        # Lấy ngữ cảnh cuộc hội thoại
        context = self.get_conversation_context(user_id)
        
        # Xử lý reset request
        if self._is_reset_request(message):
            self.reset_conversation(user_id)
            response = "🔄 **Đã khởi tạo lại phiên tư vấn!** Bạn có thể bắt đầu lại từ đầu."
            self.db_manager.save_chat_message(user_id, response, "assistant")
            return response
        
        # Trích xuất thông tin từ tin nhắn
        updated_user_info = self.info_extractor.extract_user_info(message, context)
        
        # Cập nhật ngữ cảnh với thông tin mới
        context.collected_info = updated_user_info
        
        # Kiểm tra xem đã có đủ thông tin chưa
        if self.info_extractor.is_info_complete(updated_user_info):
            # Đủ thông tin, tiến hành phân tích tử vi
            return self._perform_tuvi_analysis(user_id, updated_user_info)
        else:
            # Chưa đủ thông tin, yêu cầu bổ sung
            missing_fields = self.info_extractor.get_missing_fields(updated_user_info)
            response = self.response_generator.generate_info_request_response(missing_fields)
            
            # Cập nhật session
            context.state = ConversationState.COLLECTING_INFO
            self.db_manager.save_user_session(user_id, context)
            self.db_manager.save_chat_message(user_id, response, "assistant")
            
            return response
    
    def get_conversation_context(self, user_id: str) -> ConversationContext:
        """Lấy ngữ cảnh cuộc hội thoại"""
        context = self.db_manager.get_user_session(user_id)
        
        if not context:
            # Tạo context mới
            context = ConversationContext(
                user_id=user_id,
                state=ConversationState.GREETING,
                collected_info=UserInfo(),
                message_history=[]
            )
            self.db_manager.save_user_session(user_id, context)
        
        return context
    
    def reset_conversation(self, user_id: str) -> None:
        """Reset cuộc hội thoại"""
        self.db_manager.reset_user_session(user_id)
    
    def _is_reset_request(self, message: str) -> bool:
        """Kiểm tra xem có phải yêu cầu reset không"""
        reset_keywords = ['reset', 'bắt đầu lại', 'mới', 'khởi tạo lại', 'xin chào']
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in reset_keywords)
    
    def _perform_tuvi_analysis(self, user_id: str, user_info: UserInfo) -> str:
        """Thực hiện phân tích tử vi"""
        try:
            # Tính toán lá số tử vi
            tuvi_result = self.tuvi_calculator.calculate_tuvi(user_info)
            
            # Tạo phản hồi phân tích
            response = self.response_generator.generate_tuvi_analysis_response(user_info, tuvi_result)
            
            # Cập nhật session sang trạng thái consulting
            context = self.get_conversation_context(user_id)
            context.state = ConversationState.CONSULTING
            self.db_manager.save_user_session(user_id, context)
            self.db_manager.save_chat_message(user_id, response, "assistant")
            
            return response
            
        except Exception as e:
            error_response = f"❌ Có lỗi xảy ra khi tính lá số: {str(e)}"
            self.db_manager.save_chat_message(user_id, error_response, "assistant")
            return error_response
    
    def handle_consulting_question(self, message: str, user_id: str) -> str:
        """Xử lý câu hỏi tư vấn sau khi đã phân tích"""
        # Lưu câu hỏi
        self.db_manager.save_chat_message(user_id, message, "user")
        
        # Lấy ngữ cảnh
        context = self.get_conversation_context(user_id)
        
        if not self.info_extractor.is_info_complete(context.collected_info):
            response = "Tôi sẽ trả lời câu hỏi của bạn sau khi hoàn thành phân tích tử vi. Trước tiên, tôi cần thu thập đủ thông tin cơ bản."
            self.db_manager.save_chat_message(user_id, response, "assistant")
            return response
        
        try:
            # Tính lại lá số tử vi (có thể cache để tối ưu)
            tuvi_result = self.tuvi_calculator.calculate_tuvi(context.collected_info)
            
            # Tạo phản hồi tư vấn
            response = self.response_generator.generate_consulting_response(
                message, context.collected_info, tuvi_result
            )
            
            self.db_manager.save_chat_message(user_id, response, "assistant")
            return response
            
        except Exception as e:
            error_response = f"❌ Có lỗi xảy ra khi xử lý câu hỏi: {str(e)}"
            self.db_manager.save_chat_message(user_id, error_response, "assistant")
            return error_response


class IntelligentConversationManager(ConversationManager):
    """Conversation Manager sử dụng LLM để phân tích thông minh"""
    
    def process_message(self, message: str, user_id: str) -> str:
        """Xử lý tin nhắn với phân tích LLM thông minh"""
        # Lưu tin nhắn người dùng
        self.db_manager.save_chat_message(user_id, message, "user")
        
        # Lấy ngữ cảnh
        context = self.get_conversation_context(user_id)
        
        # Phân tích cuộc hội thoại bằng LLM
        analysis = self.llm_provider.analyze_conversation(message, context)
        
        # Xử lý theo ý định được phân tích
        if analysis['user_intent'] == 'reset':
            self.reset_conversation(user_id)
            response = "🔄 **Đã khởi tạo lại phiên tư vấn!** Bạn có thể bắt đầu lại từ đầu."
            self.db_manager.save_chat_message(user_id, response, "assistant")
            return response
        
        elif analysis['user_intent'] == 'greeting':
            response = self.response_generator.generate_greeting_response()
            context.state = ConversationState.COLLECTING_INFO
            self.db_manager.save_user_session(user_id, context)
            self.db_manager.save_chat_message(user_id, response, "assistant")
            return response
        
        elif analysis['user_intent'] == 'asking_question':
            if context.state == ConversationState.CONSULTING:
                return self.handle_consulting_question(message, user_id)
            else:
                response = "Tôi sẽ trả lời câu hỏi của bạn sau khi hoàn thành phân tích tử vi. Trước tiên, tôi cần thu thập đủ thông tin cơ bản."
                self.db_manager.save_chat_message(user_id, response, "assistant")
                return response
        
        elif analysis['user_intent'] == 'providing_info':
            # Trích xuất thông tin bằng LLM
            if analysis.get('should_extract_info', True):
                updated_user_info = self.llm_provider.extract_information(message, context)
                context.collected_info = updated_user_info
            
            # Kiểm tra đủ thông tin
            if self.info_extractor.is_info_complete(context.collected_info):
                return self._perform_tuvi_analysis(user_id, context.collected_info)
            else:
                missing_fields = self.info_extractor.get_missing_fields(context.collected_info)
                response = self.response_generator.generate_info_request_response(missing_fields)
                context.state = ConversationState.COLLECTING_INFO
                self.db_manager.save_user_session(user_id, context)
                self.db_manager.save_chat_message(user_id, response, "assistant")
                return response
        
        else:
            # Sử dụng phản hồi được gợi ý từ LLM
            if analysis.get('suggested_response'):
                response = analysis['suggested_response']
            else:
                response = "Tôi hiểu bạn muốn tư vấn tử vi. Hãy chia sẻ thông tin cơ bản về bạn."
            
            self.db_manager.save_chat_message(user_id, response, "assistant")
            return response
