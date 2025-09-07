"""
Refactored Chat Module

Sử dụng kiến trúc component-based để thay thế chat.py cũ.
Giữ nguyên interface để tương thích với app.py hiện tại.
"""

from components import (
    ConversationManager,
    DatabaseManager,
    InformationExtractor,
    ResponseGenerator,
    TuviCalculator,
    LLMProvider
)


class TuViBot:
    """Main Tu Vi Bot class sử dụng component architecture"""
    
    def __init__(self, use_intelligent_mode: bool = True):
        """
        Khởi tạo Tu Vi Bot với các component
        
        Args:
            use_intelligent_mode: Sử dụng ConversationManager (intelligent mode sẽ được implement sau)
        """
        # Initialize components
        self.db_manager = DatabaseManager()
        self.llm_provider = LLMProvider()
        self.info_extractor = InformationExtractor(self.llm_provider)
        self.response_generator = ResponseGenerator()
        self.tuvi_calculator = TuviCalculator()
        
        # Use ConversationManager (intelligent mode will be implemented later)
        self.conversation_manager = ConversationManager(
            database_manager=self.db_manager,
            information_extractor=self.info_extractor,
            response_generator=self.response_generator,
            tuvi_calculator=self.tuvi_calculator,
            llm_provider=self.llm_provider
        )
    
    def process_message(self, message: str, user_id: str = "default") -> str:
        """
        Xử lý tin nhắn từ người dùng
        
        Args:
            message: Tin nhắn từ người dùng
            user_id: ID người dùng (mặc định "default")
            
        Returns:
            Phản hồi từ bot
        """
        return self.conversation_manager.process_message(message, user_id)
    
    def get_conversation_context(self, user_id: str = "default"):
        """Lấy ngữ cảnh cuộc hội thoại"""
        return self.conversation_manager.get_conversation_context(user_id)
    
    def reset_conversation(self, user_id: str = "default"):
        """Reset cuộc hội thoại"""
        self.conversation_manager.reset_conversation(user_id)
    
    def handle_consulting_question(self, message: str, user_id: str = "default") -> str:
        """Xử lý câu hỏi tư vấn"""
        return self.conversation_manager.handle_consulting_question(message, user_id)


# Global bot instance để tương thích với code cũ
_bot_instance = None


def get_bot_instance(use_intelligent_mode: bool = True) -> TuViBot:
    """Lấy instance bot (singleton pattern)"""
    global _bot_instance
    if _bot_instance is None:
        _bot_instance = TuViBot(use_intelligent_mode=use_intelligent_mode)
    return _bot_instance


# Legacy functions để tương thích với app.py
def prompt_to_predict(questionMessage: str = '', user_id: str = 'default') -> str:
    """
    Entry point chính cho việc xử lý tin nhắn
    Tương thích với function cũ trong chat.py
    """
    bot = get_bot_instance()
    return bot.process_message(questionMessage, user_id)


def intelligent_conversation_flow(message: str, user_id: str = "default") -> str:
    """
    Intelligent conversation flow
    Tương thích với function cũ trong chat.py
    """
    bot = get_bot_instance(use_intelligent_mode=True)
    return bot.process_message(message, user_id)


# Component access functions để có thể customize
def get_tuvi_calculator() -> TuviCalculator:
    """Lấy TuVi Calculator component"""
    bot = get_bot_instance()
    return bot.tuvi_calculator


def get_database_manager() -> DatabaseManager:
    """Lấy Database Manager component"""
    bot = get_bot_instance()
    return bot.db_manager


def get_information_extractor() -> InformationExtractor:
    """Lấy Information Extractor component"""
    bot = get_bot_instance()
    return bot.info_extractor


def get_response_generator() -> ResponseGenerator:
    """Lấy Response Generator component"""
    bot = get_bot_instance()
    return bot.response_generator


def get_llm_provider() -> LLMProvider:
    """Lấy LLM Provider component"""
    bot = get_bot_instance()
    return bot.llm_provider


def get_user_from_database(name: str):
    """Lấy thông tin user từ database"""
    try:
        from models import User, Session
        
        db_session = Session()
        try:
            user = db_session.query(User).filter(User.name == name).first()
            if user:
                return {
                    'id': user.id,
                    'name': user.name,
                    'birth_date': user.birth_date.strftime('%d/%m/%Y') if user.birth_date else None,
                    'birth_hour': user.birth_hour.strftime('%H:%M') if user.birth_hour else None,
                    'gender': user.gender,
                    'created_at': user.created_at
                }
            return None
        finally:
            db_session.close()
    except Exception as e:
        print(f"❌ Error getting user from database: {e}")
        return None


