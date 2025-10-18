import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export interface DeflectionCheckRequest {
  span: number;
  deflection: number;
  load_type: 'dead' | 'live' | 'total';
  member_type: 'beam' | 'slab' | 'cantilever';
}

export interface CrackWidthCheckRequest {
  stress: number;
  cover: number;
  bar_diameter: number;
  spacing: number;
  exposure: 'mild' | 'moderate' | 'severe';
}

export interface VibrationCheckRequest {
  natural_frequency: number;
  floor_type: 'office' | 'residential' | 'hospital';
  damping_ratio?: number;
}

export interface PunchingShearCheckRequest {
  slab_thickness: number;
  column_dimensions: Record<string, number>;
  punching_force: number;
  concrete_grade: number;
}

export interface FatigueCheckRequest {
  stress_range: number;
  cycles: number;
  detail_category: string;
}

export interface SlendernessCheckRequest {
  length: number;
  radius_of_gyration: number;
  end_conditions: string;
}

export const serviceabilityApi = {
  checkDeflection: async (data: DeflectionCheckRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/serviceability/deflection', data);
    return response.data.data!;
  },

  checkCrackWidth: async (data: CrackWidthCheckRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/serviceability/crack-width', data);
    return response.data.data!;
  },

  checkVibration: async (data: VibrationCheckRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/serviceability/vibration', data);
    return response.data.data!;
  },

  checkPunchingShear: async (data: PunchingShearCheckRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/serviceability/punching-shear', data);
    return response.data.data!;
  },

  checkFatigue: async (data: FatigueCheckRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/serviceability/fatigue', data);
    return response.data.data!;
  },

  checkSlenderness: async (data: SlendernessCheckRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/serviceability/slenderness', data);
    return response.data.data!;
  },
};
