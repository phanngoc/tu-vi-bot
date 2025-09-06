export interface CungAnalysis {
  cung: string;
  stars: string[];
  element_harmony: string;
  strength: string;
  summary: string;
  detailed_analysis: string;
}

export interface LifePeriodAnalysis {
  dai_van: string;
  tieu_han: string;
  fortune_trend: string;
  advice: string;
}

export interface ComprehensiveTuviReading {
  name: string;
  birthday: string;
  birth_time: string;
  gender: string;
  basic_destiny: string;
  main_palaces_analysis: CungAnalysis[];
  family_relationships: string;
  health_fortune: string;
  career_wealth: string;
  current_period: LifePeriodAnalysis;
  annual_forecast: string;
  life_guidance: string;
}

export interface ApiResponse {
  message: string;
  status: 'success' | 'error';
}

export interface ParsedResponse {
  isStructured: boolean;
  tuviReading?: ComprehensiveTuviReading;
  plainMessage?: string;
  followUpMessage?: string;
}