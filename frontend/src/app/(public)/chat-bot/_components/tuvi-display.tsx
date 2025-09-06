import { ComprehensiveTuviReading } from '@/types/tuvi';
import { formatStrength, formatElement, formatFortuneTrend } from '@/utils/responseParser';

interface TuviDisplayProps {
  data: ComprehensiveTuviReading;
}

function TuviDisplay({ data }: TuviDisplayProps) {
  return (
    <div className="space-y-6 text-mystic-silver">
      {/* Header */}
      <div className="bg-gradient-to-r from-fortune-mystery/20 to-fortune-divination/20 backdrop-blur-sm rounded-xl p-4 border border-mystic-gold/30">
        <div className="flex items-center space-x-3 mb-3">
          <span className="text-2xl">🌟</span>
          <div>
            <h3 className="font-bold text-xl text-mystic-gold">Lá số tử vi của {data.name}</h3>
            <p className="text-mystic-silver/70 text-sm">
              {data.birthday} • {data.birth_time} • {data.gender}
            </p>
          </div>
        </div>
        
        <div className="bg-mystic-dark/30 rounded-lg p-3 border border-mystic-gold/20">
          <p className="text-mystic-amber font-medium mb-1">🔮 Căn cơ mệnh chủ:</p>
          <p className="text-mystic-silver leading-relaxed whitespace-pre-line">{data.basic_destiny}</p>
        </div>
      </div>

      {/* Main Palaces Analysis */}
      <div className="bg-gradient-to-r from-fortune-celestial/20 to-fortune-spiritual/20 backdrop-blur-sm rounded-xl p-4 border border-mystic-gold/30">
        <h4 className="font-bold text-lg text-mystic-gold mb-4 flex items-center">
          <span className="mr-2">🏛️</span>
          Phân tích 4 cung chính
        </h4>
        
        <div className="grid gap-4">
          {data.main_palaces_analysis.map((cung, index) => (
            <div key={index} className="bg-mystic-dark/30 rounded-lg p-4 border border-mystic-gold/20">
              <div className="flex items-start justify-between mb-3">
                <h5 className="font-bold text-mystic-amber text-base">{cung.cung}</h5>
                <div className="flex items-center space-x-2 text-xs">
                  <span className="bg-mystic-mist/50 px-2 py-1 rounded-full">
                    {formatElement(cung.element_harmony)}
                  </span>
                  <span className="bg-mystic-mist/50 px-2 py-1 rounded-full">
                    {formatStrength(cung.strength)}
                  </span>
                </div>
              </div>
              
              {cung.stars.length > 0 && (
                <div className="mb-3">
                  <p className="text-xs text-mystic-gold/70 mb-1">Các sao:</p>
                  <div className="flex flex-wrap gap-1">
                    {cung.stars.map((star, starIndex) => (
                      <span key={starIndex} className="text-xs bg-fortune-mystery/30 text-mystic-silver px-2 py-1 rounded-full border border-mystic-gold/20">
                        ⭐ {star}
                      </span>
                    ))}
                  </div>
                </div>
              )}
              
              <p className="text-mystic-silver/90 text-sm mb-2 leading-relaxed whitespace-pre-line">{cung.summary}</p>
              <p className="text-mystic-silver/75 text-xs leading-relaxed whitespace-pre-line">{cung.detailed_analysis}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Life Aspects */}
      <div className="grid md:grid-cols-2 gap-4">
        <div className="bg-gradient-to-br from-fortune-wisdom/20 to-mystic-sage/20 backdrop-blur-sm rounded-xl p-4 border border-mystic-gold/30">
          <h4 className="font-bold text-mystic-gold mb-3 flex items-center">
            <span className="mr-2">👨‍👩‍👧‍👦</span>
            Quan hệ gia đình
          </h4>
          <p className="text-mystic-silver/90 text-sm leading-relaxed whitespace-pre-line">{data.family_relationships}</p>
        </div>

        <div className="bg-gradient-to-br from-fortune-ancient/20 to-mystic-purple/20 backdrop-blur-sm rounded-xl p-4 border border-mystic-gold/30">
          <h4 className="font-bold text-mystic-gold mb-3 flex items-center">
            <span className="mr-2">🌿</span>
            Sức khỏe & Phúc đức
          </h4>
          <p className="text-mystic-silver/90 text-sm leading-relaxed whitespace-pre-line">{data.health_fortune}</p>
        </div>
      </div>

      {/* Career & Wealth */}
      <div className="bg-gradient-to-r from-fortune-divination/20 to-fortune-mystery/20 backdrop-blur-sm rounded-xl p-4 border border-mystic-gold/30">
        <h4 className="font-bold text-mystic-gold mb-3 flex items-center">
          <span className="mr-2">💼</span>
          Sự nghiệp & Tài chính
        </h4>
        <p className="text-mystic-silver/90 text-sm leading-relaxed whitespace-pre-line">{data.career_wealth}</p>
      </div>

      {/* Current Period */}
      <div className="bg-gradient-to-r from-fortune-celestial/20 to-fortune-spiritual/20 backdrop-blur-sm rounded-xl p-4 border border-mystic-gold/30">
        <h4 className="font-bold text-mystic-gold mb-4 flex items-center">
          <span className="mr-2">⏰</span>
          Vận hạn hiện tại
        </h4>
        
        <div className="grid md:grid-cols-2 gap-4">
          <div className="bg-mystic-dark/30 rounded-lg p-3 border border-mystic-gold/20">
            <div className="flex items-center justify-between mb-2">
              <span className="text-mystic-amber text-sm font-medium">Đại vận:</span>
              <span className="text-mystic-silver text-sm">{data.current_period.dai_van}</span>
            </div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-mystic-amber text-sm font-medium">Tiểu hạn:</span>
              <span className="text-mystic-silver text-sm">{data.current_period.tieu_han}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-mystic-amber text-sm font-medium">Xu hướng:</span>
              <span className="text-mystic-silver text-sm">{formatFortuneTrend(data.current_period.fortune_trend)}</span>
            </div>
          </div>
          
          <div className="bg-mystic-dark/30 rounded-lg p-3 border border-mystic-gold/20">
            <p className="text-xs text-mystic-gold/70 mb-2">Lời khuyên:</p>
            <p className="text-mystic-silver/90 text-sm leading-relaxed whitespace-pre-line">{data.current_period.advice}</p>
          </div>
        </div>
      </div>

      {/* Annual Forecast */}
      <div className="bg-gradient-to-r from-mystic-cosmic/20 to-fortune-mystery/20 backdrop-blur-sm rounded-xl p-4 border border-mystic-gold/30">
        <h4 className="font-bold text-mystic-gold mb-3 flex items-center">
          <span className="mr-2">📅</span>
          Dự báo năm hiện tại
        </h4>
        <p className="text-mystic-silver/90 text-sm leading-relaxed whitespace-pre-line">{data.annual_forecast}</p>
      </div>

      {/* Life Guidance */}
      <div className="bg-gradient-to-r from-fortune-wisdom/20 to-fortune-ancient/20 backdrop-blur-sm rounded-xl p-4 border border-mystic-gold/30">
        <h4 className="font-bold text-mystic-gold mb-3 flex items-center">
          <span className="mr-2">🌟</span>
          Hướng dẫn cuộc sống
        </h4>
        <p className="text-mystic-silver/90 text-sm leading-relaxed font-medium whitespace-pre-line">{data.life_guidance}</p>
      </div>
    </div>
  );
}

export default TuviDisplay;