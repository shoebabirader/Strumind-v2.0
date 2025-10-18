import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User } from '@/types/auth';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  disclaimerAccepted: boolean;
  setUser: (user: User | null) => void;
  setToken: (token: string | null) => void;
  setDisclaimerAccepted: (accepted: boolean) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      disclaimerAccepted: false,
      
      setUser: (user) => set({ user, isAuthenticated: !!user }),
      
      setToken: (token) => {
        // SECURITY FIX: Validate token format before storing
        if (token) {
          // Basic JWT format validation (header.payload.signature)
          const jwtPattern = /^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+$/;
          if (!jwtPattern.test(token)) {
            console.error('Invalid token format');
            return;
          }
          localStorage.setItem('auth_token', token);
        } else {
          localStorage.removeItem('auth_token');
        }
        set({ token, isAuthenticated: !!token });
      },
      
      setDisclaimerAccepted: (accepted) => set({ disclaimerAccepted: accepted }),
      
      logout: () => {
        localStorage.removeItem('auth_token');
        set({ user: null, token: null, isAuthenticated: false });
      },
    }),
    {
      name: 'auth-storage',
    }
  )
);
