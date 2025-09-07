# 🏗️ Tu Vi Bot - Component Architecture

## 🎯 Tổng quan

Tu Vi Bot đã được refactor từ kiến trúc monolithic thành **component-based architecture** với các nguyên tắc:

- **Keep it Simple**: Mỗi component có trách nhiệm rõ ràng và đơn giản
- **Plug-in Architecture**: Dễ dàng thay thế component mà không ảnh hưởng đến các component khác
- **Dependency Injection**: Các component có thể được inject và test độc lập

## 📁 Cấu trúc thư mục

```
components/
├── __init__.py                 # Package initialization
├── interfaces.py              # Interface definitions (ABC)
├── config.py                  # Configuration management
├── tuvi_calculator.py         # Tu Vi calculation engine
├── database_manager.py        # Database operations
├── information_extractor.py   # Information extraction
├── response_generator.py      # Response generation
├── llm_provider.py           # LLM integration
└── conversation_manager.py    # Conversation orchestration

chat_refactored.py             # Main refactored chat module
demo_component_architecture.py # Demo và testing
ARCHITECTURE.md                # Detailed architecture docs
```

## 🚀 Quick Start

### 1. Sử dụng cơ bản (tương thích với code cũ)

```python
from chat_refactored import prompt_to_predict

# Sử dụng như cũ - không cần thay đổi code
response = prompt_to_predict("Tôi tên Nguyễn Văn A, sinh 15/03/1990, 14:30, Nam")
print(response)
```

### 2. Sử dụng component architecture

```python
from chat_refactored import TuViBot

# Tạo bot instance
bot = TuViBot(use_intelligent_mode=True)

# Xử lý tin nhắn
response = bot.process_message("Xin chào", user_id="user123")
print(response)
```

### 3. Custom components

```python
from components import *
from chat_refactored import create_custom_bot

# Tạo custom information extractor
class CustomInfoExtractor(InformationExtractor):
    def extract_user_info(self, message, context):
        # Custom logic
        return super().extract_user_info(message, context)

# Tạo bot với custom components
custom_bot = create_custom_bot(
    information_extractor=CustomInfoExtractor(),
    use_intelligent_mode=True
)

response = custom_bot.process_message("Xin chào")
```

## 🧩 Component Details

### 1. TuviCalculator
**Trách nhiệm**: Tính toán lá số tử vi
```python
calculator = TuviCalculator()
result = calculator.calculate_tuvi(user_info)
```

### 2. DatabaseManager
**Trách nhiệm**: Quản lý database và session
```python
db_manager = DatabaseManager("tuvi.db")
db_manager.save_user_session(user_id, context)
```

### 3. InformationExtractor
**Trách nhiệm**: Trích xuất thông tin từ tin nhắn
```python
extractor = InformationExtractor()
user_info = extractor.extract_user_info(message, context)
```

### 4. ResponseGenerator
**Trách nhiệm**: Tạo phản hồi cho người dùng
```python
generator = ResponseGenerator()
response = generator.generate_greeting_response()
```

### 5. LLMProvider
**Trách nhiệm**: Tích hợp với LLM models
```python
llm_provider = LLMProvider()
analysis = llm_provider.analyze_conversation(message, context)
```

### 6. ConversationManager
**Trách nhiệm**: Điều phối các component khác
```python
manager = ConversationManager()
response = manager.process_message(message, user_id)
```

## ⚙️ Configuration

### Environment Variables
```bash
# Database
export TUVIBOT_DB_PATH="tuvi.db"
export TUVIBOT_DB_POOL_SIZE="5"

# LLM
export TUVIBOT_LLM_PROVIDER="openai"
export TUVIBOT_LLM_MODEL="gpt-4o-mini"
export TUVIBOT_LLM_API_KEY="your-key"

# Features
export TUVIBOT_INTELLIGENT_MODE="true"
export TUVIBOT_ENABLE_STAR_STRENGTH="true"
```

### Programmatic Configuration
```python
from chat_refactored import configure_llm_provider, configure_database

# Cấu hình LLM
configure_llm_provider("openai", api_key="your-key", model="gpt-4")

# Cấu hình database
configure_database("custom_tuvi.db")
```

## 🧪 Testing

### Run Demo
```bash
python demo_component_architecture.py
```

