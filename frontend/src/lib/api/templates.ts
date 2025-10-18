import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export interface Template {
  name: string;
  description: string;
  category: string;
  preview_image?: string;
}

export const templatesApi = {
  list: async (): Promise<Template[]> => {
    const response = await apiClient.get<ApiResponse<Template[]>>('/templates/list');
    return response.data.data!;
  },

  get: async (templateName: string): Promise<any> => {
    const response = await apiClient.get<ApiResponse<any>>(`/templates/${templateName}`);
    return response.data.data!;
  },
};
