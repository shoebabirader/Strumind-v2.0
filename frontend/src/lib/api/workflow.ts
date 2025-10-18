import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export interface WorkflowRequest {
  project_id: number;
  analysis_type?: string;
}

export const workflowApi = {
  create: async (): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/workflow/create');
    return response.data.data!;
  },

  runComplete: async (data: WorkflowRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/workflow/run-complete', data);
    return response.data.data!;
  },

  getStatus: async (workflowId: string): Promise<any> => {
    const response = await apiClient.get<ApiResponse<any>>(`/workflow/status/${workflowId}`);
    return response.data.data!;
  },
};
