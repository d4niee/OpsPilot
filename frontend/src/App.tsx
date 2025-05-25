import { useState, useEffect } from 'react';
import NavBar from './components/NavBar';
import ChatWindow from './components/ChatWindow';
import Sidebar from './components/SideBar';
import InputForm from './components/InputForm';
import ToastNotification from './components/ToastNotification';
import { CopyIcon, DownloadIcon } from './icons';
import Prism from 'prismjs';
import 'prismjs/themes/prism-tomorrow.css';
import 'prismjs/components/prism-docker';
import { ToastState } from './types/ToastState';
import { Message } from './types/Message';

const DEFAULT_RASA_WEBHOOK_URL = 'http://localhost:5005/webhooks/rest/webhook';

const RASA_WEBHOOK_URL = (() => {
  const url = import.meta.env.VITE_RASA_WEBHOOK_URL;
  if (!url) {
    console.warn(
      '[⚠️ WARNUNG] VITE_RASA_WEBHOOK_URL nicht gesetzt - benutze Fallback:',
      DEFAULT_RASA_WEBHOOK_URL
    );
    return DEFAULT_RASA_WEBHOOK_URL;
  }
  return url;
})();

function App() {
  const [messages, setMessages] = useState<Message[]>([
    { id: 1, text: 'Hello! How can I help you today?', isBot: true }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [showSidebar, setShowSidebar] = useState(false);
  const [darkMode, setDarkMode] = useState(() => {
    const saved = localStorage.getItem('darkMode');
    return saved === 'true' || (saved === null && window.matchMedia("(prefers-color-scheme: dark)").matches);
  });
  const [toast, setToast] = useState<ToastState>({
    show: false,
    message: ''
  });

  const handleTemplateClick = async (payload: string) => {
    addMessage({ id: Date.now(), text: payload, isBot: false });
    try {
      const response = await fetch(RASA_WEBHOOK_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sender: 'user', message: payload }),
      });
      const data = await response.json();
      data.forEach((res: any) => {
        if (res.text) {
          addMessage({ id: Date.now() + Math.random(), text: res.text, isBot: true, buttons: res.buttons });
        }
      });
    } catch (error) {
      console.error(error);
      addMessage({ id: Date.now() + Math.random(), text: 'Es gab ein Problem mit dem Bot.', isBot: true });
    }
  };

  useEffect(() => {
    Prism.highlightAll();
  }, [messages]);

  useEffect(() => {
    localStorage.setItem('darkMode', darkMode.toString());
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  const toggleDarkMode = () => setDarkMode((dm) => !dm);
  const handleLoginClick = () => showToast('feature currently not available!');

  const addMessage = (msg: Message) =>
    setMessages((prev) => [...prev, msg]);

  const showToast = (message: string) =>
    setToast({ show: true, message });

  const sendMessage = async (text: string) => {
    addMessage({ id: Date.now(), text, isBot: false });
    setInputMessage('');

    try {
      const response = await fetch(RASA_WEBHOOK_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sender: 'user', message: text })
      });
      const data: Array<{ text?: string; buttons?: any[] }> =
        await response.json();

      data.forEach((res) => {
        if (res.text) {
          addMessage({
            id: Date.now() + Math.random(),
            text: res.text,
            isBot: true,
            buttons: res.buttons
          });
        }
      });
    } catch (err) {
      console.error(err);
      addMessage({
        id: Date.now() + Math.random(),
        text:
          '😕 There was a problem with the bot. Please try again later or refresh the Page. (Rasa Server may be not available right now)',
        isBot: true
      });
    }
  };

  return (
    <div
      className={`d-flex flex-column min-vh-100 ${
        darkMode ? 'bg-dark text-white' : ''
      }`}
      >
      <NavBar
        darkMode={darkMode}
        toggleDarkMode={toggleDarkMode}
        onLogin={handleLoginClick}
        onToggleSidebar={() => setShowSidebar(true)}
      />
      <div className="d-flex flex-grow-1">
        <Sidebar
          show={showSidebar}
          onHide={() => setShowSidebar(false)}
          darkMode={darkMode}
        />
        <div className="container-fluid flex-grow-1 d-flex flex-column">
          <ChatWindow
            messages={messages}
            darkMode={darkMode}
            CopyIcon={CopyIcon}
            DownloadIcon={DownloadIcon}
            onButtonClick={handleTemplateClick}
          />
          <InputForm
            inputMessage={inputMessage}
            setInputMessage={setInputMessage}
            onSubmit={sendMessage}
            darkMode={darkMode}
          />
          <ToastNotification toast={toast} darkMode={darkMode} />
        </div>
      </div>
    </div>
  );
}

export default App;
