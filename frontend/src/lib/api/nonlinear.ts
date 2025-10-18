import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export interface MaterialNonlinearityRequest {
  material_type: 'concrete' | 'steel';
  model_type: 'bilinear' | 'trilinear' | 'parabolic';
  parameters: Record<string, number>;
}

export interface NewtonRaphsonRequest {
  model_id: number;
  load_steps: number;
  max_iterations?: number;
  tolerance?: number;
}

export interface ArcLengthRequest {
  model_id: number;
  arc_length: number;
  max_steps?: number;
}

export interface PlasticHingeRequest {
  element_id: number;
  hinge_type: 'moment' | 'axial' | 'interaction';
  hinge_location: 'both_ends' | 'start' | 'end';
  properties: Record<string, number>;
}

export const nonlinearApi = {
  createMaterialModel: async (data: MaterialNonlinearityRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/nonlinear/material-model', data);
    return response.data.data!;
  },

  runNewtonRaphson: async (data: NewtonRaphsonRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/nonlinear/newton-raphson', data);
    return response.data.data!;
  },

  runArcLength: async (data: ArcLengthRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/nonlinear/arc-length', data);
    return response.data.data!;
  },

  createPlasticHinge: async (data: PlasticHingeRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/nonlinear/plastic-hinge', data);
    return response.data.data!;
  },

  listSolvers: async (): Promise<string[]> => {
    const response = await apiClient.get<ApiResponse<string[]>>('/nonlinear/solvers');
    return response.data.data!;
  },
};
