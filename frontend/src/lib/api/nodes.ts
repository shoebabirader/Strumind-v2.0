import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';
import type { Node } from '@/types/model';

export const nodesApi = {
  // Create node
  create: async (data: Partial<Node>): Promise<Node> => {
    const response = await apiClient.post<ApiResponse<Node>>('/api/nodes/create', data);
    return response.data.data!;
  },

  // List nodes
  list: async (projectId: number): Promise<Node[]> => {
    const response = await apiClient.get<ApiResponse<Node[]>>(`/api/nodes/list/${projectId}`);
    return response.data.data!;
  },

  // Get node
  get: async (id: number): Promise<Node> => {
    const response = await apiClient.get<ApiResponse<Node>>(`/api/nodes/${id}`);
    return response.data.data!;
  },

  // Update node
  update: async (id: number, data: Partial<Node>): Promise<Node> => {
    const response = await apiClient.put<ApiResponse<Node>>(`/api/nodes/${id}`, data);
    return response.data.data!;
  },

  // Delete node
  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/api/nodes/${id}`);
  },
};
