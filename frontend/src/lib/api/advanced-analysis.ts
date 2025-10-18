import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export interface TimeHistoryRequest {
  model_id: number;
  ground_motion: number[];
  time_step: number;
  damping_ratio: number;
  integration_method?: 'newmark' | 'wilson';
}

export interface BucklingRequest {
  model_id: number;
  num_modes?: number;
  load_case?: string;
}

export interface LoadCombinationRequest {
  code: string;
  load_cases: string[];
  limit_state: 'ultimate' | 'serviceability';
}

export interface EnvelopeRequest {
  model_id: number;
  result_type: 'moment' | 'shear' | 'axial' | 'displacement';
  combinations: string[];
}

export const advancedAnalysisApi = {
  timeHistory: async (data: TimeHistoryRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/advanced-analysis/time-history', data);
    return response.data.data!;
  },

  buckling: async (data: BucklingRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/advanced-analysis/buckling', data);
    return response.data.data!;
  },

  loadCombinations: async (data: LoadCombinationRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/advanced-analysis/load-combinations', data);
    return response.data.data!;
  },

  envelope: async (data: EnvelopeRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/advanced-analysis/envelope', data);
    return response.data.data!;
  },

  slabDesign: async (data: any): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/advanced-analysis/slab-design', data);
    return response.data.data!;
  },

  getSteelSections: async (standard: string): Promise<any> => {
    const response = await apiClient.get<ApiResponse<any>>(`/advanced-analysis/steel-sections/${standard}`);
    return response.data.data!;
  },

  getSteelStandards: async (): Promise<string[]> => {
    const response = await apiClient.get<ApiResponse<string[]>>('/advanced-analysis/steel-sections/standards');
    return response.data.data!;
  },
};
