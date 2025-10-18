import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export interface FeedbackSubmission {
  model_type: string;
  prediction: any;
  actual: any;
  user_rating?: number;
  comments?: string;
}

export interface RetrainingRequest {
  model_type: string;
  epochs?: number;
}

export const learningApi = {
  submitFeedback: async (data: FeedbackSubmission): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/learning/feedback/submit', data);
    return response.data.data!;
  },

  triggerRetraining: async (data: RetrainingRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/learning/retrain', data);
    return response.data.data!;
  },

  listModelVersions: async (): Promise<any> => {
    const response = await apiClient.get<ApiResponse<any>>('/learning/models/versions');
    return response.data.data!;
  },

  getLatestModel: async (modelType: string): Promise<any> => {
    const response = await apiClient.get<ApiResponse<any>>(`/learning/models/${modelType}/latest`);
    return response.data.data!;
  },
};
