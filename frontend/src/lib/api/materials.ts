import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';
import type { Material } from '@/types/model';

export const materialsApi = {
  getLibrary: async (): Promise<Material[]> => {
    const response = await apiClient.get<ApiResponse<{ materials: Material[] }>>('/api/materials/library');
    return response.data.data!.materials;
  },

  create: async (data: Partial<Material>): Promise<Material> => {
    const response = await apiClient.post<ApiResponse<Material>>('/api/materials/create', data);
    return response.data.data!;
  },

  list: async (projectId: number): Promise<Material[]> => {
    const response = await apiClient.get<ApiResponse<Material[]>>(`/api/materials/list/${projectId}`);
    return response.data.data!;
  },

  get: async (id: number): Promise<Material> => {
    const response = await apiClient.get<ApiResponse<Material>>(`/api/materials/${id}`);
    return response.data.data!;
  },

  update: async (id: number, data: Partial<Material>): Promise<Material> => {
    const response = await apiClient.put<ApiResponse<Material>>(`/api/materials/${id}`, data);
    return response.data.data!;
  },

  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/api/materials/${id}`);
  },
};