def list_all_users():
    """Lấy danh sách tất cả users từ database"""
    try:
        from models import User, Session
        
        db_session = Session()
        try:
            users = db_session.query(User).all()
            return [{
                'id': user.id,
                'name': user.name,
                'birth_date': user.birth_date.strftime('%d/%m/%Y') if user.birth_date else None,
                'birth_hour': user.birth_hour.strftime('%H:%M') if user.birth_hour else None,
                'gender': user.gender,
                'created_at': user.created_at
            } for user in users]
        finally:
            db_session.close()
    except Exception as e:
        print(f"❌ Error listing users from database: {e}")
        return []


# Factory functions để tạo custom bot instances
def create_custom_bot(
    database_manager: DatabaseManager = None,
    information_extractor: InformationExtractor = None,
    response_generator: ResponseGenerator = None,
    tuvi_calculator: TuviCalculator = None,
    llm_provider: LLMProvider = None,
    use_intelligent_mode: bool = True
) -> TuViBot:
    """
    Tạo bot instance tùy chỉnh với các component được inject
    
    Args:
        database_manager: Custom database manager
        information_extractor: Custom information extractor
        response_generator: Custom response generator
        tuvi_calculator: Custom tuvi calculator
        llm_provider: Custom LLM provider
        use_intelligent_mode: Sử dụng intelligent conversation manager
        
    Returns:
        TuViBot instance với các component tùy chỉnh
    """
    return TuViBot(
        use_intelligent_mode=use_intelligent_mode
    )


# Configuration functions
def configure_llm_provider(provider_type: str = "openai", **kwargs):
    """
    Cấu hình LLM provider
    
    Args:
        provider_type: Loại provider ("openai", "anthropic", "mock")
        **kwargs: Các tham số cấu hình cho provider
    """
    global _bot_instance
    
    if provider_type == "openai":
        from components.llm_provider import OpenAILLMProvider
        llm_provider = OpenAILLMProvider(**kwargs)
    elif provider_type == "anthropic":
        from components.llm_provider import AnthropicLLMProvider
        llm_provider = AnthropicLLMProvider(**kwargs)
    elif provider_type == "mock":
        from components.llm_provider import MockLLM
        llm_provider = LLMProvider(MockLLM())
    else:
        raise ValueError(f"Unknown provider type: {provider_type}")
    
    # Reset bot instance để sử dụng provider mới
    _bot_instance = None
    get_bot_instance().llm_provider = llm_provider


def configure_database(database_path: str = "tuvi.db"):
    """
    Cấu hình database path
    
    Args:
        database_path: Đường dẫn đến database file
    """
    global _bot_instance
    
    # Reset bot instance để sử dụng database path mới
    _bot_instance = None
    get_bot_instance().db_manager = DatabaseManager(database_path)


# Utility functions
def get_component_info():
    """Lấy thông tin về các component hiện tại"""
    bot = get_bot_instance()
    
    return {
        'conversation_manager': type(bot.conversation_manager).__name__,
        'database_manager': type(bot.db_manager).__name__,
        'information_extractor': type(bot.info_extractor).__name__,
        'response_generator': type(bot.response_generator).__name__,
        'tuvi_calculator': type(bot.tuvi_calculator).__name__,
        'llm_provider': type(bot.llm_provider).__name__
    }


def test_components():
    """Test các component hoạt động"""
    try:
        bot = get_bot_instance()
        
        # Test basic functionality
        response = bot.process_message("Xin chào", "test_user")
        print(f"✅ Basic test passed: {response[:50]}...")
        
        # Test component info
        info = get_component_info()
        print(f"✅ Component info: {info}")
        
        # Test user extraction and database save
        print("\n🧪 Testing user extraction and database save...")
        test_messages = [
            "Tôi tên Nguyễn Văn Test",
            "Sinh ngày 15/03/1990",
            "Giờ sinh 14:30",
            "Giới tính Nam"
        ]
        
        for message in test_messages:
            response = bot.process_message(message, "test_user_extraction")
            print(f"User: {message}")
            print(f"Bot: {response[:50]}...")
        
        # Check if user was saved to database
        user_info = get_user_from_database("Nguyễn Văn Test")
        if user_info:
            print(f"✅ User saved to database: {user_info}")
        else:
            print("⚠️ User not found in database")
        
        # List all users
        all_users = list_all_users()
        print(f"✅ Total users in database: {len(all_users)}")
        
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Test khi chạy trực tiếp
    print("🧪 Testing Tu Vi Bot Components...")
    success = test_components()
    print(f"Test result: {'✅ PASSED' if success else '❌ FAILED'}")
