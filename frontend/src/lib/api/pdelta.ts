import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export interface PDeltaRequest {
  model_id: number;
  load_case: string;
  max_iterations?: number;
  tolerance?: number;
}

export interface StabilityIndexRequest {
  story_shear: number;
  story_weight: number;
  story_drift: number;
  story_height: number;
}

export const pdeltaApi = {
  runAnalysis: async (data: PDeltaRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/pdelta/analysis', data);
    return response.data.data!;
  },

  calculateStabilityIndex: async (data: StabilityIndexRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/pdelta/stability-index', data);
    return response.data.data!;
  },

  momentAmplification: async (Pu: number, Pc: number, Cm: number = 1.0): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/pdelta/moment-amplification', { Pu, Pc, Cm });
    return response.data.data!;
  },
};
