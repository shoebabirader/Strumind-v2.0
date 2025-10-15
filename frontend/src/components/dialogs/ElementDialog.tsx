import React, { useState } from 'react'
import { X, Plus } from 'lucide-react'
import { useModel } from '@/contexts/ModelContext'
import api from '@/lib/api'

interface ElementDialogProps {
  isOpen: boolean
  onClose: () => void
  elementToEdit?: any
}

export default function ElementDialog({ isOpen, onClose, elementToEdit }: ElementDialogProps) {
  const { addElement, nodes, materials } = useModel()
  const [formData, setFormData] = useState({
    id: elementToEdit?.id || '',
    nodeI: elementToEdit?.nodeI || '',
    nodeJ: elementToEdit?.nodeJ || '',
    type: elementToEdit?.type || 'beam',
    materialId: elementToEdit?.materialId || '',
    sectionType: elementToEdit?.sectionType || 'rectangular',
    width: elementToEdit?.width || 0.3,
    height: elementToEdit?.height || 0.5,
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  if (!isOpen) return null

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    
    try {
      const elementData = {
        ...formData,
        width: parseFloat(formData.width as any),
        height: parseFloat(formData.height as any),
      }
      
      // Save to backend
      await api.post('/api/elements/create', elementData)
      
      // Add to local state
      addElement(elementData)
      
      onClose()
      setFormData({ id: '', nodeI: '', nodeJ: '', type: 'beam', materialId: '', sectionType: 'rectangular', width: 0.3, height: 0.5 })
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail 
        ? (typeof err.response.data.detail === 'string' 
          ? err.response.data.detail 
          : JSON.stringify(err.response.data.detail))
        : 'Failed to add element'
      setError(errorMsg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="panel w-full max-w-lg">
        <div className="panel-header">
          <span>{elementToEdit ? 'Edit Element' : 'Add Element'}</span>
          <button onClick={onClose} className="toolbar-button">
            <X className="w-4 h-4" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1" style={{ color: 'var(--text-secondary)' }}>Element ID</label>
              <input
                type="text"
                value={formData.id}
                onChange={(e) => setFormData({ ...formData, id: e.target.value })}
                required
                placeholder="E1"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1" style={{ color: 'var(--text-secondary)' }}>Type</label>
              <select
                value={formData.type}
                onChange={(e) => setFormData({ ...formData, type: e.target.value })}
              >
                <option value="beam">Beam</option>
                <option value="column">Column</option>
                <option value="brace">Brace</option>
                <option value="truss">Truss</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1" style={{ color: 'var(--text-secondary)' }}>Node I</label>
              <select
                value={formData.nodeI}
                onChange={(e) => setFormData({ ...formData, nodeI: e.target.value })}
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
              <label className="block text-sm font-medium mb-1" style={{ color: 'var(--text-secondary)' }}>Node J</label>
              <select
                value={formData.nodeJ}
                onChange={(e) => setFormData({ ...formData, nodeJ: e.target.value })}
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
          </div>

          <div>
            <label className="block text-sm font-medium mb-1" style={{ color: 'var(--text-secondary)' }}>Material</label>
            <select
              value={formData.materialId}
              onChange={(e) => setFormData({ ...formData, materialId: e.target.value })}
              required
            >
              <option value="">Select Material</option>
              {materials.map((material) => (
                <option key={material.id} value={material.id}>
                  {material.name} (E={material.E} MPa)
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>Section Properties</label>
            <div className="grid grid-cols-3 gap-3">
              <div>
                <label className="block text-xs mb-1" style={{ color: 'var(--text-tertiary)' }}>Type</label>
                <select
                  value={formData.sectionType}
                  onChange={(e) => setFormData({ ...formData, sectionType: e.target.value })}
                >
                  <option value="rectangular">Rectangular</option>
                  <option value="circular">Circular</option>
                  <option value="i-section">I-Section</option>
                  <option value="t-section">T-Section</option>
                </select>
              </div>
              <div>
                <label className="block text-xs mb-1" style={{ color: 'var(--text-tertiary)' }}>Width (m)</label>
                <input
                  type="number"
                  step="0.01"
                  value={formData.width}
                  onChange={(e) => setFormData({ ...formData, width: e.target.value as any })}
                  required
                />
              </div>
              <div>
                <label className="block text-xs mb-1" style={{ color: 'var(--text-tertiary)' }}>Height (m)</label>
                <input
                  type="number"
                  step="0.01"
                  value={formData.height}
                  onChange={(e) => setFormData({ ...formData, height: e.target.value as any })}
                  required
                />
              </div>
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
                  Adding...
                </>
              ) : (
                <>
                  <Plus className="w-4 h-4 mr-2" />
                  {elementToEdit ? 'Update' : 'Add'} Element
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
