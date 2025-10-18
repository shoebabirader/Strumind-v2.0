import axios, { AxiosInstance, AxiosError } from 'axios';
import { sanitizeForLog, sanitizeToken, sanitizeObjectKeys } from '@/lib/utils/sanitize';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance
export const apiClient: AxiosInstance = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('auth_token');
      if (token) {
        // SECURITY: Validate token format before sending
        const sanitized = sanitizeToken(token);
        if (sanitized) {
          config.headers.Authorization = `Bearer ${sanitized}`;
        } else {
          console.warn('Invalid token format detected');
          localStorage.removeItem('auth_token');
        }
      }
    }
    
    // SECURITY: Sanitize request data to prevent prototype pollution
    if (config.data && typeof config.data === 'object') {
      config.data = sanitizeObjectKeys(config.data);
    }
    
    return config;
  },
  (error) => {
    console.error('Request error:', sanitizeForLog(String(error)));
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    // SECURITY: Sanitize response data to prevent prototype pollution
    if (response.data && typeof response.data === 'object') {
      response.data = sanitizeObjectKeys(response.data);
    }
    return response;
  },
  (error: AxiosError) => {
    // Handle 401 Unauthorized
    if (error.response?.status === 401) {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('auth_token');
        window.location.href = '/login';
      }
    }
    
    // SECURITY: Sanitize all error messages to prevent log injection
    if (!error.response) {
      console.error('Network error:', sanitizeForLog(error.message || 'Unknown error'));
    } else {
      const status = error.response.status;
      const message = error.response.data ? 
        sanitizeForLog(JSON.stringify(error.response.data)) : 
        'No error message';
      console.error(`API error ${status}:`, message);
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;
