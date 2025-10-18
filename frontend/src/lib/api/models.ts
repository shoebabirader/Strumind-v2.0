import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export interface ModelCreate {
  project_id: number;
  name: string;
  description?: string;
}

export interface Model {
  id: number;
  project_id: number;
  name: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export const modelsApi = {
  create: async (data: ModelCreate): Promise<Model> => {
    const response = await apiClient.post<ApiResponse<Model>>('/model/create', data);
    return response.data.data!;
  },

  get: async (modelId: number): Promise<Model> => {
    const response = await apiClient.get<ApiResponse<Model>>(`/model/${modelId}`);
    return response.data.data!;
  },
};
