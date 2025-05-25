// File: src/components/MessageBubble.tsx
import React from 'react';
import { Message } from '../types/Message';
import Button from 'react-bootstrap/Button';

interface MessageBubbleProps {
  message: Message;
  darkMode: boolean;
  CopyIcon: React.FC;
  DownloadIcon: React.FC;
  onCopy?: (text: string) => void;
  onDownload?: (text: string) => void;
  onButtonClick?: (payload: string) => void;
}

export default function MessageBubble({
  message,
  darkMode,
  CopyIcon,
  DownloadIcon,
  onCopy,
  onDownload,
  onButtonClick,
}: MessageBubbleProps) {
  const isCode = message.text.startsWith('*') && message.text.endsWith('*');
  const code = message.text.replace(/^\*+|\*+$/g, '').trim();
  const detectLanguage = (text: string): string => {
    if (/^FROM\s+/im.test(text)) return 'docker';
    if (/^apiVersion:\s+/im.test(text) || /kind:\s+/im.test(text)) return 'yml';
    return 'text';
  };

  const language = detectLanguage(code);
  const handleCopy = () => {
    navigator.clipboard.writeText(code)
      .then(() => onCopy && onCopy(code))
      .catch((err) => console.error('Copy failed:', err));
  };

  const handleDownload = () => {
    const blob = new Blob([code], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `code-${message.id}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    if (onDownload) onDownload(code);
  };

  return (
    <div className={`d-flex justify-content-${message.isBot ? 'start' : 'end'} mb-3`}>
      <div
        className={`rounded p-3 position-relative ${
          message.isBot
            ? darkMode
              ? 'bg-black text-white border-dark'
              : 'bg-light text-dark border'
            : 'bg-primary text-white'
        }`}
        style={{ maxWidth: '75%' }}
      >
        {message.isBot && isCode ? (
          <>
            <div className="position-absolute top-0 end-0 mt-2 me-2 d-flex gap-1">
              <Button size="sm" variant={darkMode ? 'outline-light' : 'outline-dark'} onClick={handleCopy} title="Copy code">
                <CopyIcon />
              </Button>
              <Button size="sm" variant={darkMode ? 'outline-light' : 'outline-dark'} onClick={handleDownload} title="Download code">
                <DownloadIcon />
              </Button>
            </div>
            <br />
            <pre className={`mb-0 ${darkMode ? 'text-white' : ''}`} style={{ whiteSpace: 'pre-wrap', paddingRight: '3rem' }}>
              <code className={`language-${language}`}>{code}</code>
            </pre>
          </>
        ) : (
          <div>{message.text}</div>
        )}
        {message.buttons?.map((b, i) => (
          <button
            key={i}
            className={`btn btn-sm me-2 mt-1 ${darkMode ? 'btn-outline-light' : 'btn-outline-secondary'}`}
            onClick={() => onButtonClick && onButtonClick(b.payload)}
          >
            {b.title}
          </button>
        ))}
      </div>
    </div>
  );
}
