import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export const cacheApi = {
  getStats: async (): Promise<any> => {
    const response = await apiClient.get<ApiResponse<any>>('/cache/stats');
    return response.data.data!;
  },

  clear: async (): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/cache/clear');
    return response.data.data!;
  },

  invalidateModel: async (modelHash: string): Promise<any> => {
    const response = await apiClient.delete<ApiResponse<any>>(`/cache/analysis/${modelHash}`);
    return response.data.data!;
  },

  checkHealth: async (): Promise<any> => {
    const response = await apiClient.get<ApiResponse<any>>('/cache/health');
    return response.data.data!;
  },
};
