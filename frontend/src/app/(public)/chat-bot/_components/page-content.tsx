'use client';

import React, { useState, useEffect } from 'react';
import Human from './human';
import Bot from './bot';
import { v4 as uuidv4 } from 'uuid';

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
  const [sessionId] = useState(() => uuidv4());

  // Initialize conversation on component mount
  useEffect(() => {
    setMessages([
      { 
        type: 'bot', 
        content: '🌙 Chào mừng bạn đến với thế giới bí ẩn của tử vi... \n\nTa là một thầy bói lão luyện, đã dành cả đời nghiên cứu thiên văn và chiêm tinh học. Hãy để ta khám phá vận mệnh và tương lai của bạn.\n\n🔮 Để bắt đầu cuộc hành trình tìm hiểu số phận, hãy nói "Xin chào" hoặc bất kỳ lời gì bạn muốn...',
        stage: 'greeting'
      }
    ]);
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleButtonClick();
    }
  };

  const resetSession = async () => {
    try {
      setIsLoading(true);
      await fetch(HOST_URL + '/api/reset-session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
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

  const detectStageFromContent = (content: string): ConversationStage => {
    if (content.includes('cung cấp thông tin') || content.includes('ngày sinh')) {
      return 'collecting_info';
    } else if (content.includes('phân tích') || content.includes('lập lá số')) {
      return 'analyzing';
    } else if (content.includes('muốn hỏi thêm') || content.includes('khía cạnh')) {
      return 'consulting';
    }
    return currentStage;
  };

  const handleButtonClick = async () => {
    if (inputValue.trim() === '' || isLoading) return;
    
    const userMessage: Message = { type: 'human', content: inputValue };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const res = await fetch(HOST_URL + '/api/reply', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          message: inputValue,
          uuid: sessionId 
        }),
      });
      
      const data = await res.json();
      
      if (data.status === 'success') {
        const newStage = detectStageFromContent(data.message);
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
    <div className="max-w-[900px] h-[calc(100vh-32px)] py-6 bg-gradient-to-br from-mystic-dark/90 to-mystic-purple/80 backdrop-blur-md relative z-10 rounded-xl shadow-2xl flex flex-1 flex-col animate-mystical-glow border border-mystic-gold/20">
      {/* Header with mystical design */}
      <div className="flex items-center justify-between mb-6 px-6">
        <div className="flex items-center space-x-4">
          <div className="animate-constellation text-3xl">🔮</div>
          <div>
            <h1 className="font-bold text-2xl text-mystic-gold animate-divination-shimmer bg-gradient-to-r from-mystic-gold via-mystic-amber to-mystic-gold bg-clip-text text-transparent bg-[length:200%_100%]">
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
            <span className="text-xl animate-wisdom-pulse">{getStageIcon()}</span>
            <div>
              <p className="text-mystic-gold font-medium text-sm">Giai đoạn hiện tại</p>
              <p className="text-mystic-silver">{getStageName()}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto px-6 space-y-4 scrollbar-thin scrollbar-thumb-mystic-gold/30 scrollbar-track-transparent">
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
                <div className="animate-spin text-mystic-gold">🔮</div>
                <p className="text-mystic-silver animate-pulse">Thầy đang suy nghiệm...</p>
              </div>
            </div>
          </div>
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
                onKeyPress={handleKeyPress}
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
              className="bg-gradient-to-r from-fortune-mystery to-fortune-divination text-white px-6 py-3 rounded-lg hover:shadow-lg hover:shadow-mystic-glow/30 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed font-medium animate-float-gentle"
            >
              {isLoading ? '🔮' : '✨ Gửi'}
            </button>
          </div>
          
          {/* Quick suggestions based on stage */}
          {currentStage === 'collecting_info' && (
            <div className="mt-3 flex flex-wrap gap-2">
              <button
                onClick={() => setInputValue('Tôi tên Nguyễn Văn A, sinh ngày 15/03/1990, 14:30, giới tính Nam')}
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
