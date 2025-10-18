/**
 * Comprehensive security utilities for input sanitization
 * Prevents XSS, log injection, prototype pollution, and other injection attacks
 */

import DOMPurify from 'isomorphic-dompurify';

/**
 * Sanitize string for logging to prevent log injection
 * Removes newlines, carriage returns, and control characters
 */
export function sanitizeForLog(input: string | unknown): string {
  const str = typeof input === 'string' ? input : String(input);
  
  return str
    .replace(/[\r\n]/g, ' ') // Remove newlines
    .replace(/[\x00-\x1F\x7F]/g, '') // Remove control characters
    .trim();
}

/**
 * Sanitize HTML using DOMPurify to prevent XSS
 * Removes all potentially dangerous HTML/JavaScript
 */
export function sanitizeHTML(input: string): string {
  if (typeof input !== 'string') {
    return '';
  }
  
  return DOMPurify.sanitize(input, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p', 'br', 'ul', 'ol', 'li'],
    ALLOWED_ATTR: ['href', 'title'],
    ALLOW_DATA_ATTR: false,
  });
}

/**
 * Sanitize rich text content (allows more tags for descriptions, etc.)
 */
export function sanitizeRichText(input: string): string {
  if (typeof input !== 'string') {
    return '';
  }
  
  return DOMPurify.sanitize(input, {
    ALLOWED_TAGS: [
      'b', 'i', 'em', 'strong', 'a', 'p', 'br', 'ul', 'ol', 'li',
      'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'code', 'pre',
      'table', 'thead', 'tbody', 'tr', 'th', 'td', 'span', 'div'
    ],
    ALLOWED_ATTR: ['href', 'title', 'class'],
    ALLOW_DATA_ATTR: false,
  });
}

/**
 * Sanitize for display in UI
 * Uses DOMPurify for comprehensive XSS protection
 */
export function sanitizeForDisplay(input: string | unknown): string {
  const str = typeof input === 'string' ? input : String(input);
  return sanitizeHTML(str);
}

/**
 * Sanitize JWT token format
 * Ensures token matches expected JWT format
 */
export function sanitizeToken(token: string): string | null {
  if (typeof token !== 'string') {
    return null;
  }
  
  // JWT format: header.payload.signature
  const jwtPattern = /^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+$/;
  
  if (!jwtPattern.test(token)) {
    return null;
  }
  
  return token;
}

/**
 * Sanitize URL to prevent javascript: and data: protocols
 */
export function sanitizeURL(url: string): string | null {
  if (typeof url !== 'string') {
    return null;
  }
  
  const trimmed = url.trim().toLowerCase();
  
  // Block dangerous protocols
  if (
    trimmed.startsWith('javascript:') ||
    trimmed.startsWith('data:') ||
    trimmed.startsWith('vbscript:') ||
    trimmed.startsWith('file:')
  ) {
    return null;
  }
  
  // Allow http, https, mailto, and relative URLs
  if (
    trimmed.startsWith('http://') ||
    trimmed.startsWith('https://') ||
    trimmed.startsWith('mailto:') ||
    trimmed.startsWith('/') ||
    trimmed.startsWith('#')
  ) {
    return url.trim();
  }
  
  return null;
}

/**
 * Validate and sanitize numeric input
 */
export function sanitizeNumber(input: unknown, defaultValue: number = 0): number {
  const num = Number(input);
  if (isNaN(num) || !isFinite(num)) {
    return defaultValue;
  }
  return num;
}

/**
 * Validate and sanitize file path
 * Prevents path traversal attacks
 */
export function sanitizeFilePath(path: string): string {
  // Remove path traversal attempts
  return path
    .replace(/\.\./g, '')
    .replace(/[\/\\]+/g, '/')
    .replace(/^\/+/, '');
}

/**
 * Sanitize filename to prevent path traversal
 */
export function sanitizeFilename(filename: string): string | null {
  if (typeof filename !== 'string') {
    return null;
  }
  
  // Remove path separators and dangerous characters
  const sanitized = filename
    .replace(/[\/\\]/g, '')
    .replace(/\.\./g, '')
    .replace(/[<>:"|?*\x00-\x1F]/g, '')
    .trim();
  
  if (sanitized.length === 0 || sanitized.length > 255) {
    return null;
  }
  
  return sanitized;
}

/**
 * Safe JSON parse with validation
 * Returns null if parsing fails or data is invalid
 */
export function safeJSONParse<T = any>(json: string): T | null {
  try {
    if (typeof json !== 'string') {
      return null;
    }
    
    const parsed = JSON.parse(json);
    
    // Prevent prototype pollution
    if (parsed && typeof parsed === 'object') {
      if ('__proto__' in parsed || 'constructor' in parsed || 'prototype' in parsed) {
        console.warn('Potential prototype pollution detected in JSON');
        return null;
      }
    }
    
    return parsed as T;
  } catch (error) {
    console.error('JSON parse error:', sanitizeForLog(String(error)));
    return null;
  }
}

/**
 * Validate and sanitize object keys
 * Removes dangerous keys that could lead to prototype pollution
 */
export function sanitizeObjectKeys<T extends Record<string, any>>(obj: T): Partial<T> {
  if (!obj || typeof obj !== 'object') {
    return {};
  }
  
  const dangerousKeys = ['__proto__', 'constructor', 'prototype'];
  const sanitized: any = {};
  
  for (const key in obj) {
    if (obj.hasOwnProperty(key) && !dangerousKeys.includes(key)) {
      sanitized[key] = obj[key];
    }
  }
  
  return sanitized;
}

/**
 * Sanitize object for API transmission
 * Recursively sanitizes all string values
 */
export function sanitizeObject<T extends Record<string, any>>(obj: T): T {
  const sanitized = { ...obj };
  
  for (const key in sanitized) {
    const value = sanitized[key];
    
    if (typeof value === 'string') {
      sanitized[key] = sanitizeForDisplay(value) as any;
    } else if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
      sanitized[key] = sanitizeObject(value);
    } else if (Array.isArray(value)) {
      sanitized[key] = value.map((item: any) => 
        typeof item === 'string' ? sanitizeForDisplay(item) : 
        typeof item === 'object' && item !== null ? sanitizeObject(item) : 
        item
      ) as any;
    }
  }
  
  return sanitized;
}
