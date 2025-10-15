import React, { useState } from 'react'
import { X, Wrench } from 'lucide-react'

interface DetailingDialogProps {
  isOpen: boolean
  onClose: () => void
  onSubmit: (data: any) => void
}

export default function DetailingDialog({ isOpen, onClose, onSubmit }: DetailingDialogProps) {
  const [detailingType, setDetailingType] = useState<'beam' | 'column' | 'slab' | 'ductile'>('beam')
  const [formData, setFormData] = useState({
    elementId: '',
    code: 'ACI318',
    coverThickness: 40,
    barDiameter: 16,
    stirrupDiameter: 10,
    spacing: 150
  })

  if (!isOpen) return null

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit({ ...formData, type: detailingType })
    onClose()
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-gray-800 rounded-lg shadow-xl w-full max-w-2xl">
        <div className="flex items-center justify-between p-4 border-b border-gray-700">
          <div className="flex items-center space-x-2">
            <Wrench className="w-5 h-5 text-blue-400" />
            <h2 className="text-lg font-semibold">Reinforcement Detailing</h2>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Detailing Type</label>
              <select
                value={detailingType}
                onChange={(e) => setDetailingType(e.target.value as any)}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded"
              >
                <option value="beam">Beam Detailing</option>
                <option value="column">Column Detailing</option>
                <option value="slab">Slab Detailing</option>
                <option value="ductile">Ductile Detailing</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Element ID</label>
              <input
                type="text"
                value={formData.elementId}
                onChange={(e) => setFormData({ ...formData, elementId: e.target.value })}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded"
                placeholder="Element ID"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Design Code</label>
              <select
                value={formData.code}
                onChange={(e) => setFormData({ ...formData, code: e.target.value })}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded"
              >
                <option value="ACI318">ACI 318</option>
                <option value="IS456">IS 456</option>
                <option value="EC2">Eurocode 2</option>
                <option value="BS8110">BS 8110</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Cover Thickness (mm)</label>
              <input
                type="number"
                value={formData.coverThickness}
                onChange={(e) => setFormData({ ...formData, coverThickness: Number(e.target.value) })}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Main Bar Diameter (mm)</label>
              <input
                type="number"
                value={formData.barDiameter}
                onChange={(e) => setFormData({ ...formData, barDiameter: Number(e.target.value) })}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Stirrup Diameter (mm)</label>
              <input
                type="number"
                value={formData.stirrupDiameter}
                onChange={(e) => setFormData({ ...formData, stirrupDiameter: Number(e.target.value) })}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Spacing (mm)</label>
              <input
                type="number"
                value={formData.spacing}
                onChange={(e) => setFormData({ ...formData, spacing: Number(e.target.value) })}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded"
              />
            </div>
          </div>

          <div className="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded"
            >
              Generate Detailing
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
