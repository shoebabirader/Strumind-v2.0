import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';
import type { Section } from '@/types/model';

export const sectionsApi = {
  getLibrary: async (): Promise<Section[]> => {
    const response = await apiClient.get<ApiResponse<{ sections: Section[] }>>('/api/sections/library');
    return response.data.data!.sections;
  },

  create: async (data: Partial<Section>): Promise<Section> => {
    const response = await apiClient.post<ApiResponse<Section>>('/api/sections/create', data);
    return response.data.data!;
  },

  list: async (projectId: number): Promise<Section[]> => {
    const response = await apiClient.get<ApiResponse<Section[]>>(`/api/sections/list/${projectId}`);
    return response.data.data!;
  },

  get: async (id: number): Promise<Section> => {
    const response = await apiClient.get<ApiResponse<Section>>(`/api/sections/${id}`);
    return response.data.data!;
  },

  update: async (id: number, data: Partial<Section>): Promise<Section> => {
    const response = await apiClient.put<ApiResponse<Section>>(`/api/sections/${id}`, data);
    return response.data.data!;
  },

  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/api/sections/${id}`);
  },
};
