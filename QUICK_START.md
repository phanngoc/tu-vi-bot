# 🚀 Quick Start Guide

## ⚡ Cách nhanh nhất để chạy dự án

### 1. Clone và setup
```bash
git clone <repository-url>
cd tu-vi-bot
python setup.py
```

### 2. Thêm API key
Mở file `.env` và thay thế:
```env
OPENAI_API_KEY=your_actual_openai_api_key_here
```

### 3. Chạy dự án
```bash
./start.sh
```

Hoặc chạy riêng lẻ:

**Backend:**
```bash
python app.py
```

**Frontend:**
```bash
cd frontend
npm run dev
```

### 4. Truy cập
- 🌐 **Frontend**: http://localhost:3000
- 🔧 **Backend API**: http://localhost:5000

## 🧪 Test nhanh

```bash
# Test API
curl -X POST http://localhost:5000/api/reply \
  -H "Content-Type: application/json" \
  -d '{"message": "phan ngọc, nam, 05/10/1993, giờ sinh: 14:00", "uuid": "test"}'

# Test Python
python -c "
from chat import prompt_to_predict
result = prompt_to_predict('phan ngọc, nam, 05/10/1993, giờ sinh: 14:00', 'test')
print(result)
"
```

## 🔧 Troubleshooting

### Lỗi thường gặp:

1. **"No module named 'llama_index'"**
   ```bash
   pip install -r requirements.txt
   ```

2. **"Database not found"**
   ```bash
   python -c "from models import Base, engine; Base.metadata.create_all(engine)"
   ```

3. **"OpenAI API key not found"**
   - Kiểm tra file `.env` có đúng API key không
   - Đảm bảo API key có quyền truy cập GPT-4

4. **Frontend không load**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## 📱 Demo Flow

1. Mở http://localhost:3000
2. Gõ: "Xin chào"
3. Gõ: "Tôi tên Nguyễn Văn A, sinh ngày 15/03/1990, 14:30, giới tính Nam"
4. Bot sẽ tự động phân tích tử vi
5. Hỏi thêm: "Công việc của tôi như thế nào?"

## 🎯 Tính năng chính

- ✅ **Intelligent Conversation**: Bot hiểu context và trò chuyện tự nhiên
- ✅ **Smart Extraction**: Tự động trích xuất thông tin từ tin nhắn
- ✅ **Auto Analysis**: Tự động phát hiện khi đủ thông tin và phân tích
- ✅ **Context Memory**: Nhớ thông tin từ cuộc hội thoại trước
- ✅ **SQLite Storage**: Lưu trữ persistent session và chat history

## 📚 Tài liệu chi tiết

- [README.md](./README.md) - Tài liệu đầy đủ
- [Intelligent Conversation Flow](./docs/INTELLIGENT_CONVERSATION_FLOW.md) - Chi tiết về flow
- [Flow Diagram](./docs/FLOW_DIAGRAM.md) - Sơ đồ hệ thống
