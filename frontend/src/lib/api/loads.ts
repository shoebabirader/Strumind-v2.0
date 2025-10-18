import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';
import type { Load } from '@/types/model';

export const loadsApi = {
  create: async (data: Partial<Load>): Promise<Load> => {
    const response = await apiClient.post<ApiResponse<Load>>('/api/loads/create', data);
    return response.data.data!;
  },

  createNodal: async (data: Partial<Load>): Promise<Load> => {
    const response = await apiClient.post<ApiResponse<Load>>('/api/loads/nodal', data);
    return response.data.data!;
  },

  createElement: async (data: Partial<Load>): Promise<Load> => {
    const response = await apiClient.post<ApiResponse<Load>>('/api/loads/element', data);
    return response.data.data!;
  },

  list: async (projectId: number): Promise<Load[]> => {
    const response = await apiClient.get<ApiResponse<Load[]>>(`/api/loads/list/${projectId}`);
    return response.data.data!;
  },

  get: async (id: number): Promise<Load> => {
    const response = await apiClient.get<ApiResponse<Load>>(`/api/loads/${id}`);
    return response.data.data!;
  },

  update: async (id: number, data: Partial<Load>): Promise<Load> => {
    const response = await apiClient.put<ApiResponse<Load>>(`/api/loads/${id}`, data);
    return response.data.data!;
  },

  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/api/loads/${id}`);
  },
};
