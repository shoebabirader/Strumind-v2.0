import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export interface ConversionRequest {
  value: number;
  from_unit: string;
  to_unit: string;
  from_system: string;
  to_system: string;
}

export interface BatchConversionRequest {
  values: Record<string, number>;
  from_system: string;
  to_system: string;
}

export const unitsApi = {
  convert: async (data: ConversionRequest): Promise<number> => {
    const response = await apiClient.post<ApiResponse<number>>('/units/convert', data);
    return response.data.data!;
  },

  batchConvert: async (data: BatchConversionRequest): Promise<Record<string, number>> => {
    const response = await apiClient.post<ApiResponse<Record<string, number>>>('/units/batch-convert', data);
    return response.data.data!;
  },

  getSupportedUnits: async (): Promise<any> => {
    const response = await apiClient.get<ApiResponse<any>>('/units/supported');
    return response.data.data!;
  },

  getUnitSystems: async (): Promise<string[]> => {
    const response = await apiClient.get<ApiResponse<string[]>>('/units/systems');
    return response.data.data!;
  },
};
