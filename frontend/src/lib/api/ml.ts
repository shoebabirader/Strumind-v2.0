import { apiClient } from './client';
import type { ApiResponse } from '@/types/api';

export interface MLPredictRequest {
  model_type: 'beam_design' | 'column_design' | 'load_prediction';
  input_features: Record<string, number>;
}

export interface MLTrainRequest {
  model_type: string;
  training_data: Array<Record<string, any>>;
  epochs?: number;
  validation_split?: number;
}

export const mlApi = {
  predict: async (data: MLPredictRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/ml/predict', data);
    return response.data.data!;
  },

  train: async (data: MLTrainRequest): Promise<any> => {
    const response = await apiClient.post<ApiResponse<any>>('/ml/train', data);
    return response.data.data!;
  },
};
