import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export const windApi = {
  calculateDesignPressure: async (data: any): Promise<any> => {
    const response = await apiClient.post<ApiResponse>('/api/wind/design-pressure', data);
    return response.data.data!;
  },

  calculateWindForces: async (data: any): Promise<any> => {
    const response = await apiClient.post<ApiResponse>('/api/wind/wind-forces', data);
    return response.data.data!;
  },

  calculateGustFactor: async (data: any): Promise<any> => {
    const response = await apiClient.post<ApiResponse>('/api/wind/gust-factor', data);
    return response.data.data!;
  },

  calculateAlongWindResponse: async (data: any): Promise<any> => {
    const response = await apiClient.post<ApiResponse>('/api/wind/along-wind-response', data);
    return response.data.data!;
  },

  calculateAcrossWindResponse: async (data: any): Promise<any> => {
    const response = await apiClient.post<ApiResponse>('/api/wind/across-wind-response', data);
    return response.data.data!;
  },

  generateLoadCombinations: async (data: any): Promise<any> => {
    const response = await apiClient.post<ApiResponse>('/api/wind/load-combinations', data);
    return response.data.data!;
  },

  calculateCladdingPressure: async (data: any): Promise<any> => {
    const response = await apiClient.post<ApiResponse>('/api/wind/cladding-pressure', data);
    return response.data.data!;
  },

  getCodes: async (): Promise<any> => {
    const response = await apiClient.get<ApiResponse>('/api/wind/codes');
    return response.data.data!;
  },

  getDefaultParameters: async (): Promise<any> => {
    const response = await apiClient.get<ApiResponse>('/api/wind/parameters/defaults');
    return response.data.data!;
  },

  getIndiaWindZones: async (): Promise<any> => {
    const response = await apiClient.get<ApiResponse>('/api/wind/wind-zones/india');
    return response.data.data!;
  },

  calculateDynamicResponse: async (data: any): Promise<any> => {
    const response = await apiClient.post<ApiResponse>('/api/wind/dynamic-response', data);
    return response.data.data!;
  },
};
