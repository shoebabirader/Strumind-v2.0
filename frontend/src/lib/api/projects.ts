import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';
import type { Project } from '@/types/model';

export const projectsApi = {
  // Create project
  create: async (data: Partial<Project>): Promise<Project> => {
    const response = await apiClient.post<ApiResponse<Project>>('/api/projects/create', data);
    return response.data.data!;
  },

  // List projects
  list: async (): Promise<Project[]> => {
    const response = await apiClient.get<ApiResponse<Project[]>>('/api/projects/list');
    return response.data.data!;
  },

  // Get project
  get: async (id: number): Promise<Project> => {
    const response = await apiClient.get<ApiResponse<Project>>(`/api/projects/${id}`);
    return response.data.data!;
  },

  // Delete project
  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/api/projects/${id}`);
  },
};
