import React, { useState } from 'react'
import { X, Sparkles, Wand2, AlertCircle, Zap } from 'lucide-react'

interface AIAssistantDialogProps {
  isOpen: boolean
  onClose: () => void
  onSubmit: (data: any) => void
}

export default function AIAssistantDialog({ isOpen, onClose, onSubmit }: AIAssistantDialogProps) {
  const [activeTab, setActiveTab] = useState<'auto-model' | 'design-assistant' | 'error-checker' | 'optimize'>('auto-model')
  const [description, setDescription] = useState('')
  const [loading, setLoading] = useState(false)

  if (!isOpen) return null

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    
    const data = {
      type: activeTab,
      description,
      timestamp: new Date().toISOString()
    }
    
    await onSubmit(data)
    setLoading(false)
    onClose()
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-gray-800 rounded-lg shadow-xl w-full max-w-3xl max-h-[90vh] flex flex-col">
        <div className="flex items-center justify-between p-4 border-b border-gray-700">
          <div className="flex items-center space-x-2">
            <Sparkles className="w-5 h-5 text-purple-400" />
            <h2 className="text-lg font-semibold">AI Assistant</h2>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="flex border-b border-gray-700">
          <button
            onClick={() => setActiveTab('auto-model')}
            className={`flex items-center space-x-2 px-4 py-3 text-sm ${
              activeTab === 'auto-model' ? 'border-b-2 border-purple-500 text-purple-400' : 'text-gray-400'
            }`}
          >
            <Wand2 className="w-4 h-4" />
            <span>Auto Model</span>
          </button>
          <button
            onClick={() => setActiveTab('design-assistant')}
            className={`flex items-center space-x-2 px-4 py-3 text-sm ${
              activeTab === 'design-assistant' ? 'border-b-2 border-purple-500 text-purple-400' : 'text-gray-400'
            }`}
          >
            <Sparkles className="w-4 h-4" />
            <span>Design Assistant</span>
          </button>
          <button
            onClick={() => setActiveTab('error-checker')}
            className={`flex items-center space-x-2 px-4 py-3 text-sm ${
              activeTab === 'error-checker' ? 'border-b-2 border-purple-500 text-purple-400' : 'text-gray-400'
            }`}
          >
            <AlertCircle className="w-4 h-4" />
            <span>Error Checker</span>
          </button>
          <button
            onClick={() => setActiveTab('optimize')}
            className={`flex items-center space-x-2 px-4 py-3 text-sm ${
              activeTab === 'optimize' ? 'border-b-2 border-purple-500 text-purple-400' : 'text-gray-400'
            }`}
          >
            <Zap className="w-4 h-4" />
            <span>Optimize</span>
          </button>
        </div>

        <form onSubmit={handleSubmit} className="flex-1 overflow-auto p-6 space-y-4">
          {activeTab === 'auto-model' && (
            <div className="space-y-4">
              <div className="bg-purple-900 bg-opacity-20 border border-purple-700 rounded p-4">
                <p className="text-sm text-purple-300">
                  Describe your structure in natural language, and AI will generate the model automatically.
                </p>
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Structure Description</label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded h-40"
                  placeholder="Example: Create a 5-story building with 4 bays in X direction and 3 bays in Y direction. Story height is 3.5m, bay width is 6m. Use concrete columns 400x400mm and beams 300x600mm..."
                />
              </div>
            </div>
          )}

          {activeTab === 'design-assistant' && (
            <div className="space-y-4">
              <div className="bg-purple-900 bg-opacity-20 border border-purple-700 rounded p-4">
                <p className="text-sm text-purple-300">
                  Get AI-powered design suggestions and recommendations for your structure.
                </p>
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">What do you need help with?</label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded h-40"
                  placeholder="Example: Suggest optimal column sizes for my building, recommend load combinations, check if my beam design is adequate..."
                />
              </div>
            </div>
          )}

          {activeTab === 'error-checker' && (
            <div className="space-y-4">
              <div className="bg-purple-900 bg-opacity-20 border border-purple-700 rounded p-4">
                <p className="text-sm text-purple-300">
                  AI will analyze your model and identify potential errors or issues.
                </p>
              </div>
              <div className="text-sm text-gray-300">
                <p className="mb-2">The AI will check for:</p>
                <ul className="list-disc list-inside space-y-1 text-gray-400">
                  <li>Structural instabilities</li>
                  <li>Missing supports or constraints</li>
                  <li>Unrealistic member sizes</li>
                  <li>Load application errors</li>
                  <li>Code compliance issues</li>
                </ul>
              </div>
            </div>
          )}

          {activeTab === 'optimize' && (
            <div className="space-y-4">
              <div className="bg-purple-900 bg-opacity-20 border border-purple-700 rounded p-4">
                <p className="text-sm text-purple-300">
                  Optimize your structure for cost, weight, or performance using AI algorithms.
                </p>
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Optimization Goal</label>
                <select className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded mb-4">
                  <option>Minimize Cost</option>
                  <option>Minimize Weight</option>
                  <option>Maximize Stiffness</option>
                  <option>Balance Cost and Performance</option>
                </select>
                <label className="block text-sm font-medium mb-2">Additional Constraints</label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded h-24"
                  placeholder="Example: Keep column sizes uniform, limit beam depth to 600mm, use standard section sizes..."
                />
              </div>
            </div>
          )}

          <div className="flex justify-end space-x-3 pt-4 border-t border-gray-700">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded disabled:opacity-50 flex items-center space-x-2"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>Processing...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4" />
                  <span>Run AI</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
