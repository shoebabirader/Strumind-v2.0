import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Authentication APIs
export const authAPI = {
  login: (username: string, password: string) => {
    const formData = new FormData()
    formData.append('username', username)
    formData.append('password', password)
    return api.post('/api/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
  },
  register: (data: any) => api.post('/api/auth/register', data),
  me: () => api.get('/api/auth/me'),
  logout: () => api.post('/api/auth/logout'),
}

// Node APIs
export const nodeAPI = {
  create: (data: any) => api.post('/api/nodes/create', data),
  list: (projectId: number) => api.get(`/api/nodes/list/${projectId}`),
  get: (id: number) => api.get(`/api/nodes/${id}`),
  update: (id: number, data: any) => api.put(`/api/nodes/${id}`, data),
  delete: (id: number) => api.delete(`/api/nodes/${id}`),
}

// Element APIs
export const elementAPI = {
  create: (data: any) => api.post('/api/elements/create', data),
  list: (projectId: number) => api.get(`/api/elements/list/${projectId}`),
  get: (id: number) => api.get(`/api/elements/${id}`),
  update: (id: number, data: any) => api.put(`/api/elements/${id}`, data),
  delete: (id: number) => api.delete(`/api/elements/${id}`),
}

// Material APIs
export const materialAPI = {
  create: (data: any) => api.post('/api/materials/create', data),
  list: (projectId: number) => api.get(`/api/materials/list/${projectId}`),
  get: (id: number) => api.get(`/api/materials/${id}`),
  update: (id: number, data: any) => api.put(`/api/materials/${id}`, data),
  delete: (id: number) => api.delete(`/api/materials/${id}`),
  library: () => api.get('/api/materials/library'),
}

// Load APIs
export const loadAPI = {
  create: (data: any) => api.post('/api/loads/create', data),
  createNodal: (data: any) => api.post('/api/loads/nodal', data),
  createElement: (data: any) => api.post('/api/loads/element', data),
  list: (projectId: number) => api.get(`/api/loads/list/${projectId}`),
  get: (id: number) => api.get(`/api/loads/${id}`),
  update: (id: number, data: any) => api.put(`/api/loads/${id}`, data),
  delete: (id: number) => api.delete(`/api/loads/${id}`),
}

// Section APIs
export const sectionAPI = {
  create: (data: any) => api.post('/api/sections/create', data),
  list: (projectId: number) => api.get(`/api/sections/list/${projectId}`),
  get: (id: number) => api.get(`/api/sections/${id}`),
  update: (id: number, data: any) => api.put(`/api/sections/${id}`, data),
  delete: (id: number) => api.delete(`/api/sections/${id}`),
  library: () => api.get('/api/sections/library'),
}

// Model APIs
export const modelAPI = {
  create: (data: any) => api.post('/api/model/create', data),
  get: (id: number) => api.get(`/api/model/${id}`),
  update: (id: number, data: any) => api.put(`/api/model/${id}`, data),
  save: (data: any) => api.post('/api/model/save', data),
  load: (id: number) => api.get(`/api/model/load/${id}`),
}

// Analysis APIs
export const analysisAPI = {
  run: (data: any) => api.post('/api/analysis/run', data),
  static: (data: any) => api.post('/api/analysis/static', data),
  modal: (data: any) => api.post('/api/analysis/modal', data),
  dynamic: (data: any) => api.post('/api/analysis/dynamic', data),
  buckling: (data: any) => api.post('/api/analysis/buckling', data),
  nonlinear: (data: any) => api.post('/api/analysis/nonlinear', data),
}

// Design APIs
export const designAPI = {
  beam: (data: any) => api.post('/api/design/beam', data),
  column: (data: any) => api.post('/api/design/column', data),
  foundation: (data: any) => api.post('/api/design/foundation', data),
  slab: (data: any) => api.post('/api/design/slab', data),
}

// Project APIs
export const projectAPI = {
  create: (data: any) => api.post('/api/projects/create', data),
  list: () => api.get('/api/projects/list'),
  get: (id: number) => api.get(`/api/projects/${id}`),
  update: (id: number, data: any) => api.put(`/api/projects/${id}`, data),
  delete: (id: number) => api.delete(`/api/projects/${id}`),
}

export default api
