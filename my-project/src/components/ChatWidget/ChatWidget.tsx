import React, { useState, useCallback, useEffect, useRef } from 'react';
import { ChatMessage, ChatWidgetProps, PageContext, Citation } from './types';
import { MessageList } from './MessageList';
import { ChatInput } from './ChatInput';
import { SelectionHandler } from './SelectionHandler';
import styles from './ChatWidget.module.css';

// Configuration - Set your backend URL here
const API_BASE_URL = 'http://localhost:8000';

const generateSessionId = (): string => {
  return 'session_' + Math.random().toString(36).substring(2, 15);
};

const generateMessageId = (): string => {
  return 'msg_' + Math.random().toString(36).substring(2, 15);
};

// Check if backend is available
const checkBackendHealth = async (baseUrl: string): Promise<boolean> => {
  try {
    const response = await fetch(`${baseUrl}/api/health`, {
      method: 'GET',
      signal: AbortSignal.timeout(3000),
    });
    return response.ok;
  } catch {
    return false;
  }
};

// Mock API response for demo when backend is not available
const mockChatResponse = async (query: string, selectedText: string | null): Promise<{
  response_text: string;
  sources: Citation[];
  is_off_topic: boolean;
}> => {
  await new Promise(resolve => setTimeout(resolve, 800));

  const bookTopics = ['robot', 'humanoid', 'ros', 'ai', 'control', 'locomotion', 'kinematics', 'dynamics', 'simulation', 'gazebo', 'vla', 'bipedal', 'manipulation', 'chapter', 'what', 'how', 'explain'];
  const isOnTopic = bookTopics.some(topic =>
    query.toLowerCase().includes(topic) ||
    (selectedText && selectedText.toLowerCase().includes(topic))
  );

  if (!isOnTopic && !selectedText) {
    return {
      response_text: "I can only answer questions about the Physical AI & Humanoid Robotics textbook content. Please ask about topics like humanoid kinematics, ROS2, simulation, locomotion, or VLA systems.",
      sources: [],
      is_off_topic: true
    };
  }

  if (selectedText) {
    return {
      response_text: `This passage discusses a concept related to Physical AI. ${selectedText.length > 100 ? 'The selected text covers technical details that are explained in more depth in the referenced chapter.' : 'Let me explain this in simpler terms based on the textbook content.'}\n\n**Demo Mode:** Connect the backend for RAG-powered responses.`,
      sources: [{
        chapter: "Chapter 1",
        section: "Embodied Intelligence",
        url: "/docs/part-i-foundations/ch01-embodied-intelligence",
        relevance_score: 0.85
      }],
      is_off_topic: false
    };
  }

  return {
    response_text: "Based on the Physical AI & Humanoid Robotics textbook, this topic is covered in detail in the referenced chapters.\n\n**Demo Mode:** The chatbot backend is not connected. To get real RAG-powered responses:\n\n1. Set up the FastAPI backend\n2. Configure environment variables\n3. Run the content ingestion script\n\nSee `backend/README.md` for setup instructions.",
    sources: [{
      chapter: "Chapter 1",
      section: "Embodied Intelligence",
      url: "/docs/part-i-foundations/ch01-embodied-intelligence",
      relevance_score: 0.92
    }, {
      chapter: "Chapter 9",
      section: "ROS2 Architecture",
      url: "/docs/part-iii-ros2/ch09-ros2-architecture",
      relevance_score: 0.78
    }],
    is_off_topic: false
  };
};

