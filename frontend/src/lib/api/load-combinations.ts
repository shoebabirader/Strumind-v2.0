import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export interface LoadCombinationGenerateRequest {
  code: string;
  load_cases: string[];
  limit_state: 'ultimate' | 'serviceability';
}

export interface EnvelopeGenerateRequest {
  model_id: number;
  result_type: 'moment' | 'shear' | 'axial' | 'displacement';
  combinations: string[];
}

export const loadCombinationsApi = {
  generate: async (data: LoadCombinationGenerateRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/load-combinations/generate', data);
    return response.data.data!;
  },

  generateEnvelope: async (data: EnvelopeGenerateRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/load-combinations/envelope', data);
    return response.data.data!;
  },

  getCodes: async (): Promise<string[]> => {
    const response = await apiClient.get<ApiResponse<string[]>>('/load-combinations/codes');
    return response.data.data!;
  },

  getFactors: async (code: string, limitState: string = 'ultimate'): Promise<any> => {
    const response = await apiClient.get<ApiResponse<any>>(`/load-combinations/factors/${code}`, {
      params: { limit_state: limitState },
    });
    return response.data.data!;
  },
};
