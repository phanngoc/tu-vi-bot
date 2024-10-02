import Bot from './bot';
import Human from './human';

function ContentChat() {
  return (
    <div className="flex-1 mt-6">
      <div className="space-y-4">
        <Bot />
        <Human/>
      </div>
    </div>
  );
}

export default ContentChat;
