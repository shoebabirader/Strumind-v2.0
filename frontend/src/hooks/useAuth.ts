import { useAuthStore } from '@/stores/authStore';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api/client';
import type { LoginRequest, RegisterRequest } from '@/types/auth';

// Inline auth API to avoid module resolution issues
const authApi = {
  login: async (data: LoginRequest) => {
    // Convert to URLSearchParams for proper form encoding
    const params = new URLSearchParams();
    params.append('username', data.username);
    params.append('password', data.password);
    const response = await apiClient.post('/api/auth/login', params.toString(), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
    return response.data;
  },
  register: async (data: RegisterRequest) => {
    const response = await apiClient.post('/api/auth/register', data);
    return response.data;
  },
  me: async () => {
    const response = await apiClient.get('/api/auth/me');
    return response.data.data;
  },
  logout: async () => {
    await apiClient.post('/api/auth/logout');
  },
};

export function useAuth() {
  const { user, token, setUser, setToken, logout: clearAuth } = useAuthStore();
  const router = useRouter();

  const login = async (username: string, password: string) => {
    try {
      const data = await authApi.login({ username, password });
      setToken(data.access_token);
      const userData = await authApi.me();
      setUser(userData);
      router.push('/workspace');
      return { success: true };
    } catch (error: any) {
      return { success: false, error: error.response?.data?.detail || 'Login failed' };
    }
  };

  const register = async (email: string, password: string, fullName: string) => {
    try {
      const data = await authApi.register({ username: email, email, password, full_name: fullName });
      setToken(data.access_token);
      setUser(data.user);
      router.push('/workspace');
      return { success: true };
    } catch (error: any) {
      return { success: false, error: error.response?.data?.detail || 'Registration failed' };
    }
  };

  const logout = async () => {
    try {
      await authApi.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      clearAuth();
      router.push('/login');
    }
  };

  return {
    user,
    token,
    isAuthenticated: !!token,
    login,
    register,
    logout,
  };
}
