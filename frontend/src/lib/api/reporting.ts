import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export interface ReportRequest {
  project_id: number;
  analysis_data: Record<string, any>;
  design_data: Record<string, any>;
  format?: 'pdf' | 'docx' | 'html';
}

export interface CalculationSheetRequest {
  element_id: number;
  design_type: 'concrete' | 'steel';
  design_code: string;
}

export const reportingApi = {
  generateAnalysisReport: async (data: ReportRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/reporting/analysis-report', data);
    return response.data.data!;
  },

  generateCalculationSheet: async (data: CalculationSheetRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/reporting/calculation-sheet', data);
    return response.data.data!;
  },
};
