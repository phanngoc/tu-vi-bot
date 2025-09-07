'use client';

import React, { useState, useEffect } from 'react';
import Human from './human';
import Bot from './bot';
import { parseApiResponse } from '@/utils/responseParser';
import type { ParsedResponse } from '@/types/tuvi';
import { getUserId, hasExistingSession, clearUserId } from '@/utils/userSession';

const HOST_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:5000';

type ConversationStage = 'greeting' | 'collecting_info' | 'analyzing' | 'consulting';

interface Message {
  type: 'human' | 'bot';
  content: string;
  stage?: ConversationStage;
  isLoading?: boolean;
}

function PageContent() {
  const [inputValue, setInputValue] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentStage, setCurrentStage] = useState<ConversationStage>('greeting');
  const [isLoading, setIsLoading] = useState(false);
  const [userId] = useState(() => getUserId());
  const [isInitialLoading, setIsInitialLoading] = useState(true);

  // Load chat history or initialize conversation on component mount
  useEffect(() => {
    const initializeChat = async () => {
      setIsInitialLoading(true);
      
      // Check if user has existing session and try to load history
      if (hasExistingSession()) {
        try {
          const res = await fetch(`${HOST_URL}/api/chat-history?user_id=${userId}`);
          const data = await res.json();
          
          if (data.status === 'success' && data.messages && data.messages.length > 0) {
            // Load existing chat history
            setMessages(data.messages);
            
            // Set current stage based on last message
            const lastMessage = data.messages[data.messages.length - 1];
            if (lastMessage.stage) {
              setCurrentStage(lastMessage.stage);
            } else {
              // Determine stage from last bot message content
              const lastBotMessage = data.messages.reverse().find((m: Message) => m.type === 'bot');
              if (lastBotMessage) {
                const detectedStage = detectStageFromContent(lastBotMessage.content);
                setCurrentStage(detectedStage);
              }
            }
          } else {
            // No existing history, show welcome message
            showWelcomeMessage();
          }
        } catch (error) {
          console.error('Error loading chat history:', error);
          // Fallback to welcome message
          showWelcomeMessage();
        }
      } else {
        // New user, show welcome message
        showWelcomeMessage();
      }
      
      setIsInitialLoading(false);
    };

    const showWelcomeMessage = () => {
      setMessages([
        { 
          type: 'bot', 
          content: '🌙 Chào mừng bạn đến với thế giới bí ẩn của tử vi... \n\nTa là một thầy bói lão luyện, đã dành cả đời nghiên cứu thiên văn và chiêm tinh học. Hãy để ta khám phá vận mệnh và tương lai của bạn.\n\n🔮 Để bắt đầu cuộc hành trình tìm hiểu số phận, hãy nói "Xin chào" hoặc bất kỳ lời gì bạn muốn...',
          stage: 'greeting'
        }
      ]);
      setCurrentStage('greeting');
    };

    initializeChat();
  }, [userId]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleButtonClick();
    }
  };

  const resetSession = async () => {
    try {
      setIsLoading(true);
      
      // Clear localStorage user ID
      clearUserId();
      
      // Reset local state
      setMessages([
        { 
          type: 'bot', 
          content: '🌙 Ta sẵn sàng cho một cuộc tư vấn mới. Hãy bắt đầu bằng cách chào hỏi...',
          stage: 'greeting'
        }
      ]);
      setCurrentStage('greeting');
      setInputValue('');
    } catch (error) {
      console.error('Error resetting session:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const detectStageFromContent = (content: string, parsedResponse?: ParsedResponse): ConversationStage => {
    // Check if this is a structured response first
    if (parsedResponse?.isStructured && parsedResponse.tuviReading) {
      // If we have a complete TuviReading, we're in consulting stage
      return 'consulting';
    }
    
    // Content-based stage detection with more keywords
    const lowerContent = content.toLowerCase();
    
    // Collecting info stage keywords
    if (lowerContent.includes('cung cấp thông tin') || 
        lowerContent.includes('ngày sinh') ||
        lowerContent.includes('họ tên') ||
        lowerContent.includes('giờ sinh') ||
        lowerContent.includes('giới tính') ||
        lowerContent.includes('ví dụ:') ||
        lowerContent.includes('vui lòng cung cấp')) {
      return 'collecting_info';
    }
    
    // Analysis stage keywords
    if (lowerContent.includes('phân tích') || 
        lowerContent.includes('lập lá số') ||
        lowerContent.includes('đang phân tích') ||
        lowerContent.includes('tôi đã ghi nhận thông tin') ||
        lowerContent.includes('cảm ơn') && lowerContent.includes('thông tin')) {
      return 'analyzing';
    }
    
    // Consulting stage keywords
    if (lowerContent.includes('muốn hỏi thêm') || 
        lowerContent.includes('khía cạnh') ||
        lowerContent.includes('sự nghiệp') ||
        lowerContent.includes('tình cảm') ||
        lowerContent.includes('sức khỏe') ||
        lowerContent.includes('tài chính') ||
        lowerContent.includes('gia đình') ||
        content.includes('💬')) {
      return 'consulting';
    }
    
    // Fallback: if no clear indicators, keep current stage
    return currentStage;
  };

  const handleButtonClick = async () => {
    if (inputValue.trim() === '' || isLoading) return;
    
    const userMessage: Message = { type: 'human', content: inputValue };
    setMessages(prev => [...prev, userMessage]);
    
    // Check for greeting "Xin chào" and provide immediate guide message
    const lowerInput = inputValue.trim().toLowerCase();
    const isGreeting = lowerInput === 'xin chào' || lowerInput === 'chào' || lowerInput === 'xin chao' || lowerInput === 'chao';
    
    setInputValue('');
    setIsLoading(true);

    if (isGreeting && currentStage === 'greeting') {
      // Provide immediate guide message for greeting
      setTimeout(() => {
        const guideMessage: Message = {
          type: 'bot',
          content: '🌟 Chào mừng bạn đã bước vào cõi huyền bí của tử vi! \n\n🔮 Ta là Thầy Tử Vi, người đã dành trọn đời nghiên cứu về thiên văn và chiêm tinh học. Để có thể nhìn thấu vận mệnh và khám phá tương lai của bạn, ta cần bạn cung cấp những thông tin thiêng liêng sau:\n\n✨ **Họ và tên đầy đủ** - để định danh linh hồn\n📅 **Ngày tháng năm sinh** (âm lịch hoặc dương lịch) - để xác định vị trí các vì sao\n🌙 **Giờ sinh chính xác** - để lập được lá số chuẩn nhất  \n👤 **Giới tính** - để hiểu rõ âm dương ngũ hành\n\n💫 **Ví dụ:** "Tôi tên Nguyễn Văn Nam, sinh ngày 15 tháng 3 năm 1990, lúc 14 giờ 30 phút, giới tính Nam"\n\n🪬 Hãy chia sẻ thông tin của bạn, và ta sẽ mở ra những bí ẩn về số phận mà bạn chưa từng biết...',
          stage: 'collecting_info'
        };
        setMessages(prev => [...prev, guideMessage]);
        setCurrentStage('collecting_info');
        setIsLoading(false);
      }, 1500); // Add slight delay for mystical effect
      return;
    }

    try {
      const res = await fetch(HOST_URL + '/api/reply', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          message: inputValue,
          uuid: userId 
        }),
      });
      
      const data = await res.json();
      
      if (data.status === 'success') {
        // Parse the response to check if it's structured
        const parsedResponse = parseApiResponse(data.message);
        const newStage = detectStageFromContent(data.message, parsedResponse);
        setCurrentStage(newStage);
        
        const botMessage: Message = {
          type: 'bot',
          content: data.message,
          stage: newStage
        };
        
        setMessages(prev => [...prev, botMessage]);
      } else {
        setMessages(prev => [...prev, {
          type: 'bot',
          content: '🌫️ Có vẻ như các vì tinh không thuận lợi... Hãy thử lại nhé.',
          stage: currentStage
        }]);
      }

    } catch (error) {
      console.error('Error fetching the horoscope:', error);
      setMessages(prev => [...prev, {
        type: 'bot',
        content: '🌫️ Kết nối với thế giới tâm linh gặp trở ngại. Xin hãy kiên nhẫn và thử lại...',
        stage: currentStage
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const getStageIcon = () => {
    switch (currentStage) {
      case 'greeting': return '🌙';
      case 'collecting_info': return '📋';
      case 'analyzing': return '🔮';
      case 'consulting': return '🌟';
      default: return '🔮';
    }
  };

  const getStageName = () => {
    switch (currentStage) {
      case 'greeting': return 'Khởi Đầu';
      case 'collecting_info': return 'Thu Thập Thông Tin';
      case 'analyzing': return 'Phân Tích Vận Mệnh';
      case 'consulting': return 'Tư Vấn Chi Tiết';
      default: return 'Bí Ẩn';
    }
  };

  return (
    <div className="max-w-[900px] h-[calc(100vh-32px)] py-6 bg-gradient-to-br from-mystic-dark/90 to-mystic-purple/80 backdrop-blur-md relative z-10 rounded-xl shadow-2xl flex flex-1 flex-col border border-mystic-gold/20">
      {/* Header with mystical design */}
      <div className="flex items-center justify-between mb-6 px-6">
        <div className="flex items-center space-x-4">
          <div className="text-3xl">🔮</div>
          <div>
            <h1 className="font-bold text-2xl text-mystic-gold">
              Thầy Tử Vi Bí Ẩn
            </h1>
            <p className="text-mystic-silver/70 text-sm">Khám phá vận mệnh và tương lai</p>
          </div>
        </div>
        
        <button
          onClick={resetSession}
          disabled={isLoading}
          className="bg-fortune-mystery/20 hover:bg-fortune-mystery/30 text-mystic-silver border border-mystic-gold/30 px-4 py-2 rounded-lg transition-all duration-300 hover:shadow-lg hover:shadow-mystic-gold/20 disabled:opacity-50"
        >
          🌀 Tư vấn mới
        </button>
      </div>

      {/* Current Stage Indicator */}
      <div className="px-6 mb-4">
        <div className="bg-mystic-mist rounded-lg p-3 border border-mystic-gold/20">
          <div className="flex items-center space-x-3">
            <span className="text-xl">{getStageIcon()}</span>
            <div>
              <p className="text-mystic-gold font-medium text-sm">Giai đoạn hiện tại</p>
              <p className="text-mystic-silver">{getStageName()}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto px-6 space-y-4 scrollbar-thin scrollbar-thumb-mystic-gold/30 scrollbar-track-transparent">
        {/* Initial loading indicator */}
        {isInitialLoading ? (
          <div className="flex justify-center items-center h-full">
            <div className="bg-mystic-cosmic/40 backdrop-blur-sm rounded-lg p-6 border border-mystic-gold/20">
              <div className="flex items-center space-x-3">
                <div className="text-mystic-gold animate-spin text-2xl">🔮</div>
                <p className="text-mystic-silver">Đang tải lịch sử trò chuyện...</p>
              </div>
            </div>
          </div>
        ) : (
          <>
            {messages.map((msg, index) =>
              msg.type === 'human' ? (
                <Human key={index} content={msg.content} />
              ) : (
                <Bot key={index} content={msg.content} stage={msg.stage} />
              )
            )}
            
            {/* Loading indicator */}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-mystic-cosmic/40 backdrop-blur-sm rounded-lg p-4 border border-mystic-gold/20">
                  <div className="flex items-center space-x-3">
                    <div className="text-mystic-gold">🔮</div>
                    <p className="text-mystic-silver">Thầy đang suy nghiệm...</p>
                  </div>
                </div>
              </div>
            )}
          </>
        )}
      </div>

      {/* Input Section */}
      <div className="mt-6 px-6">
        <div className="bg-gradient-to-r from-mystic-cosmic/30 to-fortune-ancient/30 backdrop-blur-sm rounded-xl p-4 border border-mystic-gold/30">
          <div className="flex items-center space-x-3">
            <div className="flex-1 relative">
              <input
                type="text"
                placeholder={
                  currentStage === 'greeting' ? '👋 Hãy chào hỏi để bắt đầu...' :
                  currentStage === 'collecting_info' ? '📝 Cung cấp thông tin sinh của bạn...' :
                  currentStage === 'analyzing' ? '⏳ Đang phân tích, vui lòng đợi...' :
                  '💬 Hỏi về sự nghiệp, tình cảm, sức khỏe...'
                }
                className="w-full bg-mystic-dark/50 border border-mystic-gold/20 text-mystic-silver placeholder-mystic-silver/50 p-3 rounded-lg outline-none focus:border-mystic-gold/50 focus:ring-2 focus:ring-mystic-gold/20 transition-all duration-300"
                value={inputValue}
                onChange={handleInputChange}
                onKeyDown={handleKeyDown}
                disabled={isLoading}
              />
              <div className="absolute right-3 top-1/2 transform -translate-y-1/2 text-mystic-gold/50">
                {currentStage === 'greeting' && '🌙'}
                {currentStage === 'collecting_info' && '📋'}
                {currentStage === 'analyzing' && '🔮'}
                {currentStage === 'consulting' && '🌟'}
              </div>
            </div>
            
            <button
              onClick={handleButtonClick}
              disabled={isLoading || !inputValue.trim()}
              className="bg-gradient-to-r from-fortune-mystery to-fortune-divination text-white px-6 py-3 rounded-lg hover:shadow-lg hover:shadow-mystic-glow/30 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
            >
              {isLoading ? '🔮' : '✨ Gửi'}
            </button>
          </div>
          
          {/* Quick suggestions based on stage */}
          {currentStage === 'collecting_info' && (
            <div className="mt-3 flex flex-wrap gap-2">
              <button
                onClick={() => setInputValue('Tôi tên Nguyễn Văn Nam, sinh ngày 15 tháng 3 năm 1990, lúc 14 giờ 30 phút, giới tính Nam')}
                className="text-xs bg-mystic-mist/50 text-mystic-silver px-3 py-1 rounded-full hover:bg-mystic-mist/70 transition-all duration-300"
              >
                💡 Ví dụ thông tin
              </button>
            </div>
          )}
          
          {currentStage === 'consulting' && (
            <div className="mt-3 flex flex-wrap gap-2">
              {['Sự nghiệp', 'Tình cảm', 'Sức khỏe', 'Tài chính'].map((topic) => (
                <button
                  key={topic}
                  onClick={() => setInputValue(`Tôi muốn hỏi về ${topic.toLowerCase()}`)}
                  className="text-xs bg-mystic-mist/50 text-mystic-silver px-3 py-1 rounded-full hover:bg-mystic-mist/70 transition-all duration-300"
                >
                  {topic}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default PageContent;
