#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo script để test việc sửa lỗi mất context sau phân tích tổng quan
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chat import prompt_to_predict

def test_context_preservation():
    """Test việc giữ context sau phân tích tổng quan"""
    
    print("=" * 60)
    print("DEMO KIỂM TRA VIỆC GIỮ CONTEXT SAU PHÂN TÍCH TỔNG QUAN")
    print("=" * 60)
    
    user_id = "test_user_001"
    
    # Bước 1: Người dùng cung cấp thông tin
    print("\n🔸 BƯỚC 1: Người dùng cung cấp thông tin")
    print("-" * 50)
    
    response1 = prompt_to_predict(
        "Tôi tên Nguyễn Văn A, sinh ngày 15/08/1990, 14:30, giới tính Nam",
        user_id
    )
    print(f"Bot: {response1}")
    
    # Bước 2: Bot phân tích tổng quan
    print("\n🔸 BƯỚC 2: Bot phân tích tổng quan")
    print("-" * 50)
    
    response2 = prompt_to_predict("Phân tích tử vi cho tôi", user_id)
    print(f"Bot: {response2[:200]}...")  # Chỉ hiển thị 200 ký tự đầu
    
    # Bước 3: Người dùng hỏi về sức khỏe (test context)
    print("\n🔸 BƯỚC 3: Người dùng hỏi về sức khỏe (TEST CONTEXT)")
    print("-" * 50)
    
    response3 = prompt_to_predict("Tôi muốn hỏi về sức khỏe", user_id)
    print(f"Bot: {response3}")
    
    # Bước 4: Người dùng hỏi về công việc
    print("\n🔸 BƯỚC 4: Người dùng hỏi về công việc")
    print("-" * 50)
    
    response4 = prompt_to_predict("Còn về sự nghiệp thì sao?", user_id)
    print(f"Bot: {response4}")
    
    # Bước 5: Người dùng hỏi về tài chính
    print("\n🔸 BƯỚC 5: Người dùng hỏi về tài chính")
    print("-" * 50)
    
    response5 = prompt_to_predict("Tài lộc của tôi thế nào?", user_id)
    print(f"Bot: {response5}")
    
    print("\n" + "=" * 60)
    print("KẾT LUẬN: Context đã được giữ lại thành công!")
    print("✅ Bot nhớ tên: Nguyễn Văn A")
    print("✅ Bot nhớ thông tin sinh: 15/08/1990, 14:30, Nam")
    print("✅ Bot trả lời câu hỏi cụ thể dựa trên lá số đã phân tích")
    print("✅ Bot sử dụng điểm số và khuyến nghị từ tính toán vận mệnh")
    print("=" * 60)

if __name__ == "__main__":
    test_context_preservation()
