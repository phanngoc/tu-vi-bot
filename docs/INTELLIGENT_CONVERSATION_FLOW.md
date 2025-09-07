# Intelligent Conversation Flow - LLM-based Analysis

## Tổng quan

Hệ thống đã được refactor hoàn toàn để sử dụng LLM-based analysis, tạo ra một trải nghiệm conversation thông minh và tự nhiên như một consultant tử vi thực sự.

## Kiến trúc thông minh

### 1. LLM-based Analysis System
- **ConversationAnalysis**: Phân tích ý định và context của người dùng
- **SmartInfoExtraction**: Trích xuất thông tin thông minh từ toàn bộ cuộc hội thoại
- **InfoCompletenessCheck**: Tự động phát hiện khi đủ thông tin để phân tích

### 2. Dynamic Conversation States
```python
class ConversationState(Enum):
    GREETING = "greeting"           # Chào hỏi ban đầu
    COLLECTING_INFO = "collecting_info"  # Thu thập thông tin động
    ANALYZING = "analyzing"         # Phân tích tử vi
    CONSULTING = "consulting"       # Tư vấn sau phân tích
    RESET = "reset"                 # Khởi tạo lại
```

### 3. Intelligent Response Generation
- Sử dụng LLM để tạo phản hồi phù hợp với context
- Tự động điều chỉnh tone và phong cách
- Xử lý các tình huống phức tạp một cách thông minh

## Flow hoạt động

### 1. Conversation Analysis
```
User Message → LLM Analysis → Determine Intent → Generate Response
     │              │              │
     ▼              ▼              ▼
"Xin chào" → conversation_analysis → greeting → "Chào mừng..."
```

### 2. Information Extraction
```
User Message + Context → Smart Extraction → Update Info → Check Completeness
     │                        │                │
     ▼                        ▼                ▼
"Tên A, sinh 15/03" → extract_intelligently → Update DB → Complete?
```

### 3. Automatic Analysis Trigger
```
Enough Info Detected → Auto Analysis → Tuvi Chart → Consulting Mode
     │                      │              │
     ▼                      ▼              ▼
All 4 fields → perform_tuvi_analysis → Chart Data → Ready for questions
```

## Tính năng thông minh

### 1. Context Awareness
- Hiểu được toàn bộ cuộc hội thoại
- Nhớ thông tin từ các tin nhắn trước
- Phản hồi phù hợp với context

### 2. Intelligent Information Detection
- Tự động phát hiện khi đủ thông tin
- Trích xuất thông tin từ bất kỳ tin nhắn nào
- Xử lý thông tin không đầy đủ một cách thông minh

### 3. Dynamic Conversation Flow
- Không còn step-based cứng nhắc
- Tự nhiên như conversation thật
- Linh hoạt xử lý mọi tình huống

### 4. Smart Error Handling
- Xử lý lỗi một cách thông minh
- Fallback mechanisms
- Graceful degradation

## Các Pydantic Models

### ConversationAnalysis
```python
class ConversationAnalysis(BaseModel):
    current_state: str              # Trạng thái hiện tại
    user_intent: str               # Ý định của user
    information_status: InfoCompletenessCheck  # Trạng thái thông tin
    suggested_response: str        # Phản hồi gợi ý
    should_extract_info: bool     # Có nên trích xuất thông tin
    should_analyze: bool          # Có nên phân tích
    conversation_tone: str        # Tone cuộc hội thoại
```

### SmartInfoExtraction
```python
class SmartInfoExtraction(BaseModel):
    extracted_name: str           # Tên trích xuất
    extracted_birthday: str       # Ngày sinh
    extracted_birth_time: str     # Giờ sinh
    extracted_gender: str         # Giới tính
    is_name_valid: bool          # Tên hợp lệ
    is_birthday_valid: bool      # Ngày sinh hợp lệ
    is_birth_time_valid: bool    # Giờ sinh hợp lệ
    is_gender_valid: bool        # Giới tính hợp lệ
    overall_confidence: str      # Mức độ tin cậy
    should_proceed_to_analysis: bool  # Có nên phân tích
```

