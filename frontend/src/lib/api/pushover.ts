import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export interface PushoverRequest {
  model_id: number;
  load_pattern: 'uniform' | 'triangular' | 'modal';
  target_displacement?: number;
  max_steps?: number;
}

export const pushoverApi = {
  runPushover: async (data: PushoverRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/pushover/pushover', data);
    return response.data.data!;
  },

  getCapacityCurve: async (data: PushoverRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/pushover/capacity-curve', data);
    return response.data.data!;
  },

  getPerformancePoint: async (data: PushoverRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/pushover/performance-point', data);
    return response.data.data!;
  },
};
