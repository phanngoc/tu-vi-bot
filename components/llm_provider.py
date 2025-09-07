"""
LLM Provider Component

Component tích hợp với các LLM models, có thể dễ dàng thay thế bằng các provider khác.
"""

from typing import Dict, Any
from .interfaces import ILLMProvider, UserInfo, ConversationContext


class LLMProvider(ILLMProvider):
    """Provider tích hợp với LLM"""
    
    def __init__(self, llm_model=None):
        self.llm_model = llm_model
        if not self.llm_model:
            # Default LLM setup
            self._setup_default_llm()
    
    def analyze_conversation(self, message: str, context: ConversationContext) -> Dict[str, Any]:
        """Phân tích cuộc hội thoại bằng LLM"""
        prompt = f"""
        Phân tích cuộc hội thoại và đưa ra quyết định thông minh:

        Tin nhắn hiện tại: '{message}'
        Trạng thái hiện tại: {context.state.value}
        Thông tin đã thu thập: {self._user_info_to_string(context.collected_info)}
        Lịch sử cuộc hội thoại: {self._message_history_to_string(context.message_history)}

        Hãy phân tích:
        1. Ý định của người dùng (greeting, providing_info, asking_question, reset, etc.)
        2. Trạng thái thông tin hiện tại
        3. Phản hồi phù hợp nhất
        4. Có nên trích xuất thông tin không
        5. Có nên tiến hành phân tích không
        6. Tone phù hợp (friendly/professional/urgent)

        Trả về kết quả dưới dạng JSON.
        """
        
        try:
            response = self.llm_model.query(prompt)
            # Parse response (simplified)
            return self._parse_analysis_response(str(response))
        except Exception as e:
            # Fallback analysis
            return self._fallback_analysis(message, context)
    
    def extract_information(self, message: str, context: ConversationContext) -> UserInfo:
        """Trích xuất thông tin bằng LLM"""
        prompt = f"""
        Từ cuộc hội thoại sau, hãy trích xuất thông tin một cách thông minh:

        Tin nhắn hiện tại: '{message}'
        Lịch sử cuộc hội thoại: {self._message_history_to_string(context.message_history)}

        Hãy phân tích và trích xuất:
        1. Tên người dùng (nếu có)
        2. Ngày sinh (định dạng DD/MM/YYYY)
        3. Giờ sinh (định dạng HH:MM)
        4. Giới tính (Nam hoặc Nữ)

        Trả về kết quả dưới dạng JSON với các trường: name, birthday, birth_time, gender
        """
        
        try:
            response = self.llm_model.query(prompt)
            return self._parse_user_info_response(str(response))
        except Exception as e:
            # Fallback to existing info
            return context.collected_info
    
    def generate_response(self, prompt: str) -> str:
        """Tạo phản hồi bằng LLM"""
        try:
            response = self.llm_model.query(prompt)
            return str(response)
        except Exception as e:
            return f"Xin lỗi, tôi gặp khó khăn trong việc xử lý yêu cầu của bạn. Lỗi: {str(e)}"
    
    def _setup_default_llm(self):
        """Setup LLM mặc định"""
        try:
            from llama_index.llms.openai import OpenAI
            self.llm_model = OpenAI(model="gpt-4o-mini")
        except ImportError:
            print("Warning: OpenAI not available, using mock LLM")
            self.llm_model = MockLLM()
    
    def _user_info_to_string(self, user_info: UserInfo) -> str:
        """Convert UserInfo to string"""
        return f"Tên: {user_info.name}, Ngày sinh: {user_info.birthday}, Giờ sinh: {user_info.birth_time}, Giới tính: {user_info.gender}"
    
    def _message_history_to_string(self, message_history) -> str:
        """Convert message history to string"""
        if not message_history:
            return "Chưa có lịch sử"
        
        history_str = ""
        for msg in message_history[-5:]:  # Last 5 messages
            history_str += f"{msg['role']}: {msg['message']}\n"
        
        return history_str
    
    def _parse_analysis_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM analysis response"""
        # Simplified parsing - có thể cải thiện
        return {
            'user_intent': 'providing_info',
            'suggested_response': response[:200] + "..." if len(response) > 200 else response,
            'should_extract_info': True,
            'should_analyze': False,
            'conversation_tone': 'friendly'
        }
    
    def _parse_user_info_response(self, response: str) -> UserInfo:
        """Parse LLM user info response"""
        # Simplified parsing - có thể cải thiện
        import re
        
        user_info = UserInfo()
        
        # Extract name
        name_match = re.search(r'"name":\s*"([^"]*)"', response)
        if name_match:
            user_info.name = name_match.group(1)
        
        # Extract birthday
        birthday_match = re.search(r'"birthday":\s*"([^"]*)"', response)
        if birthday_match:
            user_info.birthday = birthday_match.group(1)
        
        # Extract birth_time
        time_match = re.search(r'"birth_time":\s*"([^"]*)"', response)
        if time_match:
            user_info.birth_time = time_match.group(1)
        
        # Extract gender
        gender_match = re.search(r'"gender":\s*"([^"]*)"', response)
        if gender_match:
            user_info.gender = gender_match.group(1)
        
        return user_info
    
    def _fallback_analysis(self, message: str, context: ConversationContext) -> Dict[str, Any]:
        """Fallback analysis khi LLM không khả dụng"""
        return {
            'user_intent': 'unknown',
            'suggested_response': 'Xin lỗi, tôi gặp khó khăn trong việc hiểu tin nhắn của bạn. Vui lòng thử lại.',
            'should_extract_info': False,
            'should_analyze': False,
            'conversation_tone': 'friendly'
        }


class MockLLM:
    """Mock LLM cho testing hoặc khi không có LLM thật"""
    
    def query(self, prompt: str) -> str:
        """Mock query response"""
        return "Đây là phản hồi mock từ LLM. Trong thực tế, đây sẽ là phản hồi từ LLM thật."


class OpenAILLMProvider(LLMProvider):
    """LLM Provider sử dụng OpenAI"""
    
    def __init__(self, api_key: str = None, model: str = "gpt-4o-mini"):
        try:
            from llama_index.llms.openai import OpenAI
            self.llm_model = OpenAI(model=model, api_key=api_key)
        except ImportError:
            raise ImportError("OpenAI package not available. Please install llama-index-llms-openai")
        except Exception as e:
            raise Exception(f"Failed to initialize OpenAI LLM: {e}")


class AnthropicLLMProvider(LLMProvider):
    """LLM Provider sử dụng Anthropic Claude"""
    
    def __init__(self, api_key: str = None, model: str = "claude-3-sonnet-20240229"):
        try:
            from llama_index.llms.anthropic import Anthropic
            self.llm_model = Anthropic(model=model, api_key=api_key)
        except ImportError:
            raise ImportError("Anthropic package not available. Please install llama-index-llms-anthropic")
        except Exception as e:
            raise Exception(f"Failed to initialize Anthropic LLM: {e}")
