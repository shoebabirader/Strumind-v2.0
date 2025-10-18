import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

// IS456 Concrete Design
export interface IS456FlexuralRequest {
  b: number;
  d: number;
  fck: number;
  fy: number;
  Mu: number;
  cover?: number;
}

export interface IS456ShearRequest {
  b: number;
  d: number;
  fck: number;
  fy: number;
  Vu: number;
  Ast?: number;
}

export interface IS456TorsionRequest {
  b: number;
  d: number;
  fck: number;
  fy: number;
  Tu: number;
  Vu?: number;
  Mu?: number;
}

// IS800 Steel Design
export interface IS800TensionRequest {
  section: string;
  fy: number;
  fu: number;
  Tu: number;
  connection_type?: string;
}

export interface IS800CompressionRequest {
  section: string;
  fy: number;
  length: number;
  Pu: number;
  end_conditions: string;
}

export interface IS800BeamRequest {
  section: string;
  fy: number;
  span: number;
  Mu: number;
  lateral_support?: string;
}

export const designExtendedApi = {
  // IS456 Concrete
  is456Flexural: async (data: IS456FlexuralRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/design-extended/is456/flexural', data);
    return response.data.data!;
  },

  is456Shear: async (data: IS456ShearRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/design-extended/is456/shear', data);
    return response.data.data!;
  },

  is456Torsion: async (data: IS456TorsionRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/design-extended/is456/torsion', data);
    return response.data.data!;
  },

  // IS800 Steel
  is800Tension: async (data: IS800TensionRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/design-extended/is800/tension', data);
    return response.data.data!;
  },

  is800Compression: async (data: IS800CompressionRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/design-extended/is800/compression', data);
    return response.data.data!;
  },

  is800Beam: async (data: IS800BeamRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/design-extended/is800/beam', data);
    return response.data.data!;
  },

  // Legacy endpoints
  concreteFlexure: async (data: any): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/design-extended/concrete/flexure', data);
    return response.data.data!;
  },

  steelMember: async (data: any): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/design-extended/steel/member', data);
    return response.data.data!;
  },

  listCodes: async (): Promise<string[]> => {
    const response = await apiClient.get<ApiResponse<string[]>>('/design-extended/codes/list');
    return response.data.data!;
  },
};
