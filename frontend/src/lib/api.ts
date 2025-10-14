import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Basic APIs
export const modelAPI = {
  create: (data: any) => api.post('/api/model/create', data),
  get: (id: number) => api.get(`/api/model/${id}`),
}

export const analysisAPI = {
  run: (data: any) => api.post('/api/analysis/run', data),
  modal: (data: any) => api.post('/api/analysis/modal', data),
  static: (data: any) => api.post('/api/analysis/static', data),
}

export const designAPI = {
  run: (data: any) => api.post('/api/design/run', data),
  beam: (data: any) => api.post('/api/design/beam', data),
  column: (data: any) => api.post('/api/design/column', data),
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

// Advanced Analysis APIs
export const advancedAnalysisAPI = {
  timeHistory: (data: any) => api.post('/api/advanced-analysis/time-history', data),
  buckling: (data: any) => api.post('/api/advanced-analysis/buckling', data),
  loadCombinations: (data: any) => api.post('/api/advanced-analysis/load-combinations', data),
  envelope: (data: any) => api.post('/api/advanced-analysis/envelope', data),
  steelSections: (standard: string, sectionType?: string) => 
    api.get(`/api/advanced-analysis/steel-sections/${standard}${sectionType ? `?section_type=${sectionType}` : ''}`),
  slabDesign: (data: any) => api.post('/api/advanced-analysis/slab-design', data),
  momentDiagram: (data: any) => api.post('/api/advanced-analysis/results/moment-diagram', data),
  shearDiagram: (data: any) => api.post('/api/advanced-analysis/results/shear-diagram', data),
  deflectionCurve: (data: any) => api.post('/api/advanced-analysis/results/deflection-curve', data),
}

// Specialized Design APIs
export const specializedDesignAPI = {
  shearWall: (data: any) => api.post('/api/specialized-design/shear-wall', data),
  couplingBeam: (data: any) => api.post('/api/specialized-design/coupling-beam', data),
  retainingWall: (data: any) => api.post('/api/specialized-design/retaining-wall', data),
  staircase: (data: any) => api.post('/api/specialized-design/staircase', data),
  compositeBeam: (data: any) => api.post('/api/specialized-design/composite-beam', data),
  compositeColumn: (data: any) => api.post('/api/specialized-design/composite-column', data),
  movingLoad: (data: any) => api.post('/api/specialized-design/moving-load', data),
  temperatureAnalysis: (data: any) => api.post('/api/specialized-design/temperature-analysis', data),
  meshGenerate: (data: any) => api.post('/api/specialized-design/mesh/generate', data),
  meshRefine: (data: any) => api.post('/api/specialized-design/mesh/refine', data),
  meshQualityCheck: (data: any) => api.post('/api/specialized-design/mesh/quality-check', data),
}

// Serviceability Checks APIs
export const serviceabilityAPI = {
  deflection: (data: any) => api.post('/api/serviceability/deflection', data),
  crackWidth: (data: any) => api.post('/api/serviceability/crack-width', data),
  vibration: (data: any) => api.post('/api/serviceability/vibration', data),
  punchingShear: (data: any) => api.post('/api/serviceability/punching-shear', data),
  fatigue: (data: any) => api.post('/api/serviceability/fatigue', data),
  slenderness: (data: any) => api.post('/api/serviceability/slenderness', data),
}

// Seismic & Wind APIs
export const seismicAPI = {
  analyze: (data: any) => api.post('/api/seismic/analyze', data),
  responseSpectrum: (data: any) => api.post('/api/seismic/response-spectrum', data),
}

export const windAPI = {
  analyze: (data: any) => api.post('/api/wind/analyze', data),
  pressureCoefficients: (data: any) => api.post('/api/wind/pressure-coefficients', data),
}

// P-Delta Analysis
export const pDeltaAPI = {
  analyze: (data: any) => api.post('/api/pdelta/analyze', data),
}

// Steel Connections
export const connectionsAPI = {
  design: (data: any) => api.post('/api/connections/design', data),
}

// Reporting
export const reportingAPI = {
  generate: (data: any) => api.post('/api/reporting/generate', data),
  export: (format: string, data: any) => api.post(`/api/reporting/export/${format}`, data),
}

// Templates
export const templatesAPI = {
  list: () => api.get('/api/templates/list'),
  get: (id: string) => api.get(`/api/templates/${id}`),
  create: (data: any) => api.post('/api/templates/create', data),
}

export default api
