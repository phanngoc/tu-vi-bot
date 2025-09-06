# Enhanced Tu Vi Chatbot Flow Documentation

## Overview
The chatbot has been redesigned to follow traditional Vietnamese astrology (Tử Vi) methodology with a comprehensive consultation process that collects complete birth information and provides systematic fortune analysis.

## New Architecture

### 1. Conversation Stages
The chatbot now operates through 4 distinct stages:

```python
class ConversationStage(Enum):
    GREETING = "greeting"           # Welcome and introduction
    COLLECTING_INFO = "collecting_info"  # Gather birth data
    ANALYZING = "analyzing"         # Calculate star chart
    CONSULTING = "consulting"       # Provide readings
```

### 2. Enhanced Data Collection

#### Required Information:
- **Name** (Họ tên)
- **Birth Date** (Ngày sinh - DD/MM/YYYY)
- **Birth Time** (Giờ sinh - HH:MM) - Critical for palace positioning
- **Gender** (Giới tính - Nam/Nữ) - Affects cycle calculations

#### Validation:
- All fields are required before analysis can proceed
- Smart prompting for missing information
- Format validation for dates and times

### 3. Comprehensive Star System

#### Core Enhancements:
1. **14 Major Stars** (Chính Tinh) - Dynamic positioning based on birth data
2. **Auspicious Stars** (Cát Tinh) - Tả Hữu, Khôi Việt, Xương Khúc
3. **Inauspicious Stars** (Sát Tinh) - Kình Dương, Đà La, Không Kiếp
4. **Four Transformation Stars** (Tứ Hóa) - Based on Thiên Can
5. **Life Cycle Analysis** (Tràng Sinh) - Gender and element specific

#### Key Functions:
```python
# Palace position determination
determine_menh_cung_position(hour, month) -> str

# Life cycle based on element and gender  
get_trang_sinh_cycle(element, gender) -> List[str]

# Four transformation stars by celestial stem
get_tu_hoa_stars(thien_can) -> Dict[str, str]

# Comprehensive star placement
an_sao_tuvi_comprehensive(day, month, year, hour, gender) -> Dict
```

### 4. Traditional Methodology Integration

#### Analysis Framework:
1. **Basic Destiny** (Căn cơ mệnh chủ) - Core personality and nature
2. **Palace Relationships** (Quan hệ các cung) - 12 life aspects
3. **Element Harmony** (Tương sinh tương khắc) - Element interactions
4. **Major Periods** (Đại vận) - 10-year fortune cycles  
5. **Annual Forecast** (Tiểu hạn) - Yearly predictions
6. **Comprehensive Guidance** - Life advice and recommendations

#### 12 Palace System:
- **Mệnh** (Self) - Core personality, destiny
- **Phụ Mẫu** (Parents) - Family relationships
- **Phúc Đức** (Fortune) - Luck and blessings
- **Điền Trạch** (Property) - Real estate, home
- **Quan Lộc** (Career) - Professional life
- **Nô Bộc** (Servants/Friends) - Social relationships
- **Thiên Di** (Migration) - Travel, relocation
- **Tật Ách** (Health) - Physical wellbeing
- **Tài Bạch** (Wealth) - Financial fortune
- **Tử Tức** (Children) - Offspring, creativity
- **Phu Thê** (Spouse) - Marriage, partnerships
- **Huynh Đệ** (Siblings) - Brothers, sisters

## API Enhancements

### New Endpoints:

#### `/api/reset-session` (POST)
Resets the conversation session for new consultations:
```json
{
  "message": "Session đã được reset. Bạn có thể bắt đầu tư vấn mới.",
  "status": "success"
}
```

#### `/api/health` (GET)
Health check endpoint:
```json
{
  "status": "healthy", 
  "service": "Tu Vi Bot API"
}
```

#### Enhanced `/api/reply` (POST)
Now includes error handling and session management:
```json
// Request
{
  "message": "User message",
  "uuid": "optional_user_id"
}

// Response
{
  "message": "Bot response",
  "status": "success|error"
}
```

