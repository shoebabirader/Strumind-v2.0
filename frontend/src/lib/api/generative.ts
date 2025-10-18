import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export interface GenerativeDesignRequest {
  design_space: Record<string, any>;
  objectives: string[];
  constraints: Record<string, any>;
  num_designs?: number;
}

export interface TopologyOptimizationRequest {
  design_space: Record<string, any>;
  loads: Record<string, any>;
  constraints: Record<string, any>;
  volume_fraction?: number;
}

export interface SizeSuggestionRequest {
  model: Record<string, any>;
  loads: Record<string, any>;
  design_code: string;
}

export interface Report3DRequest {
  project_id: number;
  include_analysis?: boolean;
  include_design?: boolean;
  format?: 'pdf' | 'html';
}

export const generativeApi = {
  generateDesigns: async (data: GenerativeDesignRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/generative/generate-designs', data);
    return response.data.data!;
  },

  topologyOptimization: async (data: TopologyOptimizationRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/generative/topology-optimization', data);
    return response.data.data!;
  },

  suggestSizes: async (data: SizeSuggestionRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/generative/suggest-sizes', data);
    return response.data.data!;
  },

  generate3DReport: async (data: Report3DRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/generative/generate-3d-report', data);
    return response.data.data!;
  },

  get3DViewer: async (projectId: number): Promise<any> => {
    const response = await apiClient.get<ApiResponse<any>>(`/generative/3d-viewer/${projectId}`);
    return response.data.data!;
  },

  export3DModel: async (projectId: number, format: string): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/generative/export-3d-model', { project_id: projectId, format });
    return response.data.data!;
  },
};
