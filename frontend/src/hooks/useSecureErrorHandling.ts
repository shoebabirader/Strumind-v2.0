/**
 * Secure error handling hook
 * Provides sanitized error logging and user-friendly error messages
 */
import { useCallback } from 'react';

interface ErrorHandlingOptions {
  operation: string;
  showToast?: boolean;
  logToConsole?: boolean;
}

export function useSecureErrorHandling() {
  const sanitizeError = useCallback((error: unknown): string => {
    // SECURITY FIX: Sanitize error messages to prevent log injection
    if (error instanceof Error) {
      return error.message
        .replace(/[\r\n]/g, ' ')  // Remove newlines
        .replace(/[\x00-\x1F\x7F]/g, '')  // Remove control characters
        .substring(0, 200);  // Limit length
    }
    return 'Unknown error occurred';
  }, []);

  const handleError = useCallback((
    error: unknown,
    options: ErrorHandlingOptions
  ) => {
    const sanitizedMessage = sanitizeError(error);
    
    // SECURITY FIX: Log sanitized error only
    if (options.logToConsole !== false) {
      console.error(`${options.operation} failed:`, sanitizedMessage);
    }
    
    // TODO: Add toast notification if needed
    // if (options.showToast) {
    //   toast.error(`${options.operation} failed: ${sanitizedMessage}`);
    // }
    
    return sanitizedMessage;
  }, [sanitizeError]);

  const handleSuccess = useCallback((
    operation: string,
    logToConsole: boolean = false
  ) => {
    // SECURITY FIX: Don't log sensitive result data
    if (logToConsole) {
      console.log(`${operation} completed successfully`);
    }
  }, []);

  return {
    handleError,
    handleSuccess,
    sanitizeError,
  };
}
