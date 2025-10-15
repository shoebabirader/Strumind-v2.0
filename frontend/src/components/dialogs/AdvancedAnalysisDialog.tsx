import React, { useState } from 'react'
import { X, Activity } from 'lucide-react'

interface AdvancedAnalysisDialogProps {
  isOpen: boolean
  onClose: () => void
  onRun: (data: any) => void
}

export default function AdvancedAnalysisDialog({ isOpen, onClose, onRun }: AdvancedAnalysisDialogProps) {
  const [analysisType, setAnalysisType] = useState<'time-history' | 'response-spectrum' | 'pushover' | 'pdelta'>('time-history')
  const [formData, setFormData] = useState({
    damping: 0.05,
    timeStep: 0.01,
    duration: 10,
    scaleFactor: 1.0,
    direction: 'X'
  })

  if (!isOpen) return null

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onRun({ ...formData, type: analysisType })
    onClose()
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-gray-800 rounded-lg shadow-xl w-full max-w-2xl">
        <div className="flex items-center justify-between p-4 border-b border-gray-700">
          <div className="flex items-center space-x-2">
            <Activity className="w-5 h-5 text-orange-400" />
            <h2 className="text-lg font-semibold">Advanced Analysis</h2>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Analysis Type</label>
            <select
              value={analysisType}
              onChange={(e) => setAnalysisType(e.target.value as any)}
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded"
            >
              <option value="time-history">Time History Analysis</option>
              <option value="response-spectrum">Response Spectrum Analysis</option>
              <option value="pushover">Pushover Analysis</option>
              <option value="pdelta">P-Delta Analysis</option>
            </select>
          </div>

          {analysisType === 'time-history' && (
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Time Step (s)</label>
                <input
                  type="number"
                  step="0.001"
                  value={formData.timeStep}
                  onChange={(e) => setFormData({ ...formData, timeStep: Number(e.target.value) })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Duration (s)</label>
                <input
                  type="number"
                  value={formData.duration}
                  onChange={(e) => setFormData({ ...formData, duration: Number(e.target.value) })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Damping Ratio</label>
                <input
                  type="number"
                  step="0.01"
                  value={formData.damping}
                  onChange={(e) => setFormData({ ...formData, damping: Number(e.target.value) })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Scale Factor</label>
                <input
                  type="number"
                  step="0.1"
                  value={formData.scaleFactor}
                  onChange={(e) => setFormData({ ...formData, scaleFactor: Number(e.target.value) })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded"
                />
              </div>
            </div>
          )}

          {analysisType === 'response-spectrum' && (
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Damping Ratio</label>
                <input
                  type="number"
                  step="0.01"
                  value={formData.damping}
                  onChange={(e) => setFormData({ ...formData, damping: Number(e.target.value) })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Direction</label>
                <select
                  value={formData.direction}
                  onChange={(e) => setFormData({ ...formData, direction: e.target.value })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded"
                >
                  <option value="X">X Direction</option>
                  <option value="Y">Y Direction</option>
                  <option value="Z">Z Direction</option>
                </select>
              </div>
            </div>
          )}

          {analysisType === 'pushover' && (
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Push Direction</label>
                <select
                  value={formData.direction}
                  onChange={(e) => setFormData({ ...formData, direction: e.target.value })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded"
                >
                  <option value="X">+X Direction</option>
                  <option value="-X">-X Direction</option>
                  <option value="Y">+Y Direction</option>
                  <option value="-Y">-Y Direction</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Target Displacement</label>
                <input
                  type="number"
                  step="0.001"
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded"
                  placeholder="Auto"
                />
              </div>
            </div>
          )}

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
              className="px-4 py-2 bg-orange-600 hover:bg-orange-700 rounded"
            >
              Run Analysis
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
