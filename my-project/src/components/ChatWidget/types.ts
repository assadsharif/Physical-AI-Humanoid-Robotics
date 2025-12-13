export interface Citation {
  chapter: string;
  section: string;
  url: string;
  relevance_score: number;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  citations?: Citation[];
  timestamp: Date;
  isOffTopic?: boolean;
}

export interface PageContext {
  chapter_id: string;
  section_id: string | null;
  url: string;
}

export interface ChatRequest {
  query: string;
  session_id: string;
  selected_text: string | null;
  page_context: PageContext;
}

export interface ChatResponse {
  response: string;
  citations: Citation[];
  conversation_id: string;
  is_off_topic: boolean;
}

export interface ChatWidgetProps {
  apiEndpoint?: string;
  position?: 'bottom-right' | 'bottom-left';
}
