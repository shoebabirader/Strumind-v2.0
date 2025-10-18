import { useEffect, useRef } from 'react';
import { wsClient } from '@/lib/api/websocket';
import { useAuth } from './useAuth';

export function useWebSocket(projectId?: number) {
  const { token } = useAuth();
  const socketRef = useRef<any>(null);

  useEffect(() => {
    if (projectId && token) {
      socketRef.current = wsClient.connect(projectId, token);

      return () => {
        wsClient.disconnect();
      };
    }
  }, [projectId, token]);

  const emit = (event: string, data: any) => {
    wsClient.emit(event, data);
  };

  const on = (event: string, callback: (data: any) => void) => {
    wsClient.on(event, callback);
  };

  const off = (event: string) => {
    wsClient.off(event);
  };

  return { emit, on, off };
}
