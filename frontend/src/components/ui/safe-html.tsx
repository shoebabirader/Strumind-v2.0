/**
 * SafeHTML Component
 * Renders sanitized HTML content to prevent XSS attacks
 */

import React from 'react';
import { sanitizeHTML, sanitizeRichText } from '@/lib/utils/sanitize';

interface SafeHTMLProps {
  html: string;
  className?: string;
  allowRichText?: boolean;
}

/**
 * Component that safely renders HTML content
 * All content is sanitized using DOMPurify before rendering
 */
export function SafeHTML({ html, className, allowRichText = false }: SafeHTMLProps) {
  const sanitized = allowRichText ? sanitizeRichText(html) : sanitizeHTML(html);
  
  return (
    <div
      className={className}
      dangerouslySetInnerHTML={{ __html: sanitized }}
    />
  );
}

/**
 * Component for safely displaying user text
 * Escapes all HTML to prevent XSS
 */
export function SafeText({ text, className }: { text: string; className?: string }) {
  return <span className={className}>{text}</span>;
}
