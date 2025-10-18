import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export interface Comment {
  element_id: string;
  user_id: string;
  text: string;
  timestamp?: string;
}

export const collaborationApi = {
  addComment: async (data: Comment): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/collaboration/comments/add', data);
    return response.data.data!;
  },

  getComments: async (elementId: string): Promise<Comment[]> => {
    const response = await apiClient.get<ApiResponse<Comment[]>>(`/collaboration/comments/${elementId}`);
    return response.data.data!;
  },

  getActiveUsers: async (projectId: number): Promise<any> => {
    const response = await apiClient.get<ApiResponse<any>>(`/projects/${projectId}/active-users`);
    return response.data.data!;
  },
};
