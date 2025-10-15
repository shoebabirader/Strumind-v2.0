import React, { useState } from 'react'
import { X, Plus, Zap } from 'lucide-react'
import { useModel } from '@/contexts/ModelContext'

interface LoadDialogProps {
  isOpen: boolean
  onClose: () => void
}

export default function LoadDialog({ isOpen, onClose }: LoadDialogProps) {
  const { nodes, elements } = useModel()
  const [activeTab, setActiveTab] = useState('nodal')
  const [nodalLoad, setNodalLoad] = useState({
    nodeId: '',
    fx: 0,
    fy: 0,
    fz: 0,
    mx: 0,
    my: 0,
    mz: 0,
    loadCase: 'DL'
  })
  const [elementLoad, setElementLoad] = useState({
    elementId: '',
    loadType: 'uniform',
    direction: 'global-y',
    magnitude: 0,
    loadCase: 'DL'
  })

  if (!isOpen) return null

  const handleAddNodalLoad = (e: React.FormEvent) => {
    e.preventDefault()
    console.log('Adding nodal load:', nodalLoad)
    onClose()
  }

  const handleAddElementLoad = (e: React.FormEvent) => {
    e.preventDefault()
    console.log('Adding element load:', elementLoad)
    onClose()
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="panel w-full max-w-2xl">
        <div className="panel-header">
          <span><Zap className="w-4 h-4 inline mr-2" />Define Loads</span>
          <button onClick={onClose} className="toolbar-button">
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Tabs */}
        <div className="flex border-b" style={{ borderColor: 'var(--border-primary)' }}>
          <button
            onClick={() => setActiveTab('nodal')}
            className={`px-6 py-3 font-medium transition-colors ${
              activeTab === 'nodal' ? 'border-b-2 border-blue-500' : ''
            }`}
            style={{ color: activeTab === 'nodal' ? 'var(--accent-blue)' : 'var(--text-secondary)' }}
          >
            Nodal Loads
          </button>
          <button
            onClick={() => setActiveTab('element')}
            className={`px-6 py-3 font-medium transition-colors ${
              activeTab === 'element' ? 'border-b-2 border-blue-500' : ''
            }`}
            style={{ color: activeTab === 'element' ? 'var(--accent-blue)' : 'var(--text-secondary)' }}
          >
            Element Loads
          </button>
        </div>

        <div className="p-6">
          {activeTab === 'nodal' && (
            <form onSubmit={handleAddNodalLoad} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1" style={{ color: 'var(--text-secondary)' }}>Node</label>
                  <select
                    value={nodalLoad.nodeId}
                    onChange={(e) => setNodalLoad({ ...nodalLoad, nodeId: e.target.value })}
                    required
                  >
                    <option value="">Select Node</option>
                    {nodes.map((node) => (
                      <option key={node.id} value={node.id}>
                        {node.id} ({node.x}, {node.y}, {node.z})
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1" style={{ color: 'var(--text-secondary)' }}>Load Case</label>
                  <select
                    value={nodalLoad.loadCase}
                    onChange={(e) => setNodalLoad({ ...nodalLoad, loadCase: e.target.value })}
                  >
                    <option value="DL">Dead Load (DL)</option>
                    <option value="LL">Live Load (LL)</option>
                    <option value="WL">Wind Load (WL)</option>
                    <option value="EQ">Earthquake (EQ)</option>
                    <option value="SL">Snow Load (SL)</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>Forces (kN)</label>
                <div className="grid grid-cols-3 gap-3">
                  <div>
                    <label className="block text-xs mb-1" style={{ color: 'var(--text-tertiary)' }}>FX</label>
                    <input
                      type="number"
                      step="0.01"
                      value={nodalLoad.fx}
                      onChange={(e) => setNodalLoad({ ...nodalLoad, fx: parseFloat(e.target.value) || 0 })}
                    />
                  </div>
                  <div>
                    <label className="block text-xs mb-1" style={{ color: 'var(--text-tertiary)' }}>FY</label>
                    <input
                      type="number"
                      step="0.01"
                      value={nodalLoad.fy}
                      onChange={(e) => setNodalLoad({ ...nodalLoad, fy: parseFloat(e.target.value) || 0 })}
                    />
                  </div>
                  <div>
                    <label className="block text-xs mb-1" style={{ color: 'var(--text-tertiary)' }}>FZ</label>
                    <input
                      type="number"
                      step="0.01"
                      value={nodalLoad.fz}
                      onChange={(e) => setNodalLoad({ ...nodalLoad, fz: parseFloat(e.target.value) || 0 })}
                    />
                  </div>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>Moments (kN·m)</label>
                <div className="grid grid-cols-3 gap-3">
                  <div>
                    <label className="block text-xs mb-1" style={{ color: 'var(--text-tertiary)' }}>MX</label>
                    <input
                      type="number"
                      step="0.01"
                      value={nodalLoad.mx}
                      onChange={(e) => setNodalLoad({ ...nodalLoad, mx: parseFloat(e.target.value) || 0 })}
                    />
                  </div>
                  <div>
                    <label className="block text-xs mb-1" style={{ color: 'var(--text-tertiary)' }}>MY</label>
                    <input
                      type="number"
                      step="0.01"
                      value={nodalLoad.my}
                      onChange={(e) => setNodalLoad({ ...nodalLoad, my: parseFloat(e.target.value) || 0 })}
                    />
                  </div>
                  <div>
                    <label className="block text-xs mb-1" style={{ color: 'var(--text-tertiary)' }}>MZ</label>
                    <input
                      type="number"
                      step="0.01"
                      value={nodalLoad.mz}
                      onChange={(e) => setNodalLoad({ ...nodalLoad, mz: parseFloat(e.target.value) || 0 })}
                    />
                  </div>
                </div>
              </div>

              <div className="flex justify-end space-x-3 pt-4">
                <button type="button" onClick={onClose} className="btn-secondary">
                  Cancel
                </button>
                <button type="submit" className="btn-primary">
                  <Plus className="w-4 h-4 mr-2" />
                  Add Load
                </button>
              </div>
            </form>
          )}

          {activeTab === 'element' && (
            <form onSubmit={handleAddElementLoad} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1" style={{ color: 'var(--text-secondary)' }}>Element</label>
                  <select
                    value={elementLoad.elementId}
                    onChange={(e) => setElementLoad({ ...elementLoad, elementId: e.target.value })}
                    required
                  >
                    <option value="">Select Element</option>
                    {elements.map((elem) => (
                      <option key={elem.id} value={elem.id}>
                        {elem.id} ({elem.type})
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1" style={{ color: 'var(--text-secondary)' }}>Load Case</label>
                  <select
                    value={elementLoad.loadCase}
                    onChange={(e) => setElementLoad({ ...elementLoad, loadCase: e.target.value })}
                  >
                    <option value="DL">Dead Load (DL)</option>
                    <option value="LL">Live Load (LL)</option>
                    <option value="WL">Wind Load (WL)</option>
                    <option value="EQ">Earthquake (EQ)</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1" style={{ color: 'var(--text-secondary)' }}>Load Type</label>
                  <select
                    value={elementLoad.loadType}
                    onChange={(e) => setElementLoad({ ...elementLoad, loadType: e.target.value })}
                  >
                    <option value="uniform">Uniform</option>
                    <option value="point">Point</option>
                    <option value="trapezoidal">Trapezoidal</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1" style={{ color: 'var(--text-secondary)' }}>Direction</label>
                  <select
                    value={elementLoad.direction}
                    onChange={(e) => setElementLoad({ ...elementLoad, direction: e.target.value })}
                  >
                    <option value="global-x">Global X</option>
                    <option value="global-y">Global Y</option>
                    <option value="global-z">Global Z</option>
                    <option value="local-x">Local X</option>
                    <option value="local-y">Local Y</option>
                    <option value="local-z">Local Z</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-1" style={{ color: 'var(--text-secondary)' }}>Magnitude (kN/m)</label>
                <input
                  type="number"
                  step="0.01"
                  value={elementLoad.magnitude}
                  onChange={(e) => setElementLoad({ ...elementLoad, magnitude: parseFloat(e.target.value) || 0 })}
                  required
                />
              </div>

              <div className="flex justify-end space-x-3 pt-4">
                <button type="button" onClick={onClose} className="btn-secondary">
                  Cancel
                </button>
                <button type="submit" className="btn-primary">
                  <Plus className="w-4 h-4 mr-2" />
                  Add Load
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  )
}
