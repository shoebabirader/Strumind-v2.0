import React, { useState } from 'react'
import { X, Play, Settings } from 'lucide-react'
import { analysisAPI } from '@/lib/api'
import { useModel } from '@/contexts/ModelContext'

interface AnalysisDialogProps {
  isOpen: boolean
  onClose: () => void
  onRunAnalysis: (config: any) => void
}

export default function AnalysisDialog({ isOpen, onClose, onRunAnalysis }: AnalysisDialogProps) {
  const { nodes, elements, materials } = useModel()
  const [config, setConfig] = useState({
    analysisType: 'static',
    solver: 'direct',
    loadCombinations: ['1.2DL + 1.6LL'],
    includeGeometricNonlinearity: false,
    includePDelta: false,
    convergenceTolerance: 0.001,
    maxIterations: 100,
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  if (!isOpen) return null

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    
    try {
      // Prepare model data for backend
      const modelData = {
        nodes: nodes.map(n => ({
          id: n.id,
          coordinates: [n.x, n.y, n.z],
          restraints: n.restraints
        })),
        elements: elements.map(e => ({
          id: e.id,
          node_i: e.nodeI,
          node_j: e.nodeJ,
          type: e.type,
          material_id: e.materialId,
          section: {
            type: e.sectionType,
            width: e.width,
            height: e.height
          }
        })),
        materials: materials.map(m => ({
          id: m.id,
          name: m.name,
          E: m.E,
          nu: m.nu,
          density: m.density
        })),
        analysis_config: config
      }
      
      // Call backend API
      const response = await analysisAPI.static(modelData)
      
      // Pass results to parent
      onRunAnalysis({
        ...config,
        results: response.data
      })
      
      onClose()
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail 
        ? (typeof err.response.data.detail === 'string' 
          ? err.response.data.detail 
          : JSON.stringify(err.response.data.detail))
        : 'Failed to run analysis'
      setError(errorMsg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="panel w-full max-w-2xl">
        <div className="panel-header">
          <span><Settings className="w-4 h-4 inline mr-2" />Analysis Settings</span>
          <button onClick={onClose} className="toolbar-button">
            <X className="w-4 h-4" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {/* Analysis Type */}
          <div>
            <label className="block text-sm font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>Analysis Type</label>
            <div className="grid grid-cols-2 gap-3">
              {[
                { value: 'static', label: 'Static Linear', desc: 'Standard linear analysis' },
                { value: 'dynamic', label: 'Dynamic', desc: 'Time history or modal' },
                { value: 'buckling', label: 'Buckling', desc: 'Eigenvalue buckling' },
                { value: 'nonlinear', label: 'Nonlinear', desc: 'Geometric nonlinearity' },
              ].map((type) => (
                <label
                  key={type.value}
                  className={`panel p-3 cursor-pointer transition-all ${
                    config.analysisType === type.value ? 'border-blue-500' : ''
                  }`}
                >
                  <input
                    type="radio"
                    name="analysisType"
                    value={type.value}
                    checked={config.analysisType === type.value}
                    onChange={(e) => setConfig({ ...config, analysisType: e.target.value })}
                    className="mr-2"
                  />
                  <div>
                    <div className="font-medium">{type.label}</div>
                    <div className="text-xs" style={{ color: 'var(--text-tertiary)' }}>{type.desc}</div>
                  </div>
                </label>
              ))}
            </div>
          </div>

          {/* Solver */}
          <div>
            <label className="block text-sm font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>Solver Method</label>
            <select
              value={config.solver}
              onChange={(e) => setConfig({ ...config, solver: e.target.value })}
              className="w-full"
            >
              <option value="direct">Direct (Skyline)</option>
              <option value="iterative">Iterative (PCG)</option>
              <option value="sparse">Sparse (PARDISO)</option>
            </select>
          </div>

          {/* Load Combinations */}
          <div>
            <label className="block text-sm font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>Load Combinations</label>
            <div className="space-y-2">
              {[
                '1.4DL',
                '1.2DL + 1.6LL',
                '1.2DL + 1.0LL + 1.0WL',
                '1.2DL + 1.0LL + 1.0EQ',
                '0.9DL + 1.0WL',
              ].map((combo) => (
                <label key={combo} className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={config.loadCombinations.includes(combo)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setConfig({ ...config, loadCombinations: [...config.loadCombinations, combo] })
                      } else {
                        setConfig({ ...config, loadCombinations: config.loadCombinations.filter((c) => c !== combo) })
                      }
                    }}
                    className="rounded"
                  />
                  <span className="text-sm">{combo}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Advanced Options */}
          <div>
            <label className="block text-sm font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>Advanced Options</label>
            <div className="space-y-2">
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={config.includeGeometricNonlinearity}
                  onChange={(e) => setConfig({ ...config, includeGeometricNonlinearity: e.target.checked })}
                  className="rounded"
                />
                <span className="text-sm">Include Geometric Nonlinearity</span>
              </label>
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={config.includePDelta}
                  onChange={(e) => setConfig({ ...config, includePDelta: e.target.checked })}
                  className="rounded"
                />
                <span className="text-sm">Include P-Delta Effects</span>
              </label>
            </div>
          </div>

          {/* Convergence */}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1" style={{ color: 'var(--text-secondary)' }}>Convergence Tolerance</label>
              <input
                type="number"
                step="0.0001"
                value={config.convergenceTolerance}
                onChange={(e) => setConfig({ ...config, convergenceTolerance: parseFloat(e.target.value) })}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1" style={{ color: 'var(--text-secondary)' }}>Max Iterations</label>
              <input
                type="number"
                value={config.maxIterations}
                onChange={(e) => setConfig({ ...config, maxIterations: parseInt(e.target.value) })}
              />
            </div>
          </div>

          {error && (
            <div className="p-3 rounded" style={{ background: 'var(--accent-red)', color: 'white' }}>
              {error}
            </div>
          )}

          <div className="flex justify-end space-x-3 pt-4">
            <button type="button" onClick={onClose} className="btn-secondary" disabled={loading}>
              Cancel
            </button>
            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Running Analysis...
                </>
              ) : (
                <>
                  <Play className="w-4 h-4 mr-2" />
                  Run Analysis
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
