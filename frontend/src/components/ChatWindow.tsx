import React, { useRef, useEffect } from 'react';
import { Message } from '../types/Message';
import MessageBubble from './MessageBubble';

interface ChatWindowProps {
  messages: Message[];
  darkMode: boolean;
  CopyIcon: React.FC;
  DownloadIcon: React.FC;
  onButtonClick: (payload: string) => void;
}

export default function ChatWindow({
  messages,
  darkMode,
  CopyIcon,
  DownloadIcon,
  onButtonClick,
}: ChatWindowProps) {
  const endRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (endRef.current) {
      endRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  return (
    <div className="flex-grow-1 overflow-auto p-3">
      {messages.map((msg) => (
        <MessageBubble
          key={msg.id}
          message={msg}
          darkMode={darkMode}
          CopyIcon={CopyIcon}
          DownloadIcon={DownloadIcon}
          onButtonClick={onButtonClick}
        />
      ))}
      <div ref={endRef} />
    </div>
  );
}
