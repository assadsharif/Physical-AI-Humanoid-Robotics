import React from 'react';
import { Citation } from './types';
import styles from './ChatWidget.module.css';

interface CitationLinkProps {
  citation: Citation;
  index: number;
}

export function CitationLink({ citation, index }: CitationLinkProps) {
  const handleClick = (e: React.MouseEvent) => {
    e.preventDefault();
    // Navigate to the citation URL
    if (typeof window !== 'undefined') {
      window.location.href = citation.url;
    }
  };

  return (
    <a
      href={citation.url}
      className={styles.citationLink}
      onClick={handleClick}
      title={`${citation.chapter}: ${citation.section} (Relevance: ${Math.round(citation.relevance_score * 100)}%)`}
      aria-label={`Source ${index}: ${citation.chapter}, ${citation.section}`}
    >
      <span className={styles.citationIndex}>[{index}]</span>
      <span className={styles.citationChapter}>{citation.chapter}</span>
    </a>
  );
}

export default CitationLink;
