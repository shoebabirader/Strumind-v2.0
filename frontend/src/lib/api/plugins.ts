import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export interface Plugin {
  name: string;
  version: string;
  description: string;
  type: 'analysis' | 'design' | 'utility';
  enabled: boolean;
}

export const pluginsApi = {
  list: async (): Promise<Plugin[]> => {
    const response = await apiClient.get<ApiResponse<Plugin[]>>('/plugins');
    return response.data.data!;
  },

  getInfo: async (pluginName: string): Promise<Plugin> => {
    const response = await apiClient.get<ApiResponse<Plugin>>(`/plugins/${pluginName}`);
    return response.data.data!;
  },

  getByType: async (pluginType: string): Promise<Plugin[]> => {
    const response = await apiClient.get<ApiResponse<Plugin[]>>(`/plugins/type/${pluginType}`);
    return response.data.data!;
  },

  execute: async (pluginName: string, params: Record<string, any>): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>(`/plugins/${pluginName}/execute`, params);
    return response.data.data!;
  },

  runAnalysis: async (pluginName: string, modelData: any): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>(`/plugins/${pluginName}/analysis`, modelData);
    return response.data.data!;
  },

  runDesign: async (pluginName: string, designData: any): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>(`/plugins/${pluginName}/design`, designData);
    return response.data.data!;
  },

  reload: async (): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/plugins/reload');
    return response.data.data!;
  },

  listHooks: async (): Promise<any> => {
    const response = await apiClient.get<ApiResponse<any>>('/plugins/hooks/list');
    return response.data.data!;
  },

  triggerHook: async (hookName: string, data: any): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>(`/plugins/hooks/${hookName}/trigger`, data);
    return response.data.data!;
  },
};
