import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';
import type { AnalysisConfig, AnalysisResults } from '@/types/analysis';

export const analysisApi = {
  run: async (config: AnalysisConfig): Promise<AnalysisResults> => {
    const response = await apiClient.post<ApiResponse<AnalysisResults>>('/api/analysis/run', config);
    return response.data.data!;
  },
};
