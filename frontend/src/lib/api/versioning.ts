import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export interface VersionCreate {
  project_id: number;
  version_name: string;
  description?: string;
}

export interface Version {
  id: number;
  project_id: number;
  version_number: number;
  version_name: string;
  description?: string;
  created_at: string;
  created_by: string;
}

export const versioningApi = {
  createVersion: async (data: VersionCreate): Promise<Version> => {
    const response = await apiClient.post<ApiResponse<Version>>('/versions', data);
    return response.data.data!;
  },

  listVersions: async (projectId: number): Promise<Version[]> => {
    const response = await apiClient.get<ApiResponse<Version[]>>(`/projects/${projectId}/versions`);
    return response.data.data!;
  },

  getVersion: async (versionId: number): Promise<any> => {
    const response = await apiClient.get<ApiResponse<any>>(`/versions/${versionId}`);
    return response.data.data!;
  },

  restoreVersion: async (projectId: number, versionNumber: number): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>(`/projects/${projectId}/restore/${versionNumber}`);
    return response.data.data!;
  },

  compareVersions: async (projectId: number, version1: number, version2: number): Promise<any> => {
    const response = await apiClient.get<ApiResponse<any>>(`/projects/${projectId}/versions/compare/${version1}/${version2}`);
    return response.data.data!;
  },
};
