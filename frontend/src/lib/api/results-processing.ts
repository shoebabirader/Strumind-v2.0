import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export interface DiagramRequest {
  element_id: number;
  load_case?: string;
  span?: number;
}

export const resultsProcessingApi = {
  momentDiagram: async (data: DiagramRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/results/moment-diagram', data);
    return response.data.data!;
  },

  shearDiagram: async (data: DiagramRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/results/shear-diagram', data);
    return response.data.data!;
  },

  deflectionCurve: async (data: DiagramRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/results/deflection-curve', data);
    return response.data.data!;
  },

  processBatch: async (elementIds: string[], resultsData: Record<string, any>): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/results/process-batch', {
      element_ids: elementIds,
      results_data: resultsData,
    });
    return response.data.data!;
  },

  getExportFormats: async (): Promise<string[]> => {
    const response = await apiClient.get<ApiResponse<string[]>>('/results/export-formats');
    return response.data.data!;
  },
};
