import React, { useState, useCallback, forwardRef, KeyboardEvent, ChangeEvent } from 'react';
import styles from './ChatWidget.module.css';

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

export const ChatInput = forwardRef<HTMLTextAreaElement, ChatInputProps>(
  function ChatInput({ onSend, disabled = false, placeholder = "Ask about the textbook..." }, ref) {
    const [value, setValue] = useState('');

    const handleChange = useCallback((e: ChangeEvent<HTMLTextAreaElement>) => {
      const newValue = e.target.value;
      if (newValue.length <= 500) {
        setValue(newValue);
      }
    }, []);

    const handleSubmit = useCallback(() => {
      if (value.trim() && !disabled) {
        onSend(value.trim());
        setValue('');
      }
    }, [value, disabled, onSend]);

    const handleKeyDown = useCallback((e: KeyboardEvent<HTMLTextAreaElement>) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSubmit();
      }
    }, [handleSubmit]);

    const charCount = value.length;
    const isNearLimit = charCount >= 450;

    return (
      <div className={styles.inputContainer}>
        <div className={styles.inputWrapper}>
          <textarea
            ref={ref}
            className={styles.input}
            value={value}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            disabled={disabled}
            rows={1}
            aria-label="Chat message input"
            aria-describedby="char-count"
            maxLength={500}
          />
          <button
            className={styles.sendButton}
            onClick={handleSubmit}
            disabled={disabled || !value.trim()}
            aria-label="Send message"
            type="button"
          >
            <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true">
              <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
            </svg>
          </button>
        </div>
        <div
          id="char-count"
          className={`${styles.charCount} ${isNearLimit ? styles.nearLimit : ''}`}
          aria-live="polite"
        >
          {charCount}/500
        </div>
      </div>
    );
  }
);

export default ChatInput;
