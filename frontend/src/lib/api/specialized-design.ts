import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export interface ShearWallRequest {
  height: number;
  length: number;
  thickness: number;
  axial_load: number;
  shear_force: number;
  moment: number;
  boundary_element?: boolean;
}

export interface RetainingWallRequest {
  wall_type: 'cantilever' | 'gravity';
  height: number;
  surcharge?: number;
  soil_properties: Record<string, number>;
}

export interface StaircaseRequest {
  stair_type: 'dog_legged' | 'cantilever' | 'spiral';
  flight_length?: number;
  flight_width?: number;
  waist_thickness: number;
  riser: number;
  tread: number;
  loads: Record<string, number>;
}

export interface CompositeBeamRequest {
  span: number;
  steel_section: Record<string, any>;
  slab_thickness: number;
  slab_width: number;
  loads: Record<string, number>;
}

export interface CompositeColumnRequest {
  height: number;
  steel_section: Record<string, any>;
  concrete_dimensions: Record<string, number>;
  axial_load: number;
  moment: number;
}

export interface MovingLoadRequest {
  span: number;
  response_type: string;
  location: number;
  loading_standard?: string;
}

export interface TemperatureAnalysisRequest {
  analysis_type: 'uniform' | 'gradient' | 'fire' | 'seasonal';
  delta_T?: number;
  material?: string;
  length: number;
}

export interface MeshRequest {
  mesh_type: 'rectangle' | 'circle';
  width?: number;
  height?: number;
  nx?: number;
  ny?: number;
}

export const specializedDesignApi = {
  shearWall: async (data: ShearWallRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/specialized-design/shear-wall', data);
    return response.data.data!;
  },

  couplingBeam: async (data: any): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/specialized-design/coupling-beam', data);
    return response.data.data!;
  },

  retainingWall: async (data: RetainingWallRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/specialized-design/retaining-wall', data);
    return response.data.data!;
  },

  staircase: async (data: StaircaseRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/specialized-design/staircase', data);
    return response.data.data!;
  },

  compositeBeam: async (data: CompositeBeamRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/specialized-design/composite-beam', data);
    return response.data.data!;
  },

  compositeColumn: async (data: CompositeColumnRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/specialized-design/composite-column', data);
    return response.data.data!;
  },

  movingLoad: async (data: MovingLoadRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/specialized-design/moving-load', data);
    return response.data.data!;
  },

  temperatureAnalysis: async (data: TemperatureAnalysisRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/specialized-design/temperature-analysis', data);
    return response.data.data!;
  },

  generateMesh: async (data: MeshRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/specialized-design/mesh/generate', data);
    return response.data.data!;
  },

  refineMesh: async (data: any): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/specialized-design/mesh/refine', data);
    return response.data.data!;
  },

  checkMeshQuality: async (data: any): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/specialized-design/mesh/quality-check', data);
    return response.data.data!;
  },
};
