import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export interface NodeCreateRequest {
  x: number;
  y: number;
  z: number;
  coordinate_system?: string;
}

export interface RestraintUpdateRequest {
  node_id: number;
  restraint_type: 'fixed' | 'pinned' | 'roller';
  dof?: Record<string, boolean>;
}

export interface ElementCreateRequest {
  node_i: number;
  node_j: number;
  section_id: number;
  material_id: number;
}

export interface DistributedLoadRequest {
  element_id: number;
  load_type: 'uniform' | 'varying';
  w1: number;
  w2?: number;
  direction: 'x' | 'y' | 'z';
}

export const geometryApi = {
  createEngine: async (): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/geometry/create-engine');
    return response.data.data!;
  },

  createNode: async (data: NodeCreateRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/geometry/nodes/create', data);
    return response.data.data!;
  },

  setRestraint: async (data: RestraintUpdateRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/geometry/nodes/set-restraint', data);
    return response.data.data!;
  },

  createElement: async (data: ElementCreateRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/geometry/elements/create', data);
    return response.data.data!;
  },

  addDistributedLoad: async (data: DistributedLoadRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/geometry/elements/add-distributed-load', data);
    return response.data.data!;
  },

  validate: async (nodeCount: number, elementCount: number): Promise<any> => {
    const response = await apiClient.get<ApiResponse<any>>('/geometry/validate', {
      params: { node_count: nodeCount, element_count: elementCount },
    });
    return response.data.data!;
  },
};
