import { io, Socket } from 'socket.io-client';
import { sanitizeToken } from '@/lib/utils/sanitize';

// SECURITY FIX: Use secure WebSocket protocol in production
const getWebSocketURL = (): string => {
  const baseURL = process.env.NEXT_PUBLIC_WS_URL || 'http://localhost:8000';
  
  // In production, enforce WSS (secure WebSocket)
  if (typeof window !== 'undefined' && window.location.protocol === 'https:') {
    return baseURL.replace('http://', 'https://').replace('ws://', 'wss://');
  }
  
  return baseURL;
};

const WS_URL = getWebSocketURL();

export class WebSocketClient {
  private socket: Socket | null = null;

  connect(projectId: number, token: string) {
    // SECURITY FIX: Validate token before connecting
    const validatedToken = sanitizeToken(token);
    if (!validatedToken) {
      console.error('Invalid token format for WebSocket connection');
      throw new Error('Invalid authentication token');
    }
    
    // SECURITY FIX: Validate project ID
    if (!Number.isInteger(projectId) || projectId <= 0) {
      console.error('Invalid project ID for WebSocket connection');
      throw new Error('Invalid project ID');
    }
    
    this.socket = io(`${WS_URL}/ws/projects/${projectId}`, {
      auth: { token: validatedToken },
      transports: ['websocket'],
      secure: window.location.protocol === 'https:',
      rejectUnauthorized: true,
    });

    this.socket.on('connect', () => {
      console.log('WebSocket connected');
    });

    this.socket.on('disconnect', () => {
      console.log('WebSocket disconnected');
    });

    return this.socket;
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  emit(event: string, data: Record<string, unknown>) {
    if (this.socket) {
      // SECURITY FIX: Validate event name
      if (typeof event !== 'string' || event.length === 0) {
        console.error('Invalid event name');
        return;
      }
      this.socket.emit(event, data);
    }
  }

  on(event: string, callback: (data: Record<string, unknown>) => void) {
    if (this.socket) {
      // SECURITY FIX: Validate event name
      if (typeof event !== 'string' || event.length === 0) {
        console.error('Invalid event name');
        return;
      }
      this.socket.on(event, callback);
    }
  }

  off(event: string) {
    if (this.socket) {
      this.socket.off(event);
    }
  }
}

export const wsClient = new WebSocketClient();
