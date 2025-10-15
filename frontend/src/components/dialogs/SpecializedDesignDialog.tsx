import React, { useState } from 'react'
import { X, Building2 } from 'lucide-react'

interface SpecializedDesignDialogProps {
  isOpen: boolean
  onClose: () => void
  onDesign: (data: any) => void
}

export default function SpecializedDesignDialog({ isOpen, onClose, onDesign }: SpecializedDesignDialogProps) {
  const [designType, setDesignType] = useState<'shear-wall' | 'retaining-wall' | 'staircase' | 'composite'>('shear-wall')
  const [formData, setFormData] = useState({
    length: 6000,
    height: 3500,
    thickness: 300,
    concrete: 'M30',
    steel: 'Fe500'
  })

  if (!isOpen) return null

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onDesign({ ...formData, type: designType })
    onClose()
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-gray-800 rounded-lg shadow-xl w-full max-w-2xl">
        <div className="flex items-center justify-between p-4 border-b border-gray-700">
          <div className="flex items-center space-x-2">
            <Building2 className="w-5 h-5 text-cyan-400" />
            <h2 className="text-lg font-semibold">Specialized Design</h2>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Design Type</label>
            <select
              value={designType}
              onChange={(e) => setDesignType(e.target.value as any)}
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded"
            >
              <option value="shear-wall">Shear Wall Design</option>
              <option value="retaining-wall">Retaining Wall Design</option>
              <option value="staircase">Staircase Design</option>
              <option value="composite">Composite Beam Design</option>
            </select>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">
                {designType === 'staircase' ? 'Flight Length' : 'Length'} (mm)
              </label>
              <input
                type="number"
                value={formData.length}
                onChange={(e) => setFormData({ ...formData, length: Number(e.target.value) })}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">
                {designType === 'staircase' ? 'Rise' : 'Height'} (mm)
              </label>
              <input
                type="number"
                value={formData.height}
                onChange={(e) => setFormData({ ...formData, height: Number(e.target.value) })}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Thickness (mm)</label>
              <input
                type="number"
                value={formData.thickness}
                onChange={(e) => setFormData({ ...formData, thickness: Number(e.target.value) })}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Concrete Grade</label>
              <select
                value={formData.concrete}
                onChange={(e) => setFormData({ ...formData, concrete: e.target.value })}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded"
              >
                <option value="M20">M20</option>
                <option value="M25">M25</option>
                <option value="M30">M30</option>
                <option value="M35">M35</option>
                <option value="M40">M40</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Steel Grade</label>
              <select
                value={formData.steel}
                onChange={(e) => setFormData({ ...formData, steel: e.target.value })}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded"
              >
                <option value="Fe415">Fe 415</option>
                <option value="Fe500">Fe 500</option>
                <option value="Fe550">Fe 550</option>
              </select>
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
              className="px-4 py-2 bg-cyan-600 hover:bg-cyan-700 rounded"
            >
              Design
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
