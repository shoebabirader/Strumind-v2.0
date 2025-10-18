import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';
import type { Node } from '@/types/model';

export const nodesApi = {
  // Create node
  create: async (data: Partial<Node>): Promise<Node> => {
    const response = await apiClient.post<ApiResponse<Node>>('/api/nodes/create', data);
    if (!response.data.data) {
      throw new Error('No data returned from create node');
    }
    return response.data.data;
  },

  // List nodes
  list: async (projectId: number): Promise<Node[]> => {
    try {
      const response = await apiClient.get<ApiResponse<Node[]>>(`/api/nodes/list/${projectId}`);
      return response.data.data || [];
    } catch (error) {
      console.error('Failed to fetch nodes:', error);
      return []; // Return empty array on error
    }
  },

  // Get node
  get: async (id: number): Promise<Node> => {
    const response = await apiClient.get<ApiResponse<Node>>(`/api/nodes/${id}`);
    if (!response.data.data) {
      throw new Error('Node not found');
    }
    return response.data.data;
  },

  // Update node
  update: async (id: number, data: Partial<Node>): Promise<Node> => {
    const response = await apiClient.put<ApiResponse<Node>>(`/api/nodes/${id}`, data);
    if (!response.data.data) {
      throw new Error('No data returned from update node');
    }
    return response.data.data;
  },

  // Delete node
  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/api/nodes/${id}`);
  },
};