export function ChatWidget({
  apiEndpoint = `${API_BASE_URL}/api/chat`,
  position = 'bottom-right'
}: ChatWidgetProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(generateSessionId);
  const [selectedText, setSelectedText] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [backendAvailable, setBackendAvailable] = useState<boolean | null>(null);
  const chatPanelRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Check backend availability on mount
  useEffect(() => {
    checkBackendHealth(API_BASE_URL).then(setBackendAvailable);
  }, []);

  const getPageContext = useCallback((): PageContext => {
    const path = typeof window !== 'undefined' ? window.location.pathname : '';
    const parts = path.split('/');
    return {
      chapter_id: parts[parts.length - 1] || 'unknown',
      section_id: null,
      url: path
    };
  }, []);

  const handleToggle = useCallback(() => {
    setIsOpen(prev => !prev);
    setError(null);
  }, []);

  const handleClose = useCallback(() => {
    setIsOpen(false);
    setSelectedText(null);
    setError(null);
  }, []);

  const handleTextSelection = useCallback((text: string) => {
    setSelectedText(text);
    setIsOpen(true);
  }, []);

  const handleClearSelection = useCallback(() => {
    setSelectedText(null);
  }, []);

  const handleSendMessage = useCallback(async (query: string) => {
    if (!query.trim() || isLoading) return;

    // Validate query length
    if (query.length > 500) {
      setError('Query is too long. Please limit to 500 characters.');
      return;
    }

    setError(null);
    const userMessage: ChatMessage = {
      id: generateMessageId(),
      role: 'user',
      content: query,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      let responseData;

      // Use real API if backend is available, otherwise fall back to mock
      if (backendAvailable) {
        const response = await fetch(apiEndpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            query,
            session_id: sessionId,
            selected_text: selectedText,
            page_context: getPageContext()
          })
        });

        if (!response.ok) {
          if (response.status === 429) {
            throw new Error('Rate limit exceeded. Please wait a moment before trying again.');
          }
          throw new Error('Failed to get response. Please try again.');
        }

        responseData = await response.json();
      } else {
        // Use mock API when backend is not available
        responseData = await mockChatResponse(query, selectedText);
      }

      const assistantMessage: ChatMessage = {
        id: generateMessageId(),
        role: 'assistant',
        content: responseData.response_text,
        citations: responseData.sources,
        isOffTopic: responseData.is_off_topic,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
      setSelectedText(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  }, [apiEndpoint, sessionId, selectedText, getPageContext, isLoading]);

  // Handle keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        handleClose();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, handleClose]);

  // Focus input when chat opens
  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);

  // Check if we're on a docs page
  const isDocsPage = typeof window !== 'undefined' && window.location.pathname.includes('/docs');

  if (!isDocsPage) {
    return null;
  }

  return (
    <>
      <SelectionHandler onTextSelected={handleTextSelection} />

      {/* Chat Toggle Button */}
      <button
        className={`${styles.toggleButton} ${styles[position]}`}
        onClick={handleToggle}
        aria-label={isOpen ? 'Close chat assistant' : 'Open chat assistant'}
        aria-expanded={isOpen}
        aria-controls="chat-panel"
      >
        {isOpen ? (
          <svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor" aria-hidden="true">
            <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
          </svg>
        ) : (
          <svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor" aria-hidden="true">
            <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/>
          </svg>
        )}
      </button>

      {/* Chat Panel */}
      {isOpen && (
        <div
          id="chat-panel"
          ref={chatPanelRef}
          className={`${styles.chatPanel} ${styles[position]}`}
          role="dialog"
          aria-label="Physical AI Textbook Assistant"
          aria-modal="true"
        >
          {/* Header */}
          <div className={styles.header}>
            <h2 className={styles.headerTitle}>Textbook Assistant</h2>
            <button
              className={styles.closeButton}
              onClick={handleClose}
              aria-label="Close chat"
            >
              <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true">
                <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
              </svg>
            </button>
          </div>

          {/* Selected Text Banner */}
          {selectedText && (
            <div className={styles.selectionBanner}>
              <span className={styles.selectionLabel}>Selected text:</span>
              <span className={styles.selectionText}>
                {selectedText.length > 100 ? selectedText.substring(0, 100) + '...' : selectedText}
              </span>
              <button
                className={styles.clearSelection}
                onClick={handleClearSelection}
                aria-label="Clear selection"
              >
                Clear
              </button>
            </div>
          )}

          {/* Messages */}
          <MessageList
            messages={messages}
            isLoading={isLoading}
          />

          {/* Error Display */}
          {error && (
            <div className={styles.error} role="alert">
              {error}
            </div>
          )}

          {/* Input */}
          <ChatInput
            ref={inputRef}
            onSend={handleSendMessage}
            disabled={isLoading}
            placeholder={selectedText ? "Ask about the selected text..." : "Ask about the textbook..."}
          />
        </div>
      )}
    </>
  );
}

export default ChatWidget;
