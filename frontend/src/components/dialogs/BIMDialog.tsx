import React, { useState } from 'react'
import { X, Upload, Download, Eye } from 'lucide-react'

interface BIMDialogProps {
  isOpen: boolean
  onClose: () => void
  onAction: (action: string, data: any) => void
}

export default function BIMDialog({ isOpen, onClose, onAction }: BIMDialogProps) {
  const [activeTab, setActiveTab] = useState<'import' | 'export' | 'visualize'>('import')
  const [file, setFile] = useState<File | null>(null)

  if (!isOpen) return null

  const handleImport = () => {
    if (file) {
      onAction('import', { file })
      onClose()
    }
  }

  const handleExport = () => {
    onAction('export', { format: 'ifc' })
    onClose()
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-gray-800 rounded-lg shadow-xl w-full max-w-2xl">
        <div className="flex items-center justify-between p-4 border-b border-gray-700">
          <h2 className="text-lg font-semibold">BIM Integration</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="flex border-b border-gray-700">
          <button
            onClick={() => setActiveTab('import')}
            className={`flex items-center space-x-2 px-4 py-3 text-sm ${
              activeTab === 'import' ? 'border-b-2 border-blue-500 text-blue-400' : 'text-gray-400'
            }`}
          >
            <Upload className="w-4 h-4" />
            <span>Import</span>
          </button>
          <button
            onClick={() => setActiveTab('export')}
            className={`flex items-center space-x-2 px-4 py-3 text-sm ${
              activeTab === 'export' ? 'border-b-2 border-blue-500 text-blue-400' : 'text-gray-400'
            }`}
          >
            <Download className="w-4 h-4" />
            <span>Export</span>
          </button>
          <button
            onClick={() => setActiveTab('visualize')}
            className={`flex items-center space-x-2 px-4 py-3 text-sm ${
              activeTab === 'visualize' ? 'border-b-2 border-blue-500 text-blue-400' : 'text-gray-400'
            }`}
          >
            <Eye className="w-4 h-4" />
            <span>Visualize</span>
          </button>
        </div>

        <div className="p-6">
          {activeTab === 'import' && (
            <div className="space-y-4">
              <div className="border-2 border-dashed border-gray-600 rounded-lg p-8 text-center">
                <Upload className="w-12 h-12 mx-auto mb-4 text-gray-400" />
                <p className="text-sm text-gray-400 mb-2">Drop IFC file here or click to browse</p>
                <input
                  type="file"
                  accept=".ifc"
                  onChange={(e) => setFile(e.target.files?.[0] || null)}
                  className="hidden"
                  id="file-upload"
                />
                <label
                  htmlFor="file-upload"
                  className="inline-block px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded cursor-pointer"
                >
                  Select File
                </label>
                {file && <p className="mt-2 text-sm text-green-400">Selected: {file.name}</p>}
              </div>
              <div className="flex justify-end space-x-3">
                <button onClick={onClose} className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded">
                  Cancel
                </button>
                <button
                  onClick={handleImport}
                  disabled={!file}
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded disabled:opacity-50"
                >
                  Import
                </button>
              </div>
            </div>
          )}

          {activeTab === 'export' && (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Export Format</label>
                <select className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded">
                  <option value="ifc">IFC (Industry Foundation Classes)</option>
                  <option value="ifc2x3">IFC 2x3</option>
                  <option value="ifc4">IFC 4</option>
                </select>
              </div>
              <div className="flex justify-end space-x-3">
                <button onClick={onClose} className="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded">
                  Cancel
                </button>
                <button
                  onClick={handleExport}
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded"
                >
                  Export
                </button>
              </div>
            </div>
          )}

          {activeTab === 'visualize' && (
            <div className="space-y-4">
              <p className="text-sm text-gray-400">3D BIM visualization settings</p>
              <div className="space-y-2">
                <label className="flex items-center space-x-2">
                  <input type="checkbox" defaultChecked className="rounded" />
                  <span className="text-sm">Show structural elements</span>
                </label>
                <label className="flex items-center space-x-2">
                  <input type="checkbox" defaultChecked className="rounded" />
                  <span className="text-sm">Show architectural elements</span>
                </label>
                <label className="flex items-center space-x-2">
                  <input type="checkbox" className="rounded" />
                  <span className="text-sm">Show MEP elements</span>
                </label>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