## Conversation Flow Example

### Stage 1: Greeting
```
User: "Xin chào"

Bot: "Chào mừng bạn đến với dịch vụ tư vấn tử vi!

Để có thể lập lá số chính xác và tư vấn vận mệnh, tôi cần bạn cung cấp:
1. **Họ tên** của bạn
2. **Ngày sinh** (DD/MM/YYYY) 
3. **Giờ sinh** chính xác (HH:MM) - rất quan trọng cho việc xác định cung Mệnh
4. **Giới tính** (Nam/Nữ) - ảnh hưởng đến cách an sao và luận vận

Ví dụ: 'Tôi tên Nguyễn Văn A, sinh ngày 15/03/1990, 14:30, giới tính Nam'

Bạn có thể cung cấp thông tin này không?"
```

### Stage 2: Information Collection
```
User: "Tôi tên Nguyễn Văn A, sinh ngày 15/03/1990, 14:30, giới tính Nam"

Bot: "Cảm ơn Nguyễn Văn A! Tôi đã ghi nhận thông tin:
- Ngày sinh: 15/03/1990  
- Giờ sinh: 14:30
- Giới tính: Nam

Đang tiến hành lập lá số và phân tích vận mệnh... ⏳"
```

### Stage 3: Analysis & Results
```
Bot: "[Comprehensive fortune analysis based on calculated star chart]

💬 **Bạn có muốn hỏi thêm về khía cạnh nào khác không?** 
(sự nghiệp, tình cảm, sức khỏe, tài chính, gia đình...)"
```

### Stage 4: Ongoing Consultation
```
User: "Tôi muốn hỏi về sự nghiệp"

Bot: "[Detailed career analysis based on 官禄宫 and related palaces]"
```

## Testing Results

### Core Logic Tests ✅
- **Thiên Can Địa Chi calculation**: Verified for multiple years
- **Element (Cục) determination**: All 5 elements tested
- **Palace positioning**: Accurate Mệnh Cung placement
- **Life cycles**: Gender-specific Tràng Sinh sequences
- **Transformation stars**: Complete Tứ Hóa mapping
- **Edge cases**: Proper handling of invalid inputs

### Integration Features ✅
- **Session management**: Multi-stage conversation flow
- **Data validation**: Complete birth information required
- **Error handling**: Graceful failure and user guidance
- **API endpoints**: Enhanced with proper status codes

## Key Improvements

### 1. **Authentic Methodology**
- Follows traditional Tử Vi calculation methods
- Comprehensive 14 major stars system
- Gender-specific life cycle analysis
- Four transformation stars by celestial stem

### 2. **User Experience**
- Guided information collection
- Clear stage progression
- Intelligent validation and prompting
- Session reset capability

### 3. **Technical Architecture**
- Stateful conversation management
- Modular function design
- Comprehensive error handling
- Scalable data models

### 4. **Cultural Accuracy**
- Vietnamese terminology throughout
- Traditional calculation methods
- Proper palace relationships
- Element harmony analysis

## Usage Instructions

### For Users:
1. Start with any greeting message
2. Provide complete birth information when prompted
3. Wait for comprehensive analysis
4. Ask specific questions about life aspects

### For Developers:
1. Install dependencies: `pip install -r requirements.txt`
2. Start Flask app: `python app.py`
3. Use `/api/reset-session` to clear user sessions
4. Monitor with `/api/health` endpoint

### Frontend Integration:
- Add reset session button for new consultations
- Implement step-by-step information collection UI
- Display analysis results in structured format
- Enable follow-up question functionality

## Next Steps

1. **Enhanced UI**: Update frontend to match new flow
2. **Data Persistence**: Save user charts for reference
3. **Advanced Features**: 
   - Fortune period calculations
   - Compatibility analysis
   - Lucky date selection
4. **Performance**: Optimize star calculations
5. **Multilingual**: Support for English translations

The enhanced chatbot now provides a professional, comprehensive Vietnamese astrology consultation experience that follows traditional methodology while maintaining modern usability.