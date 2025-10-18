import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export interface OneWaySlabRequest {
  span: number;
  width: number;
  loads: Record<string, number>;
  code?: string;
}

export interface TwoWaySlabRequest {
  lx: number;
  ly: number;
  loads: Record<string, number>;
  support_conditions: string;
  code?: string;
}

export interface FlatSlabRequest {
  panel_dimensions: Record<string, number>;
  column_dimensions: Record<string, number>;
  loads: Record<string, number>;
  code?: string;
}

export const slabDesignApi = {
  oneWay: async (data: OneWaySlabRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/slab-design/one-way', data);
    return response.data.data!;
  },

  twoWay: async (data: TwoWaySlabRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/slab-design/two-way', data);
    return response.data.data!;
  },

  flatSlab: async (data: FlatSlabRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/slab-design/flat-slab', data);
    return response.data.data!;
  },

  getCodes: async (): Promise<string[]> => {
    const response = await apiClient.get<ApiResponse<string[]>>('/slab-design/codes');
    return response.data.data!;
  },
};
