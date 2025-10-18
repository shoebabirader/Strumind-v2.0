import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export interface ShellElementRequest {
  nodes: number[];
  thickness: number;
  material_id: number;
  formulation?: 'thin' | 'thick';
}

export interface PlateElementRequest {
  nodes: number[];
  thickness: number;
  material_id: number;
  formulation?: 'kirchhoff' | 'mindlin';
}

export interface SolidElementRequest {
  nodes: number[];
  material_id: number;
  element_type: 'tetrahedron' | 'hexahedron';
}

export interface LinkElementRequest {
  node_i: number;
  node_j: number;
  area?: number;
  element_type: 'truss' | 'cable' | 'gap';
}

export const advancedElementsApi = {
  createShell: async (data: ShellElementRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/advanced-elements/shell', data);
    return response.data.data!;
  },

  createPlate: async (data: PlateElementRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/advanced-elements/plate', data);
    return response.data.data!;
  },

  createSolid: async (data: SolidElementRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/advanced-elements/solid', data);
    return response.data.data!;
  },

  createLink: async (data: LinkElementRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/advanced-elements/link', data);
    return response.data.data!;
  },

  listTypes: async (): Promise<string[]> => {
    const response = await apiClient.get<ApiResponse<string[]>>('/advanced-elements/types');
    return response.data.data!;
  },

  listFormulations: async (): Promise<any> => {
    const response = await apiClient.get<ApiResponse<any>>('/advanced-elements/formulations');
    return response.data.data!;
  },
};
