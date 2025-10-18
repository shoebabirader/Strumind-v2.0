import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';
import type { Element } from '@/types/model';

export const elementsApi = {
  create: async (data: Partial<Element>): Promise<Element> => {
    const response = await apiClient.post<ApiResponse<Element>>('/api/elements/create', data);
    if (!response.data.data) {
      throw new Error('No data returned from create element');
    }
    return response.data.data;
  },

  list: async (projectId: number): Promise<Element[]> => {
    try {
      const response = await apiClient.get<ApiResponse<Element[]>>(`/api/elements/list/${projectId}`);
      return response.data.data || [];
    } catch (error) {
      console.error('Failed to fetch elements:', error);
      return [];
    }
  },

  get: async (id: number): Promise<Element> => {
    const response = await apiClient.get<ApiResponse<Element>>(`/api/elements/${id}`);
    if (!response.data.data) {
      throw new Error('Element not found');
    }
    return response.data.data;
  },

  update: async (id: number, data: Partial<Element>): Promise<Element> => {
    const response = await apiClient.put<ApiResponse<Element>>(`/api/elements/${id}`, data);
    if (!response.data.data) {
      throw new Error('No data returned from update element');
    }
    return response.data.data;
  },

  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/api/elements/${id}`);
  },
};
