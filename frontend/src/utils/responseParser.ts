import { ComprehensiveTuviReading, ParsedResponse } from '@/types/tuvi';

export function parseApiResponse(message: string): ParsedResponse {
  try {
    // Check if message contains structured JSON - improved regex to handle nested objects
    const jsonMatch = message.match(/\{(?:[^{}]|{[^{}]*})*\}/);
    
    if (jsonMatch) {
      const jsonStr = jsonMatch[0];
      
      // Validate JSON string before parsing
      if (!isValidJsonString(jsonStr)) {
        console.warn('Invalid JSON structure detected, falling back to plain text');
        return {
          isStructured: false,
          plainMessage: message
        };
      }
      
      const parsedData = JSON.parse(jsonStr);
      
      // Validate that parsed data matches ComprehensiveTuviReading structure
      if (!isValidTuviReading(parsedData)) {
        console.warn('Parsed JSON does not match expected TuviReading structure');
        return {
          isStructured: false,
          plainMessage: message
        };
      }
      
      const tuviReading = parsedData as ComprehensiveTuviReading;
      
      // Extract follow-up message if present - improved regex
      const followUpMatch = message.match(/\}\s*\n?\s*([\s\S]+?)$/);
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

function isValidJsonString(str: string): boolean {
  try {
    const parsed = JSON.parse(str);
    return typeof parsed === 'object' && parsed !== null;
  } catch {
    return false;
  }
}

function isValidTuviReading(data: unknown): boolean {
  if (!data || typeof data !== 'object' || data === null) return false;
  
  const dataObj = data as Record<string, unknown>;
  
  // Check for required fields
  const requiredFields = ['name', 'birthday', 'birth_time', 'gender', 'basic_destiny'];
  for (const field of requiredFields) {
    if (!dataObj[field] || typeof dataObj[field] !== 'string') {
      return false;
    }
  }
  
  // Check for main_palaces_analysis array
  if (!Array.isArray(dataObj.main_palaces_analysis)) {
    return false;
  }
  
  // Basic validation for palace analysis structure
  for (const palace of dataObj.main_palaces_analysis) {
    if (!palace || typeof palace !== 'object' || palace === null) {
      return false;
    }
    const palaceObj = palace as Record<string, unknown>;
    if (!palaceObj.cung || !palaceObj.summary || !palaceObj.detailed_analysis) {
      return false;
    }
  }
  
  return true;
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