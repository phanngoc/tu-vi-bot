interface HumanProps {
  content: string;
}

function Human({ content }: HumanProps) {
  const formatContent = (text: string) => {
    // Split by newlines and format each line
    const lines = text.split('\n').filter(line => line.trim());
    
    return lines.map((line, index) => (
      <p key={index} className="mb-1 last:mb-0">
        {line}
      </p>
    ));
  };

  return (
    <div className="flex justify-end items-start space-x-3">
      {/* Message Content */}
      <div className="max-w-[70%] p-4 bg-gradient-to-br from-mystic-amber/80 to-mystic-gold/60 text-white rounded-xl shadow-lg border border-mystic-gold/40 backdrop-blur-sm animate-ancient-breathe">
        <div className="prose prose-sm max-w-none text-white">
          {formatContent(content)}
        </div>
      </div>
      
      {/* User Avatar */}
      <div className="flex-shrink-0 w-10 h-10 bg-gradient-to-br from-mystic-silver/20 to-mystic-cosmic/40 rounded-full flex items-center justify-center text-lg border border-mystic-silver/30 animate-float-gentle">
        👤
      </div>
    </div>
  );
}

export default Human;