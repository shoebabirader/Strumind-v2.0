import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export interface RayleighDampingRequest {
  mode1: number;
  mode2: number;
  damping_ratio1: number;
  damping_ratio2: number;
}

export interface ModalDampingRequest {
  modes: number[];
  damping_ratios: number[];
}

export interface ModalAnalysisRequest {
  model_id: number;
  num_modes?: number;
  frequency_range?: [number, number];
}

export interface FrequencyResponseRequest {
  model_id: number;
  frequency_range: [number, number];
  num_points?: number;
  damping_ratio?: number;
}

export const dynamicAnalysisApi = {
  calculateRayleighDamping: async (data: RayleighDampingRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/dynamic/rayleigh-damping', data);
    return response.data.data!;
  },

  calculateModalDamping: async (data: ModalDampingRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/dynamic/modal-damping', data);
    return response.data.data!;
  },

  performModalAnalysis: async (data: ModalAnalysisRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/dynamic/modal-analysis', data);
    return response.data.data!;
  },

  calculateFrequencyResponse: async (data: FrequencyResponseRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/dynamic/frequency-response', data);
    return response.data.data!;
  },

  listDampingModels: async (): Promise<any> => {
    const response = await apiClient.get<ApiResponse<any>>('/dynamic/damping-models');
    return response.data.data!;
  },

  listIntegrationMethods: async (): Promise<string[]> => {
    const response = await apiClient.get<ApiResponse<string[]>>('/dynamic/integration-methods');
    return response.data.data!;
  },

  runTimeHistory: async (data: any): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/dynamic/time-history', data);
    return response.data.data!;
  },

  runResponseSpectrum: async (data: any): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/dynamic/response-spectrum', data);
    return response.data.data!;
  },
};
