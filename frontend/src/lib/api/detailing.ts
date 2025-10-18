import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export interface DetailingRequest {
  element_id: number;
  design_results: Record<string, any>;
  drawing_standard?: 'IS' | 'BS' | 'ACI';
}

export const detailingApi = {
  generate: async (data: DetailingRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/detailing/generate', data);
    return response.data.data!;
  },
};
