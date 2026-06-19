import React, { useState, useRef, useEffect } from 'react';
import './ChatWidget.css';

const ChatWidget = ({ apiUrl = 'http://localhost:8000' }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      text: 'Hallo! 👋 Ich bin der WiSo Chatbot. Ich helfe dir bei Fragen zu deinem Studium an der FAU.',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [language, setLanguage] = useState('de');
  const messagesEndRef = useRef(null);

  const sampleQuestions = [
    'Wie melde ich mich zu Prüfungen an?',
    'Was ist StudOn?',
    'Wo finde ich die Modulhandbücher?',
    'Wann beginnt das Wintersemester?'
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (text = input) => {
    if (!text.trim()) return;

    const userMessage = {
      id: messages.length + 1,
      type: 'user',
      text: text,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch(`${apiUrl}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, language })
      });

      const data = await response.json();
      
      const botMessage = {
        id: messages.length + 2,
        type: 'bot',
        text: data.answer,
        confidence: data.confidence,
        sources: data.sources,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        id: messages.length + 2,
        type: 'bot',
        text: 'Entschuldigung, es gab ein technisches Problem. Bitte versuche es später noch einmal.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    }

    setLoading(false);
  };

  return (
    <div className="chat-widget">
      <div className="chat-header">
        <h2>🎓 WiSo Chatbot</h2>
        <select 
          value={language} 
          onChange={(e) => setLanguage(e.target.value)}
          className="language-selector"
        >
          <option value="de">Deutsch</option>
          <option value="en">English</option>
        </select>
      </div>

      <div className="chat-messages">
        {messages.map(msg => (
          <div key={msg.id} className={`message message-${msg.type}`}>
            <div className="message-content">
              {msg.text}
              {msg.confidence && (
                <div className="confidence">Konfidenz: {(msg.confidence * 100).toFixed(0)}%</div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="message message-bot">
            <div className="loading">
              <span></span><span></span><span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {messages.length === 1 && (
        <div className="sample-questions">
          <p>Beispielfragen:</p>
          {sampleQuestions.map((q, idx) => (
            <button
              key={idx}
              className="sample-btn"
              onClick={() => sendMessage(q)}
            >
              {q}
            </button>
          ))}
        </div>
      )}

      <div className="chat-input-area">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Stelle eine Frage..."
          className="chat-input"
          disabled={loading}
        />
        <button
          onClick={() => sendMessage()}
          className="send-btn"
          disabled={loading || !input.trim()}
        >
          Senden
        </button>
      </div>
    </div>
  );
};

export default ChatWidget;
