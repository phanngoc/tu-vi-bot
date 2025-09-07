# 🏗️ Tu Vi Bot - Component-Based Architecture

## 📋 Tổng quan

Tu Vi Bot đã được refactor từ kiến trúc monolithic (1 file 1768 dòng) thành kiến trúc component-based với các nguyên tắc:

- **Keep it Simple**: Mỗi component có trách nhiệm rõ ràng và đơn giản
- **Plug-in Architecture**: Dễ dàng thay thế component mà không ảnh hưởng đến các component khác
- **Dependency Injection**: Các component có thể được inject và test độc lập
- **Interface Segregation**: Mỗi interface chỉ định nghĩa những method cần thiết

## 🧩 Cấu trúc Component

```
components/
├── __init__.py                 # Package initialization
├── interfaces.py              # Interface definitions
├── config.py                  # Configuration management
├── tuvi_calculator.py         # Tu Vi calculation engine
├── database_manager.py        # Database operations
├── information_extractor.py   # Information extraction
├── response_generator.py      # Response generation
├── llm_provider.py           # LLM integration
└── conversation_manager.py    # Conversation orchestration
```

## 🔌 Component Interfaces

### 1. ITuviCalculator
```python
class ITuviCalculator(ABC):
    def calculate_tuvi(self, user_info: UserInfo) -> TuviResult
    def get_star_strength(self, star_name: str, chi_position: str) -> str
```

### 2. IConversationManager
```python
class IConversationManager(ABC):
    def process_message(self, message: str, user_id: str) -> str
    def get_conversation_context(self, user_id: str) -> ConversationContext
    def reset_conversation(self, user_id: str) -> None
```

### 3. IDatabaseManager
```python
class IDatabaseManager(ABC):
    def save_user_session(self, user_id: str, context: ConversationContext) -> None
    def get_user_session(self, user_id: str) -> Optional[ConversationContext]
    def save_chat_message(self, user_id: str, message: str, role: str) -> None
    def get_chat_history(self, user_id: str, limit: int = 50) -> List[Dict[str, str]]
```

### 4. IInformationExtractor
```python
class IInformationExtractor(ABC):
    def extract_user_info(self, message: str, context: ConversationContext) -> UserInfo
    def is_info_complete(self, user_info: UserInfo) -> bool
    def get_missing_fields(self, user_info: UserInfo) -> List[str]
```

### 5. IResponseGenerator
```python
class IResponseGenerator(ABC):
    def generate_greeting_response(self) -> str
    def generate_info_request_response(self, missing_fields: List[str]) -> str
    def generate_tuvi_analysis_response(self, user_info: UserInfo, tuvi_result: TuviResult) -> str
    def generate_consulting_response(self, question: str, user_info: UserInfo, tuvi_result: TuviResult) -> str
```

### 6. ILLMProvider
```python
class ILLMProvider(ABC):
    def analyze_conversation(self, message: str, context: ConversationContext) -> Dict[str, Any]
    def extract_information(self, message: str, context: ConversationContext) -> UserInfo
    def generate_response(self, prompt: str) -> str
```

## 🎯 Component Implementations

### 1. TuviCalculator
- **Trách nhiệm**: Tính toán lá số tử vi theo phương pháp truyền thống
- **Có thể thay thế**: Thuật toán tính toán khác, API external
- **Dependencies**: Không có (pure calculation)

### 2. DatabaseManager
- **Trách nhiệm**: Quản lý database và session
- **Có thể thay thế**: PostgreSQL, MongoDB, Redis, in-memory storage
- **Dependencies**: SQLAlchemy models

### 3. InformationExtractor
- **Trách nhiệm**: Trích xuất thông tin từ tin nhắn
- **Có thể thay thế**: LLM-based extraction, NLP libraries
- **Dependencies**: Regex patterns, có thể dùng LLM

### 4. ResponseGenerator
- **Trách nhiệm**: Tạo phản hồi cho người dùng
- **Có thể thay thế**: Template engines, AI response generation
- **Dependencies**: TuviResult, UserInfo

### 5. LLMProvider
- **Trách nhiệm**: Tích hợp với LLM models
- **Có thể thay thế**: OpenAI, Anthropic, local models, mock
- **Dependencies**: LLM libraries

### 6. ConversationManager
- **Trách nhiệm**: Điều phối các component khác
- **Có thể thay thế**: Rule-based, AI-powered conversation flows
- **Dependencies**: Tất cả các component khác

## 🔄 Dependency Flow

```
ConversationManager
├── DatabaseManager (saves/loads context)
├── InformationExtractor (extracts user info)
├── TuviCalculator (calculates tuvi)
├── ResponseGenerator (generates responses)
└── LLMProvider (intelligent analysis)
```

## 🚀 Usage Examples

### Basic Usage
```python
from chat_refactored import prompt_to_predict

# Sử dụng như cũ
response = prompt_to_predict("Tôi tên Nguyễn Văn A, sinh 15/03/1990")
```

### Custom Components
```python
from components import *
from chat_refactored import create_custom_bot

# Tạo custom bot với components tùy chỉnh
custom_bot = create_custom_bot(
    database_manager=CustomDatabaseManager(),
    llm_provider=CustomLLMProvider(),
    use_intelligent_mode=True
)

response = custom_bot.process_message("Xin chào")
```

### Configuration
```python
from components.config import configure_llm_provider, configure_database

# Cấu hình LLM provider
configure_llm_provider("openai", api_key="your-key", model="gpt-4")

# Cấu hình database
configure_database("custom_tuvi.db")
```

## 🧪 Testing

### Component Testing
```python
from components import TuviCalculator, UserInfo

# Test individual component
calculator = TuviCalculator()
user_info = UserInfo(name="Test", birthday="15/03/1990", birth_time="14:30", gender="Nam")
result = calculator.calculate_tuvi(user_info)
```

### Integration Testing
```python
from chat_refactored import test_components

# Test all components
success = test_components()
```

## 🔧 Environment Configuration

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

## 📈 Benefits

### 1. Maintainability
- Mỗi component có trách nhiệm rõ ràng
- Dễ debug và fix lỗi
- Code dễ đọc và hiểu

### 2. Testability
- Test từng component độc lập
- Mock dependencies dễ dàng
- Integration testing rõ ràng

### 3. Extensibility
- Thêm component mới không ảnh hưởng code cũ
- Thay thế implementation dễ dàng
- Plugin architecture

### 4. Scalability
- Scale từng component riêng biệt
- Microservices-ready
- Load balancing per component

## 🔄 Migration Path

### Phase 1: Component Creation ✅
- Tạo interfaces và implementations
- Test individual components

### Phase 2: Integration ✅
- Tạo ConversationManager
- Refactor chat.py

### Phase 3: Configuration
- Environment-based config
- Runtime component switching

### Phase 4: Advanced Features
- Caching layer
- Monitoring and metrics
- A/B testing framework

## 🎯 Future Enhancements

1. **Caching Layer**: Cache TuVi calculations
2. **Metrics & Monitoring**: Component performance tracking
3. **A/B Testing**: Test different component implementations
4. **Microservices**: Deploy components as separate services
5. **Plugin System**: Dynamic component loading
6. **Configuration UI**: Web-based configuration management
