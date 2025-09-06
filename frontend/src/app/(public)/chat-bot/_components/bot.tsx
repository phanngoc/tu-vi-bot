import TuviDisplay from './tuvi-display';
import { parseApiResponse } from '@/utils/responseParser';

interface BotProps {
  content: string;
  stage?: 'greeting' | 'collecting_info' | 'analyzing' | 'consulting';
}

function Bot({ content, stage }: BotProps) {
  const parsedResponse = parseApiResponse(content);
  const getStageStyle = () => {
    switch (stage) {
      case 'greeting':
        return 'border-mystic-gold/30 bg-gradient-to-br from-mystic-cosmic/30 to-fortune-mystery/20';
      case 'collecting_info':
        return 'border-fortune-wisdom/30 bg-gradient-to-br from-fortune-wisdom/20 to-mystic-sage/20';
      case 'analyzing':
        return 'border-fortune-divination/30 bg-gradient-to-br from-fortune-divination/20 to-mystic-purple/30';
      case 'consulting':
        return 'border-fortune-celestial/30 bg-gradient-to-br from-fortune-celestial/20 to-fortune-spiritual/20';
      default:
        return 'border-mystic-gold/30 bg-gradient-to-br from-mystic-cosmic/30 to-fortune-mystery/20';
    }
  };

  const getAvatar = () => {
    switch (stage) {
      case 'greeting': return '🌙';
      case 'collecting_info': return '📜';
      case 'analyzing': return '🔮';
      case 'consulting': return '🌟';
      default: return '🔮';
    }
  };

  const formatContent = (text: string) => {
    // Split by newlines and filter empty lines
    const lines = text.split('\n').filter(line => line.trim());
    
    return lines.map((line, index) => {
      const trimmedLine = line.trim();
      
      // Handle emoji-prefixed lines with broader emoji detection
      if (trimmedLine.match(/^[\uD800-\uDBFF][\uDC00-\uDFFF]|[\u2600-\u26FF]|[\u2700-\u27BF]/) || 
          trimmedLine.match(/^[🌙🔮💬⏳📝👋✨🌟📋🌫️📅🌿👨‍👩‍👧‍👦💼⚪🟢🔵🔴🟡📈📉➡️💪💔⚖️]/)) {
        return (
          <p key={index} className="mb-3 text-mystic-silver leading-relaxed font-medium">
            {trimmedLine}
          </p>
        );
      }
      
      // Regular paragraphs
      return (
        <p key={index} className="mb-2 text-mystic-silver/90 leading-relaxed">
          {formatTextWithMarkdown(trimmedLine)}
        </p>
      );
    });
  };

  const formatTextWithMarkdown = (text: string) => {
    // Split text by bold markers while preserving the markers for processing
    const parts = text.split(/(\*\*[^*]+\*\*)/g);
    
    return parts.map((part, index) => {
      if (part.match(/^\*\*.*\*\*$/)) {
        // Bold text - remove markers and apply styling
        const content = part.replace(/\*\*/g, '');
        return (
          <strong key={index} className="text-mystic-gold font-bold">
            {content}
          </strong>
        );
      }
      return part;
    });
  };

  return (
    <div className="flex items-start space-x-3">
      {/* Mystical Avatar */}
      <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center text-lg border ${getStageStyle()}`}>
        {getAvatar()}
      </div>
      
      {/* Message Content */}
      <div className={`${parsedResponse.isStructured ? 'max-w-[95%]' : 'max-w-[75%]'} p-4 rounded-xl border backdrop-blur-sm ${getStageStyle()}`}>
        {parsedResponse.isStructured && parsedResponse.tuviReading ? (
          // Display structured Tu Vi reading
          <div className="space-y-4">
            <TuviDisplay data={parsedResponse.tuviReading} />
          </div>
        ) : (
          // Display plain text message
          <div className="prose prose-sm max-w-none">
            {formatContent(parsedResponse.plainMessage || content)}
          </div>
        )}
        
        {/* Mystical decoration for analysis stage */}
        {stage === 'analyzing' && !parsedResponse.isStructured && (
          <div className="mt-3 flex justify-center">
            <div className="flex space-x-2">
              <div className="w-2 h-2 bg-fortune-divination rounded-full"></div>
              <div className="w-2 h-2 bg-mystic-gold rounded-full"></div>
              <div className="w-2 h-2 bg-fortune-celestial rounded-full"></div>
            </div>
          </div>
        )}
        
        {/* Consultation stage decoration */}
        {stage === 'consulting' && (content.includes('muốn hỏi thêm') || parsedResponse.followUpMessage?.includes('muốn hỏi thêm')) && (
          <div className="mt-3 pt-3 border-t border-mystic-gold/20">
            <p className="text-xs text-mystic-gold/70 italic text-center">
              ✨ Hãy hỏi ta về những khía cạnh khác trong cuộc sống ✨
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Bot;