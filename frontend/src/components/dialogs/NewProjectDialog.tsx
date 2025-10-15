import React, { useState } from 'react'
import { X, FolderPlus } from 'lucide-react'

interface NewProjectDialogProps {
  isOpen: boolean
  onClose: () => void
  onCreateProject: (project: any) => void
}

export default function NewProjectDialog({ isOpen, onClose, onCreateProject }: NewProjectDialogProps) {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    units: 'metric',
    code: 'IS456',
    template: 'blank'
  })

  if (!isOpen) return null

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onCreateProject(formData)
    onClose()
    setFormData({ name: '', description: '', units: 'metric', code: 'IS456', template: 'blank' })
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="panel w-full max-w-2xl">
        <div className="panel-header">
          <span><FolderPlus className="w-4 h-4 inline mr-2" />New Project</span>
          <button onClick={onClose} className="toolbar-button">
            <X className="w-4 h-4" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1" style={{ color: 'var(--text-secondary)' }}>Project Name</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
              placeholder="My Building Project"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1" style={{ color: 'var(--text-secondary)' }}>Description</label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              rows={3}
              placeholder="Brief description of the project..."
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1" style={{ color: 'var(--text-secondary)' }}>Unit System</label>
              <select
                value={formData.units}
                onChange={(e) => setFormData({ ...formData, units: e.target.value })}
              >
                <option value="metric">Metric (kN, m)</option>
                <option value="imperial">Imperial (kip, ft)</option>
                <option value="si">SI (N, m)</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1" style={{ color: 'var(--text-secondary)' }}>Design Code</label>
              <select
                value={formData.code}
                onChange={(e) => setFormData({ ...formData, code: e.target.value })}
              >
                <option value="IS456">IS 456:2000 (India)</option>
                <option value="ACI318">ACI 318 (USA)</option>
                <option value="EC2">Eurocode 2 (Europe)</option>
                <option value="BS8110">BS 8110 (UK)</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>Project Template</label>
            <div className="grid grid-cols-2 gap-3">
              {[
                { value: 'blank', label: 'Blank Project', desc: 'Start from scratch' },
                { value: 'building', label: 'Building Frame', desc: 'Multi-story building' },
                { value: 'bridge', label: 'Bridge', desc: 'Bridge structure' },
                { value: 'truss', label: 'Truss', desc: 'Truss structure' },
              ].map((template) => (
                <label
                  key={template.value}
                  className={`panel p-3 cursor-pointer transition-all ${
                    formData.template === template.value ? 'border-blue-500' : ''
                  }`}
                >
                  <input
                    type="radio"
                    name="template"
                    value={template.value}
                    checked={formData.template === template.value}
                    onChange={(e) => setFormData({ ...formData, template: e.target.value })}
                    className="mr-2"
                  />
                  <div>
                    <div className="font-medium text-sm">{template.label}</div>
                    <div className="text-xs" style={{ color: 'var(--text-tertiary)' }}>{template.desc}</div>
                  </div>
                </label>
              ))}
            </div>
          </div>

          <div className="flex justify-end space-x-3 pt-4">
            <button type="button" onClick={onClose} className="btn-secondary">
              Cancel
            </button>
            <button type="submit" className="btn-primary">
              <FolderPlus className="w-4 h-4 mr-2" />
              Create Project
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
