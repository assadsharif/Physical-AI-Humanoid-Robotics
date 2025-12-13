import React from 'react';
import { ChatWidget } from '../components/ChatWidget';

interface RootProps {
  children: React.ReactNode;
}

// Default implementation that wraps the entire Docusaurus app
export default function Root({ children }: RootProps): React.JSX.Element {
  return (
    <>
      {children}
      <ChatWidget position="bottom-right" />
    </>
  );
}
