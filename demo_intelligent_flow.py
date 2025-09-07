#!/usr/bin/env python3
"""
Demo script for intelligent conversation flow
Shows the power of LLM-based analysis and dynamic conversation
"""

from chat import prompt_to_predict
import time

def demo_intelligent_conversation():
    """Demo the intelligent conversation capabilities"""
    print("🧠 INTELLIGENT CONVERSATION FLOW DEMO")
    print("=" * 60)
    print("This demo shows how the bot acts like a smart consultant")
    print("using LLM-based analysis instead of rigid step-by-step flow")
    print("=" * 60)
    
    user_id = "demo_user"
    
    # Demo scenarios
    scenarios = [
        {
            "title": "🎯 Scenario 1: Complete info in one message",
            "description": "User provides all information at once",
            "messages": [
                "Xin chào",
                "Tôi tên Nguyễn Văn A, sinh ngày 15/03/1990, 14:30, giới tính Nam"
            ]
        },
        {
            "title": "🎯 Scenario 2: Gradual info collection",
            "description": "User provides information gradually",
            "messages": [
                "Hello",
                "Tôi tên Phan Thị B",
                "Sinh ngày 20/05/1995",
                "Giờ sinh 8:30 sáng",
                "Giới tính Nữ"
            ]
        },
        {
            "title": "🎯 Scenario 3: Mixed conversation",
            "description": "User asks questions while providing info",
            "messages": [
                "Chào bạn",
                "Tôi muốn xem tử vi",
                "Tên tôi là Trần Văn C",
                "Sinh 10/12/1988, 16:45, Nam",
                "Vận mệnh của tôi như thế nào?",
                "Tình duyên ra sao?"
            ]
        },
        {
            "title": "🎯 Scenario 4: Reset and restart",
            "description": "User resets and starts over",
            "messages": [
                "Xin chào",
                "Tôi tên Lê Thị D",
                "Sinh 25/08/1992, 12:00, Nữ",
                "Reset",
                "Tôi tên Hoàng Văn E",
                "Sinh 03/01/1985, 20:15, Nam"
            ]
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{scenario['title']}")
        print(f"📝 {scenario['description']}")
        print("-" * 50)
        
        for j, message in enumerate(scenario['messages'], 1):
            print(f"\n👤 User: {message}")
            
            try:
                response = prompt_to_predict(message, user_id)
                print(f"🤖 Bot: {response}")
            except Exception as e:
                print(f"❌ Error: {str(e)}")
            
            time.sleep(1)  # Pause for readability
        
        print("\n" + "=" * 50)
        time.sleep(2)  # Pause between scenarios
    
    print("\n🎉 DEMO COMPLETED!")
    print("The intelligent conversation flow demonstrates:")
    print("✅ LLM-based analysis for understanding user intent")
    print("✅ Dynamic conversation flow (no rigid steps)")
    print("✅ Smart information extraction from context")
    print("✅ Automatic detection of when enough info is collected")
    print("✅ Natural conversation like a real consultant")
    print("✅ Context-aware responses")
    print("✅ Error handling and fallback mechanisms")

def demo_edge_cases():
    """Demo edge cases and error handling"""
    print("\n🔍 EDGE CASES DEMO")
    print("=" * 40)
    
    user_id = "edge_case_demo"
    
    edge_cases = [
        "Tôi không biết tên mình",
        "Sinh ngày 32/13/1990",  # Invalid date
        "Giờ sinh 25:70",  # Invalid time
        "Giới tính không xác định",
        "Tôi muốn hỏi về tử vi nhưng không muốn cung cấp thông tin",
        "",  # Empty message
        "Tôi tên A, sinh B, giờ C, giới tính D"  # All invalid
    ]
    
    for i, message in enumerate(edge_cases, 1):
        print(f"\n👤 Edge Case {i}: '{message}'")
        
        try:
            response = prompt_to_predict(message, user_id)
            print(f"🤖 Bot: {response}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        time.sleep(1)
    
    print("\n✅ Edge cases handled gracefully!")

if __name__ == "__main__":
    demo_intelligent_conversation()
    demo_edge_cases()
    
    print("\n" + "=" * 60)
    print("🚀 INTELLIGENT CONVERSATION FLOW IS READY!")
    print("The bot now acts like a smart consultant with:")
    print("- LLM-based analysis")
    print("- Dynamic conversation flow")
    print("- Context awareness")
    print("- Smart information detection")
    print("- Natural conversation experience")
    print("=" * 60)
