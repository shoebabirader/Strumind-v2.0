import React, { useState } from 'react'
import { X, Plus } from 'lucide-react'
import { useModel } from '@/contexts/ModelContext'
import api from '@/lib/api'

interface NodeDialogProps {
  isOpen: boolean
  onClose: () => void
  nodeToEdit?: any
}

export default function NodeDialog({ isOpen, onClose, nodeToEdit }: NodeDialogProps) {
  const { addNode, currentProjectId } = useModel()
  const [formData, setFormData] = useState({
    node_id: nodeToEdit?.node_id || '',
    x: nodeToEdit?.x || 0,
    y: nodeToEdit?.y || 0,
    z: nodeToEdit?.z || 0,
    restraints: nodeToEdit?.restraints || [false, false, false, false, false, false],
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  if (!isOpen) return null

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    
    try {
      if (!currentProjectId) {
        setError('No project selected. Please create or open a project first.')
        setLoading(false)
        return
      }

      const nodeData = {
        project_id: currentProjectId,
        node_id: formData.node_id,
        x: parseFloat(formData.x as any),
        y: parseFloat(formData.y as any),
        z: parseFloat(formData.z as any),
        restraints: formData.restraints,
      }
      
      // Save to backend
      const response = await api.post('/api/nodes/create', nodeData)
      
      // Add to local state
      addNode(response.data)
      
      onClose()
      setFormData({ node_id: '', x: 0, y: 0, z: 0, restraints: [false, false, false, false, false, false] })
    } catch (err: any) {
      const errorMsg = err.response?.data?.detail 
        ? (typeof err.response.data.detail === 'string' 
          ? err.response.data.detail 
          : JSON.stringify(err.response.data.detail))
        : 'Failed to add node'
      setError(errorMsg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="panel w-full max-w-md">
        <div className="panel-header">
          <span>{nodeToEdit ? 'Edit Node' : 'Add Node'}</span>
          <button onClick={onClose} className="toolbar-button">
            <X className="w-4 h-4" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1" style={{ color: 'var(--text-secondary)' }}>Node ID</label>
            <input
              type="text"
              value={formData.node_id}
              onChange={(e) => setFormData({ ...formData, node_id: e.target.value })}
              required
              placeholder="N1"
            />
          </div>

          <div className="grid grid-cols-3 gap-3">
            <div>
              <label className="block text-sm font-medium mb-1" style={{ color: 'var(--text-secondary)' }}>X (m)</label>
              <input
                type="number"
                step="0.01"
                value={formData.x}
                onChange={(e) => setFormData({ ...formData, x: e.target.value as any })}
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1" style={{ color: 'var(--text-secondary)' }}>Y (m)</label>
              <input
                type="number"
                step="0.01"
                value={formData.y}
                onChange={(e) => setFormData({ ...formData, y: e.target.value as any })}
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1" style={{ color: 'var(--text-secondary)' }}>Z (m)</label>
              <input
                type="number"
                step="0.01"
                value={formData.z}
                onChange={(e) => setFormData({ ...formData, z: e.target.value as any })}
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>Restraints</label>
            <div className="grid grid-cols-3 gap-2">
              {['UX', 'UY', 'UZ', 'RX', 'RY', 'RZ'].map((dof, idx) => (
                <label key={dof} className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={formData.restraints[idx]}
                    onChange={(e) => {
                      const newRestraints = [...formData.restraints]
                      newRestraints[idx] = e.target.checked
                      setFormData({ ...formData, restraints: newRestraints })
                    }}
                    className="rounded"
                  />
                  <span className="text-sm">{dof}</span>
                </label>
              ))}
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
                  {nodeToEdit ? 'Update' : 'Add'} Node
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
