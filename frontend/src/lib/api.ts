import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const modelAPI = {
  create: (data: any) => api.post('/api/model/create', data),
  get: (id: number) => api.get(`/api/model/${id}`),
}

export const analysisAPI = {
  run: (data: any) => api.post('/api/analysis/run', data),
}

export const designAPI = {
  run: (data: any) => api.post('/api/design/run', data),
}

export const detailingAPI = {
  generate: (data: any) => api.post('/api/detailing/generate', data),
}

export const mlAPI = {
  predict: (data: any) => api.post('/api/ml/predict', data),
  train: (data: any) => api.post('/api/ml/train', data),
}

export const bimAPI = {
  exportIFC: (data: any) => api.post('/api/bim/export/ifc', data),
  importIFC: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/api/bim/import/ifc', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  generateScene: (data: any) => api.post('/api/bim/visualization/scene', data),
}

export default api