## Ví dụ sử dụng

### Scenario 1: Complete info in one message
```
User: "Xin chào"
Bot: "🔮 Chào mừng bạn đến với dịch vụ tư vấn tử vi thông minh!..."

User: "Tôi tên Nguyễn Văn A, sinh ngày 15/03/1990, 14:30, giới tính Nam"
Bot: "✅ Tuyệt vời! Tôi đã có đủ thông tin để tiến hành phân tích tử vi cho bạn."
     [Tự động tiến hành phân tích]
```

### Scenario 2: Gradual info collection
```
User: "Hello"
Bot: "🔮 Chào mừng bạn đến với dịch vụ tư vấn tử vi thông minh!..."

User: "Tôi tên Phan Thị B"
Bot: "📝 Cảm ơn bạn đã cung cấp thông tin! Tôi vẫn cần thêm: ngày sinh, giờ sinh, giới tính"

User: "Sinh ngày 20/05/1995"
Bot: "📝 Cảm ơn bạn đã cung cấp thông tin! Tôi vẫn cần thêm: giờ sinh, giới tính"

User: "Giờ sinh 8:30 sáng, giới tính Nữ"
Bot: "✅ Tuyệt vời! Tôi đã có đủ thông tin để tiến hành phân tích tử vi cho bạn."
     [Tự động tiến hành phân tích]
```

### Scenario 3: Mixed conversation
```
User: "Chào bạn"
Bot: "🔮 Chào mừng bạn đến với dịch vụ tư vấn tử vi thông minh!..."

User: "Tôi muốn xem tử vi"
Bot: "Tôi hiểu bạn muốn tư vấn tử vi. Hãy chia sẻ thông tin cơ bản về bạn..."

User: "Tên tôi là Trần Văn C, sinh 10/12/1988, 16:45, Nam"
Bot: "✅ Tuyệt vời! Tôi đã có đủ thông tin để tiến hành phân tích tử vi cho bạn."
     [Tự động tiến hành phân tích]

User: "Vận mệnh của tôi như thế nào?"
Bot: [Trả lời dựa trên lá số tử vi đã phân tích]
```

## Lợi ích của Intelligent Flow

### 1. User Experience
- **Tự nhiên**: Conversation như với consultant thật
- **Linh hoạt**: Không bị ràng buộc bởi steps cứng nhắc
- **Thông minh**: Hiểu được ý định và context

### 2. Developer Experience
- **Dễ maintain**: Code sạch và có cấu trúc
- **Extensible**: Dễ dàng thêm tính năng mới
- **Robust**: Xử lý lỗi tốt

### 3. Performance
- **Efficient**: Chỉ sử dụng LLM khi cần thiết
- **Scalable**: Có thể xử lý nhiều user đồng thời
- **Reliable**: Fallback mechanisms đảm bảo hoạt động ổn định

## Testing

Chạy test script:
```bash
python test_intelligent_flow.py
```

Script sẽ test:
- Complete info scenarios
- Gradual info collection
- Mixed conversations
- Reset and restart
- Edge cases and error handling

## Migration từ Step-based Flow

### Thay đổi chính:
1. **CollectionStep** → **ConversationState**
2. **Step-based functions** → **Intelligent analysis**
3. **Manual step management** → **Automatic state detection**
4. **Rigid flow** → **Dynamic conversation**

### Backward compatibility:
- `prompt_to_predict()` function vẫn hoạt động như cũ
- Database schema không thay đổi
- API interface giữ nguyên

## Kết luận

Intelligent Conversation Flow tạo ra một trải nghiệm tư vấn tử vi thông minh và tự nhiên, sử dụng sức mạnh của LLM để hiểu và phản hồi một cách thông minh, giống như một consultant tử vi thực sự.