### Test Individual Components
```python
from components import TuviCalculator, UserInfo

# Test calculator
calculator = TuviCalculator()
user_info = UserInfo(name="Test", birthday="15/03/1990", birth_time="14:30", gender="Nam")
result = calculator.calculate_tuvi(user_info)
print(result.basic_info)
```

### Test Integration
```python
from chat_refactored import test_components

success = test_components()
print(f"Test result: {'✅ PASSED' if success else '❌ FAILED'}")
```

## 🔌 Plugin System

### Thay thế LLM Provider
```python
from components.llm_provider import OpenAILLMProvider, AnthropicLLMProvider

# OpenAI
openai_provider = OpenAILLMProvider(api_key="your-key")

# Anthropic
anthropic_provider = AnthropicLLMProvider(api_key="your-key")

# Sử dụng trong bot
bot = create_custom_bot(llm_provider=openai_provider)
```

### Thay thế Database
```python
class CustomDatabaseManager(DatabaseManager):
    def save_user_session(self, user_id, context):
        # Custom database logic
        pass

bot = create_custom_bot(database_manager=CustomDatabaseManager())
```

### Thay thế Information Extractor
```python
class AIInfoExtractor(InformationExtractor):
    def extract_user_info(self, message, context):
        # Sử dụng AI/ML để extract
        return super().extract_user_info(message, context)

bot = create_custom_bot(information_extractor=AIInfoExtractor())
```

## 📊 Benefits

### 1. Maintainability
- ✅ Mỗi component có trách nhiệm rõ ràng
- ✅ Dễ debug và fix lỗi
- ✅ Code dễ đọc và hiểu

### 2. Testability
- ✅ Test từng component độc lập
- ✅ Mock dependencies dễ dàng
- ✅ Integration testing rõ ràng

### 3. Extensibility
- ✅ Thêm component mới không ảnh hưởng code cũ
- ✅ Thay thế implementation dễ dàng
- ✅ Plugin architecture

### 4. Scalability
- ✅ Scale từng component riêng biệt
- ✅ Microservices-ready
- ✅ Load balancing per component

## 🔄 Migration từ code cũ

### Trước (chat.py - 1768 dòng)
```python
# Tất cả logic trong 1 file
def prompt_to_predict(questionMessage='', user_id='default'):
    # 1768 dòng code phức tạp
    pass
```

### Sau (component-based)
```python
# Logic được chia thành các component
bot = TuViBot()
response = bot.process_message(message, user_id)
```

### Backward Compatibility
```python
# Code cũ vẫn hoạt động
from chat_refactored import prompt_to_predict
response = prompt_to_predict("Xin chào")  # ✅ Hoạt động như cũ
```

## 🎯 Use Cases

### 1. Development
```python
# Test với mock components
bot = create_custom_bot(
    llm_provider=MockLLMProvider(),
    database_manager=InMemoryDatabaseManager()
)
```

### 2. Production
```python
# Sử dụng production components
bot = create_custom_bot(
    llm_provider=OpenAILLMProvider(api_key=os.getenv('OPENAI_API_KEY')),
    database_manager=DatabaseManager("production_tuvi.db")
)
```

### 3. A/B Testing
```python
# Test different implementations
bot_a = create_custom_bot(information_extractor=RegexExtractor())
bot_b = create_custom_bot(information_extractor=AIExtractor())

# Compare results
response_a = bot_a.process_message(message)
response_b = bot_b.process_message(message)
```

## 🚀 Future Enhancements

1. **Caching Layer**: Cache TuVi calculations
2. **Metrics & Monitoring**: Component performance tracking
3. **A/B Testing**: Test different component implementations
4. **Microservices**: Deploy components as separate services
5. **Plugin System**: Dynamic component loading
6. **Configuration UI**: Web-based configuration management

## 📚 Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - Detailed architecture documentation
- [demo_component_architecture.py](demo_component_architecture.py) - Complete demo
- [components/interfaces.py](components/interfaces.py) - Interface definitions

## 🤝 Contributing

1. Tạo component mới bằng cách implement interface tương ứng
2. Test component độc lập
3. Tích hợp vào ConversationManager
4. Update documentation

## 📞 Support

Nếu có vấn đề với component architecture:
1. Check [demo_component_architecture.py](demo_component_architecture.py)
2. Review [ARCHITECTURE.md](ARCHITECTURE.md)
3. Test individual components
4. Check configuration
