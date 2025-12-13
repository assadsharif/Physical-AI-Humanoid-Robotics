import React, { useEffect, useRef } from 'react';
import { ChatMessage } from './types';
import { CitationLink } from './Citation';
import styles from './ChatWidget.module.css';

interface MessageListProps {
  messages: ChatMessage[];
  isLoading: boolean;
}

export function MessageList({ messages, isLoading }: MessageListProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const listRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  return (
    <div
      ref={listRef}
      className={styles.messageList}
      role="log"
      aria-label="Chat messages"
      aria-live="polite"
      aria-atomic="false"
    >
      {messages.length === 0 && !isLoading && (
        <div className={styles.welcomeMessage}>
          <h3>Welcome to the Textbook Assistant</h3>
          <p>Ask questions about the Physical AI & Humanoid Robotics textbook content.</p>
          <ul>
            <li>Ask about concepts like "What is Zero Moment Point?"</li>
            <li>Select text on the page and ask "Explain this"</li>
            <li>Get references to specific chapters</li>
          </ul>
        </div>
      )}

      {messages.map((message) => (
        <div
          key={message.id}
          className={`${styles.message} ${styles[message.role]}`}
          role="article"
          aria-label={`${message.role === 'user' ? 'You' : 'Assistant'}: ${message.content.substring(0, 50)}...`}
        >
          <div className={styles.messageContent}>
            {message.role === 'assistant' ? (
              <div className={styles.assistantMessage}>
                <div className={styles.messageText}>
                  {message.content.split('\n').map((line, i) => (
                    <React.Fragment key={i}>
                      {line.startsWith('**') && line.endsWith('**') ? (
                        <strong>{line.replace(/\*\*/g, '')}</strong>
                      ) : (
                        line
                      )}
                      {i < message.content.split('\n').length - 1 && <br />}
                    </React.Fragment>
                  ))}
                </div>
                {message.citations && message.citations.length > 0 && (
                  <div className={styles.citations}>
                    <span className={styles.citationsLabel}>Sources:</span>
                    {message.citations.map((citation, index) => (
                      <CitationLink key={index} citation={citation} index={index + 1} />
                    ))}
                  </div>
                )}
                {message.isOffTopic && (
                  <div className={styles.offTopicIndicator}>
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true">
                      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
                    </svg>
                    Off-topic query
                  </div>
                )}
              </div>
            ) : (
              <div className={styles.userMessage}>{message.content}</div>
            )}
          </div>
        </div>
      ))}

      {isLoading && (
        <div className={`${styles.message} ${styles.assistant}`} role="status" aria-label="Assistant is typing">
          <div className={styles.messageContent}>
            <div className={styles.loadingIndicator}>
              <span className={styles.dot}></span>
              <span className={styles.dot}></span>
              <span className={styles.dot}></span>
            </div>
          </div>
        </div>
      )}

      <div ref={messagesEndRef} />
    </div>
  );
}

export default MessageList;
