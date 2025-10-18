import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export const seismicApi = {
  calculateBaseShear: async (data: any): Promise<any> => {
    const response = await apiClient.post<ApiResponse>('/api/seismic/base-shear', data);
    return response.data.data!;
  },

  responseSpectrum: async (data: any): Promise<any> => {
    const response = await apiClient.post<ApiResponse>('/api/seismic/response-spectrum', data);
    return response.data.data!;
  },

  checkStoryDrift: async (data: any): Promise<any> => {
    const response = await apiClient.post<ApiResponse>('/api/seismic/story-drift-check', data);
    return response.data.data!;
  },

  distributeLoads: async (data: any): Promise<any> => {
    const response = await apiClient.post<ApiResponse>('/api/seismic/load-distribution', data);
    return response.data.data!;
  },

  checkTorsionalIrregularity: async (data: any): Promise<any> => {
    const response = await apiClient.post<ApiResponse>('/api/seismic/torsional-irregularity', data);
    return response.data.data!;
  },

  checkSoftStory: async (data: any): Promise<any> => {
    const response = await apiClient.post<ApiResponse>('/api/seismic/soft-story-check', data);
    return response.data.data!;
  },

  getCodes: async (): Promise<any> => {
    const response = await apiClient.get<ApiResponse>('/api/seismic/codes');
    return response.data.data!;
  },

  getDefaultParameters: async (): Promise<any> => {
    const response = await apiClient.get<ApiResponse>('/api/seismic/parameters/defaults');
    return response.data.data!;
  },
};
