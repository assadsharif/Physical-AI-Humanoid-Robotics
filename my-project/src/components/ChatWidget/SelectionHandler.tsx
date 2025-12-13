import { useEffect, useCallback } from 'react';

interface SelectionHandlerProps {
  onTextSelected: (text: string) => void;
  maxLength?: number;
}

export function SelectionHandler({
  onTextSelected,
  maxLength = 2000
}: SelectionHandlerProps) {
  const handleMouseUp = useCallback(() => {
    const selection = window.getSelection();
    if (!selection || selection.isCollapsed) return;

    const selectedText = selection.toString().trim();
    if (!selectedText) return;

    // Check if selection is within docs content
    const range = selection.getRangeAt(0);
    const container = range.commonAncestorContainer;

    // Only capture selections within the main content area
    const isInDocsContent =
      container instanceof Element
        ? container.closest('article, .markdown, [class*="docItemContainer"]')
        : container.parentElement?.closest('article, .markdown, [class*="docItemContainer"]');

    if (!isInDocsContent) return;

    // Validate length
    if (selectedText.length > maxLength) {
      console.warn(`Selected text too long (${selectedText.length} chars). Max: ${maxLength}`);
      return;
    }

    // Only trigger if meaningful selection (more than just whitespace or single word)
    if (selectedText.length >= 10) {
      onTextSelected(selectedText);
    }
  }, [onTextSelected, maxLength]);

  useEffect(() => {
    // Only run in browser environment
    if (typeof window === 'undefined') return;

    // Listen for text selection completion
    document.addEventListener('mouseup', handleMouseUp);

    return () => {
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [handleMouseUp]);

  // This component doesn't render anything
  return null;
}

export default SelectionHandler;
