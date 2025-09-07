"""
Response Generator Component

Component tạo phản hồi cho người dùng, có thể dễ dàng thay thế bằng các template engine khác.
"""

from typing import List
from .interfaces import IResponseGenerator, UserInfo, TuviResult


class ResponseGenerator(IResponseGenerator):
    """Tạo phản hồi cho người dùng"""
    
    def generate_greeting_response(self) -> str:
        """Tạo phản hồi chào hỏi"""
        return """🔮 **Chào mừng bạn đến với dịch vụ tư vấn tử vi thông minh!**

Tôi là trợ lý AI chuyên về tử vi, có thể giúp bạn:
- Phân tích lá số tử vi chi tiết
- Tư vấn về vận mệnh, tình duyên, sự nghiệp
- Dự báo vận hạn và đưa ra lời khuyên

Để bắt đầu, tôi cần biết một số thông tin cơ bản về bạn. Bạn có thể chia sẻ tên, ngày sinh, giờ sinh và giới tính của mình không?

*Ví dụ: "Tôi tên Nguyễn Văn A, sinh ngày 15/03/1990, 14:30, giới tính Nam"*"""
    
    def generate_info_request_response(self, missing_fields: List[str]) -> str:
        """Tạo phản hồi yêu cầu thông tin"""
        if not missing_fields:
            return "✅ **Tuyệt vời! Tôi đã có đủ thông tin để tiến hành phân tích tử vi cho bạn.**"
        
        missing_text = {
            'tên': 'tên',
            'ngày sinh': 'ngày sinh', 
            'giờ sinh': 'giờ sinh',
            'giới tính': 'giới tính'
        }
        
        missing_list = [missing_text[field] for field in missing_fields if field in missing_text]
        
        return f"""📝 **Cảm ơn bạn đã cung cấp thông tin!**

Tôi vẫn cần thêm: **{', '.join(missing_list)}**

Bạn có thể cung cấp thông tin còn thiếu để tôi có thể tiến hành phân tích tử vi chính xác."""
    
    def generate_tuvi_analysis_response(self, user_info: UserInfo, tuvi_result: TuviResult) -> str:
        """Tạo phản hồi phân tích tử vi"""
        analysis = f"""🔮 **Phân tích tử vi cho {user_info.name}**

✨ **Thông tin cơ bản:**
- 📅 Sinh: {user_info.birthday} lúc {user_info.birth_time}
- ⚥ Giới tính: {user_info.gender}
- 🌟 Thiên Can: {tuvi_result.basic_info['thien_can']}
- 🐉 Địa Chi: {tuvi_result.basic_info['dia_chi']}
- ⭐ Cục: {tuvi_result.basic_info['cuc']}
- 🏠 Cung Mệnh: {tuvi_result.basic_info['menh_cung']}
- 🎂 Tuổi hiện tại: {tuvi_result.basic_info['current_age']}

🌌 **Các sao trong 12 cung:**
"""
        
        for cung, sao_list in tuvi_result.sao_cung.items():
            sao_str = ', '.join(sao_list) if sao_list else 'Trống'
            analysis += f"• **{cung}**: {sao_str}\n"
        
        # Thêm thông tin vận hạn
        analysis += f"""

📊 **Điểm 4 trụ chính:**
- 💼 **Công việc**: {tuvi_result.analysis['four_pillars']['cong_viec']}/3
- 💰 **Tài chính**: {tuvi_result.analysis['four_pillars']['tai_chinh']}/3  
- ❤️ **Tình cảm**: {tuvi_result.analysis['four_pillars']['tinh_cam']}/3
- 🏥 **Sức khỏe**: {tuvi_result.analysis['four_pillars']['suc_khoe']}/3

🌟 **Vận hạn hiện tại:**
- 🎯 **Đại vận**: {tuvi_result.analysis['current_dai_van']['cung']} ({tuvi_result.analysis['current_dai_van']['age_range']})
- 📅 **Tiểu vận**: {tuvi_result.analysis['tieu_van']['description']}
- 📈 **Lưu tháng**: {tuvi_result.fortune['luu_thang']['description']}
- 📆 **Lưu ngày**: {tuvi_result.fortune['luu_ngay']['description']}

🎯 **Kim chỉ nam**: {tuvi_result.guidance['kim_chi_nam']}

💫 **Phân tích hoàn tất!** Lá số của {user_info.name} đã được tính toán theo phương pháp tử vi truyền thống với các tính toán vận mệnh nâng cao.

✨ **Bạn có thể hỏi tôi về:**
- Vận mệnh và tính cách tổng quan
- Tình duyên và hôn nhân  
- Sự nghiệp và công danh
- Tài lộc và đầu tư
- Sức khỏe và tuổi thọ
- Mối quan hệ gia đình
- Vận hạn chi tiết theo năm/tháng

💬 *Để bắt đầu phiên tư vấn mới, bạn có thể nói 'Xin chào' hoặc 'Tôi muốn xem tử vi'*"""
        
        return analysis
    
    def generate_consulting_response(self, question: str, user_info: UserInfo, tuvi_result: TuviResult) -> str:
        """Tạo phản hồi tư vấn"""
        # Phân tích loại câu hỏi
        question_lower = question.lower()
        
        if any(keyword in question_lower for keyword in ['sức khỏe', 'sức khoẻ', 'bệnh', 'ốm', 'khỏe']):
            return self._generate_health_advice(user_info, tuvi_result)
        elif any(keyword in question_lower for keyword in ['công việc', 'sự nghiệp', 'nghề', 'làm việc']):
            return self._generate_career_advice(user_info, tuvi_result)
        elif any(keyword in question_lower for keyword in ['tài chính', 'tiền', 'tài lộc', 'đầu tư']):
            return self._generate_finance_advice(user_info, tuvi_result)
        elif any(keyword in question_lower for keyword in ['tình cảm', 'tình yêu', 'hôn nhân', 'gia đình']):
            return self._generate_relationship_advice(user_info, tuvi_result)
        else:
            return self._generate_general_advice(question, user_info, tuvi_result)
    
    def _generate_health_advice(self, user_info: UserInfo, tuvi_result: TuviResult) -> str:
        """Tạo tư vấn sức khỏe"""
        health_score = tuvi_result.analysis['four_pillars']['suc_khoe']
        
        return f"""🏥 **Tư vấn sức khỏe cho {user_info.name}**

📊 **Điểm sức khỏe**: {health_score}/3

💡 **Phân tích tổng quan**: Dựa trên lá số tử vi, sức khỏe của bạn có điểm số {health_score}/3.

🌟 **Vận hạn sức khỏe**:
- Đại vận hiện tại: {tuvi_result.analysis['current_dai_van']['cung']} ({tuvi_result.analysis['current_dai_van']['age_range']})
- Tiểu vận: {tuvi_result.analysis['tieu_van']['description']}

💫 **Khuyến nghị chung**: Hãy duy trì lối sống lành mạnh và kiểm tra sức khỏe định kỳ."""
    
    def _generate_career_advice(self, user_info: UserInfo, tuvi_result: TuviResult) -> str:
        """Tạo tư vấn sự nghiệp"""
        career_score = tuvi_result.analysis['four_pillars']['cong_viec']
        
        return f"""💼 **Tư vấn sự nghiệp cho {user_info.name}**

📊 **Điểm công việc**: {career_score}/3

💡 **Phân tích tổng quan**: Dựa trên lá số tử vi, sự nghiệp của bạn có điểm số {career_score}/3.

🌟 **Vận hạn sự nghiệp**:
- Đại vận hiện tại: {tuvi_result.analysis['current_dai_van']['cung']} ({tuvi_result.analysis['current_dai_van']['age_range']})
- Tiểu vận: {tuvi_result.analysis['tieu_van']['description']}

💫 **Khuyến nghị chung**: Hãy tập trung vào việc phát triển kỹ năng và xây dựng mối quan hệ trong công việc."""
    
    def _generate_finance_advice(self, user_info: UserInfo, tuvi_result: TuviResult) -> str:
        """Tạo tư vấn tài chính"""
        finance_score = tuvi_result.analysis['four_pillars']['tai_chinh']
        
        return f"""💰 **Tư vấn tài chính cho {user_info.name}**

📊 **Điểm tài chính**: {finance_score}/3

💡 **Phân tích tổng quan**: Dựa trên lá số tử vi, tài chính của bạn có điểm số {finance_score}/3.

🌟 **Vận hạn tài chính**:
- Đại vận hiện tại: {tuvi_result.analysis['current_dai_van']['cung']} ({tuvi_result.analysis['current_dai_van']['age_range']})
- Tiểu vận: {tuvi_result.analysis['tieu_van']['description']}

💫 **Khuyến nghị chung**: Hãy quản lý chi tiêu cẩn thận và tìm kiếm cơ hội đầu tư phù hợp."""
    
    def _generate_relationship_advice(self, user_info: UserInfo, tuvi_result: TuviResult) -> str:
        """Tạo tư vấn tình cảm"""
        relationship_score = tuvi_result.analysis['four_pillars']['tinh_cam']
        
        return f"""❤️ **Tư vấn tình cảm cho {user_info.name}**

📊 **Điểm tình cảm**: {relationship_score}/3

💡 **Phân tích tổng quan**: Dựa trên lá số tử vi, tình cảm của bạn có điểm số {relationship_score}/3.

🌟 **Vận hạn tình cảm**:
- Đại vận hiện tại: {tuvi_result.analysis['current_dai_van']['cung']} ({tuvi_result.analysis['current_dai_van']['age_range']})
- Tiểu vận: {tuvi_result.analysis['tieu_van']['description']}

💫 **Khuyến nghị chung**: Hãy tăng cường giao tiếp và xây dựng mối quan hệ bền vững."""
    
    def _generate_general_advice(self, question: str, user_info: UserInfo, tuvi_result: TuviResult) -> str:
        """Tạo tư vấn tổng quát"""
        return f"""💫 **Tư vấn tổng quát cho {user_info.name}**

📝 **Câu hỏi của bạn**: {question}

🔮 **Dựa trên lá số tử vi**:
- Thiên Can: {tuvi_result.basic_info['thien_can']}
- Địa Chi: {tuvi_result.basic_info['dia_chi']}
- Cục: {tuvi_result.basic_info['cuc']}
- Cung Mệnh: {tuvi_result.basic_info['menh_cung']}

🌟 **Vận hạn hiện tại**: {tuvi_result.analysis['current_dai_van']['cung']} ({tuvi_result.analysis['current_dai_van']['age_range']})

💡 **Lời khuyên**: Dựa trên lá số tử vi của bạn, hãy tập trung vào việc phát triển bản thân và tận dụng những cơ hội tốt trong giai đoạn hiện tại."""
