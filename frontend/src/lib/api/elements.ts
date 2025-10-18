import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';
import type { Element } from '@/types/model';

export const elementsApi = {
  create: async (data: Partial<Element>): Promise<Element> => {
    const response = await apiClient.post<ApiResponse<Element>>('/api/elements/create', data);
    return response.data.data!;
  },

  list: async (projectId: number): Promise<Element[]> => {
    const response = await apiClient.get<ApiResponse<Element[]>>(`/api/elements/list/${projectId}`);
    return response.data.data!;
  },

  get: async (id: number): Promise<Element> => {
    const response = await apiClient.get<ApiResponse<Element>>(`/api/elements/${id}`);
    return response.data.data!;
  },

  update: async (id: number, data: Partial<Element>): Promise<Element> => {
    const response = await apiClient.put<ApiResponse<Element>>(`/api/elements/${id}`, data);
    return response.data.data!;
  },

  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/api/elements/${id}`);
  },
};
