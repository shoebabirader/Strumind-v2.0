import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export interface BatchAnalysisRequest {
  model_ids: number[];
  analysis_type: string;
  parallel: boolean;
}

export interface ParametricStudyRequest {
  base_model_id: number;
  parameters: Record<string, number[]>;
  analysis_type: string;
}

export const parallelApi = {
  runBatchAnalysis: async (data: BatchAnalysisRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/batch-analysis', data);
    return response.data.data!;
  },

  runParametricStudy: async (data: ParametricStudyRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/parametric-study', data);
    return response.data.data!;
  },

  getExecutionStatus: async (): Promise<any> => {
    const response = await apiClient.get<ApiResponse<any>>('/execution/status');
    return response.data.data!;
  },

  getCapabilities: async (): Promise<any> => {
    const response = await apiClient.get<ApiResponse<any>>('/execution/capabilities');
    return response.data.data!;
  },
};
