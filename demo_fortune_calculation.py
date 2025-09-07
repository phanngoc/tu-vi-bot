#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo script để test các tính toán vận mệnh mới cho chatbot tử vi
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chat import an_sao_tuvi_comprehensive, demo_fortune_analysis

def test_fortune_calculation():
    """Test các tính toán vận mệnh với nhiều trường hợp khác nhau"""
    
    print("=" * 60)
    print("DEMO TÍNH TOÁN VẬN MỆNH CHO CHATBOT TỬ VI")
    print("=" * 60)
    
    # Test case 1: Nam, sinh 15/8/1990, giờ Ngọ
    print("\n🔸 TEST CASE 1: Nam, sinh 15/8/1990, giờ Ngọ")
    print("-" * 50)
    
    result1 = an_sao_tuvi_comprehensive(
        day=15, month=8, year=1990, hour=6, gender='Nam',
        current_year=2025, current_month=1, current_day=15
    )
    
    print(f"Thông tin cơ bản:")
    print(f"  - Sinh: {result1['basic_info']['birth_info']}")
    print(f"  - Thiên Can: {result1['basic_info']['thien_can']}")
    print(f"  - Địa Chi: {result1['basic_info']['dia_chi']}")
    print(f"  - Cục: {result1['basic_info']['cuc']}")
    print(f"  - Cung Mệnh: {result1['basic_info']['menh_cung']}")
    print(f"  - Tuổi hiện tại: {result1['basic_info']['current_age']}")
    
    print(f"\nVận hạn:")
    print(f"  - Đại vận hiện tại: {result1['analysis']['current_dai_van']}")
    print(f"  - Tiểu vận: {result1['analysis']['tieu_van']['description']}")
    print(f"  - Lưu tháng: {result1['fortune']['luu_thang']['description']}")
    print(f"  - Lưu ngày: {result1['fortune']['luu_ngay']['description']}")
    
    print(f"\nĐiểm 4 trụ chính:")
    for pillar, score in result1['analysis']['four_pillars'].items():
        pillar_name = {
            'cong_viec': 'Công việc',
            'tai_chinh': 'Tài chính', 
            'tinh_cam': 'Tình cảm',
            'suc_khoe': 'Sức khỏe'
        }[pillar]
        print(f"  - {pillar_name}: {score}")
    
    print(f"\nKim chỉ nam: {result1['guidance']['kim_chi_nam']}")
    print(f"Điểm tổng quát: {result1['guidance']['overall_score']}")
    
    print(f"\nKhuyến nghị chi tiết:")
    for rec in result1['guidance']['recommendations']:
        print(f"\n📌 {rec['category']} ({rec['level']} - {rec['score']}):")
        print(f"   {rec['advice']}")
        print(f"   Hành động: {', '.join(rec['actions'])}")
    
    # Test case 2: Nữ, sinh 20/3/1995, giờ Tý
    print("\n\n🔸 TEST CASE 2: Nữ, sinh 20/3/1995, giờ Tý")
    print("-" * 50)
    
    result2 = an_sao_tuvi_comprehensive(
        day=20, month=3, year=1995, hour=0, gender='Nữ',
        current_year=2025, current_month=1, current_day=15
    )
    
    print(f"Thông tin cơ bản:")
    print(f"  - Sinh: {result2['basic_info']['birth_info']}")
    print(f"  - Thiên Can: {result2['basic_info']['thien_can']}")
    print(f"  - Địa Chi: {result2['basic_info']['dia_chi']}")
    print(f"  - Cục: {result2['basic_info']['cuc']}")
    print(f"  - Cung Mệnh: {result2['basic_info']['menh_cung']}")
    print(f"  - Tuổi hiện tại: {result2['basic_info']['current_age']}")
    
    print(f"\nĐiểm 4 trụ chính:")
    for pillar, score in result2['analysis']['four_pillars'].items():
        pillar_name = {
            'cong_viec': 'Công việc',
            'tai_chinh': 'Tài chính', 
            'tinh_cam': 'Tình cảm',
            'suc_khoe': 'Sức khỏe'
        }[pillar]
        print(f"  - {pillar_name}: {score}")
    
    print(f"\nKim chỉ nam: {result2['guidance']['kim_chi_nam']}")
    print(f"Điểm tổng quát: {result2['guidance']['overall_score']}")
    
    # Test case 3: So sánh điểm số các cung
    print("\n\n🔸 TEST CASE 3: So sánh điểm số các cung (Case 1)")
    print("-" * 50)
    
    print("Điểm số chi tiết các cung:")
    for cung_name, score_info in result1['cung_scores'].items():
        print(f"\n{cung_name}:")
        print(f"  - Điểm cơ bản: {score_info['base_score']:.1f}")
        print(f"  - Combo bonus: {score_info['combo_bonus']:.1f}")
        print(f"  - Điểm cuối: {score_info['final_score']:.1f}")
        print(f"  - Điểm chuẩn hóa: {score_info['normalized_score']}")
        print(f"  - Sao: {', '.join([s['sao'] for s in score_info['star_details']])}")
    
    print("\n" + "=" * 60)
    print("KẾT LUẬN: Các tính toán vận mệnh đã được bổ sung thành công!")
    print("Chatbot giờ đây có thể:")
    print("✅ Tính Đại vận (10 năm/cung) với chiều thuận/nghịch")
    print("✅ Tính Tiểu vận (lưu niên) với sao lưu")
    print("✅ Tính Lưu tháng và Lưu ngày")
    print("✅ Scoring các cung dựa trên sao và vị trí miếu/vượng")
    print("✅ Tính combo cát/sát tinh")
    print("✅ Đưa ra khuyến nghị 4 trụ chính")
    print("✅ Tạo kim chỉ nam tổng quát")
    print("=" * 60)

if __name__ == "__main__":
    test_fortune_calculation()
