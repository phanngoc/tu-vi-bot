'use client';

import React, { useState } from 'react';
import Human from './human';
import Bot from './bot';


const HOST_URL = 'http://127.0.0.1:5000';

function PageContent() {
  const [inputValue, setInputValue] = useState('những năm tuổi dễ sống hạnh phúc');
  const [messages, setMessages] = useState<{ type: string; content: string }[]>(
    [
      { type: 'bot', content: 'Bạn muốn biết gì về thiên mệnh trong cuộc sống này ?' }
    ]
  );

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const handleButtonClick = async () => {
    console.log('inputValue', inputValue);
    if (inputValue.trim() === '') return;
    setMessages([...messages, { type: 'human', content: inputValue }]);
    setInputValue('');

    try {
      const res = await fetch(HOST_URL + '/api/reply', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: inputValue }),
      });
      const data = await res.json();
      setMessages((prevMessages) => [
        ...prevMessages,
        { type: 'bot', content: data.message },
      ]);

    } catch (error) {
      console.error('Error fetching the horoscope:', error);
    }
  };

  return (
    <div className="max-w-[800px] h-[calc(100vh-32px)] py-4 bg-black/60 relative z-10 rounded-lg shadow-lg flex flex-1 flex-col p-6">
      <h1 className="font-bold text-2xl text-blue-500 dark:text-yellow-300 font-title">
        Xem tử vi
      </h1>
      <div className="h-full overflow-y-auto">
        <div className="flex flex-col items-center justify-center mt-6 bg-neutral-100 rounded-md p-4">
          <div className="text-center">
            <p className="font-semibold text-lg">Today&apos;s Horoscope</p>
            <p className="text-sm mt-3">
              Your adventures might take you to unconventional places. Embrace the unknown.
            </p>
          </div>
          <div className="mt-6">
            <svg width="100" height="100" viewBox="0 0 24 24">
              <path
                fill="currentColor"
                d="M17,18a1,1,0,0,0,.92-.6A6.34,6.34,0,0,0,19,15V9A7,7,0,0,0,5,9v6a6.34,6.34,0,0,0,1.08,2.4,1,1,0,0,0,.92.6A1,1,0,0,0,8,17.6l.58,1.16a1,1,0,0,0,.89.54H14.53a1,1,0,0,0,.89-.54L16,17.6A1,1,0,0,0,17,18ZM7,9a5,5,0,0,1,10,0v6a.42.42,0,0,1-.08.2H7.08A.41.41,0,0,1,7,15Z"
              />
              <circle cx="9" cy="12" r="1.25" fill="currentColor" />
              <circle cx="15" cy="12" r="1.25" fill="currentColor" />
            </svg>
          </div>
        </div>
        {messages.map((msg, index) =>
          msg.type === 'human' ? (
            <Human key={index} content={msg.content} />
          ) : (
            <Bot key={index} content={msg.content} />
          )
        )}
      </div>
      <div className="mt-4 flex items-center bg-neutral-100 rounded-md p-3 gap-3">
        <input
          type="text"
          placeholder="Điền câu trả lời của bạn tại đây..."
          className="flex-1 bg-neutral-50 p-2 rounded-md outline-none"
          value={inputValue}
          onChange={handleInputChange}
        />
        <button
          className="text-black rounded-full w-fit h-[40px] flex items-center justify-center"
          onClick={handleButtonClick}
        >
          Trả lời
        </button>
      </div>
    </div>
  );
}

export default PageContent;
