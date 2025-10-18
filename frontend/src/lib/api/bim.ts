import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export interface IFCExportRequest {
  project_id: number;
  include_analysis_results?: boolean;
  ifc_version?: '2x3' | '4';
}

export interface VisualizationRequest {
  model_id: number;
  analysis_results?: Record<string, any>;
}

export const bimApi = {
  exportIFC: async (data: IFCExportRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/bim/export/ifc', data);
    return response.data.data!;
  },

  importIFC: async (file: File): Promise<any> => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await apiClient.post<ApiResponse<any>>('/bim/import/ifc', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data.data!;
  },

  generateScene: async (data: VisualizationRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/bim/visualization/scene', data);
    return response.data.data!;
  },

  generateStressVisualization: async (data: VisualizationRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/bim/visualization/stress', data);
    return response.data.data!;
  },

  generateDeformationVisualization: async (data: VisualizationRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/bim/visualization/deformation', data);
    return response.data.data!;
  },
};
