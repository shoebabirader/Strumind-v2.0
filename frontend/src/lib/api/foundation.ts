import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export interface FoundationDesignRequest {
  type: 'isolated' | 'mat' | 'pile';
  loads: {
    P: number;
    Mx?: number;
    My?: number;
    Hx?: number;
    Hy?: number;
  };
  soil_bearing_capacity: number;
  concrete_grade: number;
  steel_grade: number;
  depth?: number;
}

export interface IsolatedFootingRequest {
  loads: Record<string, number>;
  soil_bearing_capacity: number;
  concrete_grade: number;
  steel_grade: number;
}

export interface MatFoundationRequest {
  loads: Record<string, number>;
  soil_bearing_capacity: number;
  area: number;
}

export interface PileFoundationRequest {
  loads: Record<string, number>;
  pile_capacity: number;
  pile_diameter: number;
}

export const foundationApi = {
  design: async (data: FoundationDesignRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/foundation/design', data);
    return response.data.data!;
  },

  isolatedFooting: async (data: IsolatedFootingRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/foundation/isolated-footing', data);
    return response.data.data!;
  },

  matFoundation: async (data: MatFoundationRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/foundation/mat-foundation', data);
    return response.data.data!;
  },

  pileFoundation: async (data: PileFoundationRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/foundation/pile-foundation', data);
    return response.data.data!;
  },
};
