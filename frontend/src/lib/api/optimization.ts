import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export interface BeamOptimizationRequest {
  span: number;
  loads: Record<string, number>;
  constraints: Record<string, number>;
  objective: 'cost' | 'weight' | 'carbon';
}

export interface ColumnOptimizationRequest {
  height: number;
  loads: Record<string, number>;
  constraints: Record<string, number>;
  objective: 'cost' | 'weight' | 'carbon';
}

export interface MultiObjectiveRequest {
  model_id: number;
  objectives: string[];
  constraints: Record<string, any>;
}

export const optimizationApi = {
  beamSection: async (data: BeamOptimizationRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/optimization/beam-section', data);
    return response.data.data!;
  },

  columnSection: async (data: ColumnOptimizationRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/optimization/column-section', data);
    return response.data.data!;
  },

  multiObjective: async (data: MultiObjectiveRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/optimization/multi-objective', data);
    return response.data.data!;
  },

  listAlgorithms: async (): Promise<string[]> => {
    const response = await apiClient.get<ApiResponse<string[]>>('/optimization/algorithms');
    return response.data.data!;
  },
};
