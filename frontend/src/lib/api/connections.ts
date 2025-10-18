import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export interface MomentConnectionRequest {
  beam_section: string;
  column_section: string;
  moment: number;
  shear: number;
  steel_grade: number;
}

export interface ShearConnectionRequest {
  beam_section: string;
  shear: number;
  steel_grade: number;
  connection_type: 'bolted' | 'welded';
}

export interface BasePlateRequest {
  column_section: string;
  axial_load: number;
  moment?: number;
  concrete_grade: number;
}

export const connectionsApi = {
  momentConnection: async (data: MomentConnectionRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/connections/moment-connection', data);
    return response.data.data!;
  },

  shearConnection: async (data: ShearConnectionRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/connections/shear-connection', data);
    return response.data.data!;
  },

  basePlate: async (data: BasePlateRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/connections/base-plate', data);
    return response.data.data!;
  },
};
