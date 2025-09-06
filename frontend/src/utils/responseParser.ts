import { ComprehensiveTuviReading, ParsedResponse } from '@/types/tuvi';

export function parseApiResponse(message: string): ParsedResponse {
  try {
    // Check if message contains structured JSON
    const jsonMatch = message.match(/\{[\s\S]*\}/);
    
    if (jsonMatch) {
      const jsonStr = jsonMatch[0];
      const tuviReading = JSON.parse(jsonStr) as ComprehensiveTuviReading;
      
      // Extract follow-up message if present
      const followUpMatch = message.match(/\}\s*([\s\S]+)$/);
      const followUpMessage = followUpMatch ? followUpMatch[1].trim() : undefined;
      
      return {
        isStructured: true,
        tuviReading,
        followUpMessage
      };
    }
  } catch (error) {
    console.warn('Failed to parse JSON from response:', error);
  }
  
  // If no structured data found, return as plain message
  return {
    isStructured: false,
    plainMessage: message
  };
}

export function formatStrength(strength: string): string {
  const strengthMap: Record<string, string> = {
    'Mạnh': '💪 Mạnh',
    'Yếu': '💔 Yếu', 
    'Trung bình': '⚖️ Trung bình'
  };
  
  return strengthMap[strength] || strength;
}

export function formatElement(element: string): string {
  const elementMap: Record<string, string> = {
    'Kim': '⚪ Kim',
    'Mộc': '🟢 Mộc',
    'Thủy': '🔵 Thủy',
    'Hỏa': '🔴 Hỏa',
    'Thổ': '🟡 Thổ'
  };
  
  return elementMap[element] || element;
}

export function formatFortuneTrend(trend: string): string {
  const trendMap: Record<string, string> = {
    'thăng': '📈 Thăng tiến',
    'trầm': '📉 Trầm lắng',
    'ổn định': '➡️ Ổn định',
    'Ổn định': '➡️ Ổn định'
  };
  
  return trendMap[trend] || trend;
}