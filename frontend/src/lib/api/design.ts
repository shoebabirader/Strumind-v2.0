import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export interface DesignRequest {
  model_id: number;
  design_code: 'IS456' | 'IS800' | 'ACI318' | 'AISC360';
  element_ids?: number[];
  design_type: 'concrete' | 'steel';
}

export interface DesignResults {
  success: boolean;
  designed_elements: Array<{
    element_id: number;
    status: 'pass' | 'fail';
    reinforcement?: any;
    section?: any;
    utilization_ratio: number;
  }>;
  summary: {
    total_elements: number;
    passed: number;
    failed: number;
  };
}

export const designApi = {
  run: async (data: DesignRequest): Promise<DesignResults> => {
    const response = await apiClient.post<ApiResponse<DesignResults>>('/design/run', data);
    return response.data.data!;
  },
};
