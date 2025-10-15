import React, { useState } from 'react'
import { X, Plus, Search } from 'lucide-react'
import { useModel } from '@/contexts/ModelContext'

interface MaterialDialogProps {
  isOpen: boolean
  onClose: () => void
}

const PREDEFINED_MATERIALS = [
  { id: 'concrete_m20', name: 'Concrete M20', E: 22000, nu: 0.2, density: 2500, type: 'concrete', fy: 20 },
  { id: 'concrete_m25', name: 'Concrete M25', E: 25000, nu: 0.2, density: 2500, type: 'concrete', fy: 25 },
  { id: 'concrete_m30', name: 'Concrete M30', E: 27000, nu: 0.2, density: 2500, type: 'concrete', fy: 30 },
  { id: 'steel_fe415', name: 'Steel Fe415', E: 200000, nu: 0.3, density: 7850, type: 'steel', fy: 415 },
  { id: 'steel_fe500', name: 'Steel Fe500', E: 200000, nu: 0.3, density: 7850, type: 'steel', fy: 500 },
  { id: 'steel_a36', name: 'Steel A36', E: 200000, nu: 0.3, density: 7850, type: 'steel', fy: 250 },
  { id: 'aluminum_6061', name: 'Aluminum 6061', E: 70000, nu: 0.33, density: 2700, type: 'aluminum', fy: 276 },
]

export default function MaterialDialog({ isOpen, onClose }: MaterialDialogProps) {
  const { materials, addMaterial } = useModel()
  const [searchTerm, setSearchTerm] = useState('')
  const [showAddForm, setShowAddForm] = useState(false)
  const [newMaterial, setNewMaterial] = useState({
    id: '',
    name: '',
    E: 0,
    nu: 0,
    density: 0,
    fy: 0,
    type: 'concrete'
  })

  if (!isOpen) return null

  const filteredMaterials = PREDEFINED_MATERIALS.filter(
    (mat) =>
      mat.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      mat.type.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const handleAddMaterial = () => {
    if (newMaterial.id && newMaterial.name) {
      addMaterial(newMaterial)
      setShowAddForm(false)
      setNewMaterial({ id: '', name: '', E: 0, nu: 0, density: 0, fy: 0, type: 'concrete' })
    }
  }

  const handleSelectMaterial = (material: any) => {
    if (!materials.find((m) => m.id === material.id)) {
      addMaterial(material)
    }
    onClose()
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="panel w-full max-w-4xl max-h-[80vh] flex flex-col">
        <div className="panel-header">
          <span>Material Library</span>
          <button onClick={onClose} className="toolbar-button">
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="p-6 space-y-4 flex-1 overflow-auto">
          {/* Search */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4" style={{ color: 'var(--text-tertiary)' }} />
            <input
              type="text"
              placeholder="Search materials..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>

          {/* Add Custom Material */}
          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="w-full p-3 border-2 border-dashed rounded hover:border-blue-500 transition-colors flex items-center justify-center"
            style={{ borderColor: 'var(--border-primary)' }}
          >
            <Plus className="w-4 h-4 mr-2" />
            Add Custom Material
          </button>

          {/* Add Material Form */}
          {showAddForm && (
            <div className="panel p-4 space-y-3">
              <div className="grid grid-cols-2 gap-3">
                <input
                  type="text"
                  placeholder="Material ID"
                  value={newMaterial.id}
                  onChange={(e) => setNewMaterial({ ...newMaterial, id: e.target.value })}
                />
                <input
                  type="text"
                  placeholder="Material Name"
                  value={newMaterial.name}
                  onChange={(e) => setNewMaterial({ ...newMaterial, name: e.target.value })}
                />
              </div>
              <div className="grid grid-cols-2 gap-3">
                <select
                  value={newMaterial.type}
                  onChange={(e) => setNewMaterial({ ...newMaterial, type: e.target.value })}
                >
                  <option value="concrete">Concrete</option>
                  <option value="steel">Steel</option>
                  <option value="aluminum">Aluminum</option>
                  <option value="timber">Timber</option>
                </select>
                <input
                  type="number"
                  placeholder="Yield Strength (MPa)"
                  value={newMaterial.fy || ''}
                  onChange={(e) => setNewMaterial({ ...newMaterial, fy: parseFloat(e.target.value) })}
                />
              </div>
              <div className="grid grid-cols-3 gap-3">
                <input
                  type="number"
                  placeholder="E (MPa)"
                  value={newMaterial.E || ''}
                  onChange={(e) => setNewMaterial({ ...newMaterial, E: parseFloat(e.target.value) })}
                />
                <input
                  type="number"
                  placeholder="Poisson's Ratio"
                  step="0.01"
                  value={newMaterial.nu || ''}
                  onChange={(e) => setNewMaterial({ ...newMaterial, nu: parseFloat(e.target.value) })}
                />
                <input
                  type="number"
                  placeholder="Density (kg/m³)"
                  value={newMaterial.density || ''}
                  onChange={(e) => setNewMaterial({ ...newMaterial, density: parseFloat(e.target.value) })}
                />
              </div>
              <button onClick={handleAddMaterial} className="btn-primary w-full">
                Add Material
              </button>
            </div>
          )}

          {/* Materials Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {filteredMaterials.map((material) => (
              <div
                key={material.id}
                onClick={() => handleSelectMaterial(material)}
                className="panel p-4 cursor-pointer transition-all hover:border-blue-500"
              >
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h3 className="font-semibold">{material.name}</h3>
                    <p className="text-xs" style={{ color: 'var(--text-tertiary)' }}>ID: {material.id}</p>
                  </div>
                  <span 
                    className="px-2 py-1 text-xs rounded"
                    style={{ 
                      background: material.type === 'concrete' ? 'var(--accent-blue)' : 
                                 material.type === 'steel' ? 'var(--accent-red)' : 'var(--accent-purple)',
                      color: 'white'
                    }}
                  >
                    {material.type}
                  </span>
                </div>
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div>
                    <span style={{ color: 'var(--text-tertiary)' }}>E:</span> {material.E.toLocaleString()} MPa
                  </div>
                  <div>
                    <span style={{ color: 'var(--text-tertiary)' }}>fy:</span> {material.fy} MPa
                  </div>
                  <div>
                    <span style={{ color: 'var(--text-tertiary)' }}>ν:</span> {material.nu}
                  </div>
                  <div>
                    <span style={{ color: 'var(--text-tertiary)' }}>ρ:</span> {material.density} kg/m³
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Current Materials */}
          {materials.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold mb-2" style={{ color: 'var(--text-secondary)' }}>Current Project Materials</h3>
              <div className="space-y-2">
                {materials.map((material) => (
                  <div key={material.id} className="flex items-center justify-between p-2 rounded" style={{ background: 'var(--bg-tertiary)' }}>
                    <span className="text-sm">{material.name}</span>
                    <span className="text-xs" style={{ color: 'var(--text-tertiary)' }}>E: {material.E} MPa</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
