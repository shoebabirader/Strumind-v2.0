import React, { useState } from 'react'
import { X, Ruler } from 'lucide-react'

interface DesignDialogProps {
  isOpen: boolean
  onClose: () => void
}

export default function DesignDialog({ isOpen, onClose }: DesignDialogProps) {
  const [designType, setDesignType] = useState('concrete')
  const [code, setCode] = useState('IS456')

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="panel w-full max-w-2xl">
        <div className="panel-header">
          <span><Ruler className="w-4 h-4 inline mr-2" />Design Settings</span>
          <button onClick={onClose} className="toolbar-button">
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="p-6 space-y-6">
          {/* Design Type */}
          <div>
            <label className="block text-sm font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>
              Design Type
            </label>
            <div className="grid grid-cols-3 gap-3">
              {[
                { value: 'concrete', label: 'Concrete Design' },
                { value: 'steel', label: 'Steel Design' },
                { value: 'foundation', label: 'Foundation Design' },
              ].map((type) => (
                <label
                  key={type.value}
                  className={`panel p-3 cursor-pointer transition-all ${
                    designType === type.value ? 'border-blue-500' : ''
                  }`}
                >
                  <input
                    type="radio"
                    name="designType"
                    value={type.value}
                    checked={designType === type.value}
                    onChange={(e) => setDesignType(e.target.value)}
                    className="mr-2"
                  />
                  <span className="text-sm">{type.label}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Design Code */}
          <div>
            <label className="block text-sm font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>
              Design Code
            </label>
            <select
              value={code}
              onChange={(e) => setCode(e.target.value)}
              className="w-full"
            >
              <option value="IS456">IS 456:2000 (India)</option>
              <option value="ACI318">ACI 318 (USA)</option>
              <option value="EC2">Eurocode 2 (Europe)</option>
              <option value="BS8110">BS 8110 (UK)</option>
            </select>
          </div>

          {/* Design Parameters */}
          <div>
            <label className="block text-sm font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>
              Design Parameters
            </label>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs mb-1" style={{ color: 'var(--text-tertiary)' }}>
                  Concrete Grade
                </label>
                <select className="w-full">
                  <option>M20</option>
                  <option>M25</option>
                  <option>M30</option>
                  <option>M35</option>
                </select>
              </div>
              <div>
                <label className="block text-xs mb-1" style={{ color: 'var(--text-tertiary)' }}>
                  Steel Grade
                </label>
                <select className="w-full">
                  <option>Fe415</option>
                  <option>Fe500</option>
                  <option>Fe550</option>
                </select>
              </div>
            </div>
          </div>

          <div className="flex justify-end space-x-3 pt-4">
            <button onClick={onClose} className="btn-secondary">
              Cancel
            </button>
            <button className="btn-primary">
              <Ruler className="w-4 h-4 mr-2" />
              Run Design
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
