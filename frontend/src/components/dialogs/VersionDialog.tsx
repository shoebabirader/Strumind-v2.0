import React, { useState } from 'react'
import { X, Clock, RotateCcw, GitBranch } from 'lucide-react'

interface VersionDialogProps {
  isOpen: boolean
  onClose: () => void
  onRestore: (versionId: string) => void
}

export default function VersionDialog({ isOpen, onClose, onRestore }: VersionDialogProps) {
  const [versions] = useState([
    {
      id: 'v1.3',
      timestamp: '2024-01-15 14:30',
      user: 'John Doe',
      description: 'Added seismic loads',
      changes: 15
    },
    {
      id: 'v1.2',
      timestamp: '2024-01-15 10:15',
      user: 'Jane Smith',
      description: 'Updated column sizes',
      changes: 8
    },
    {
      id: 'v1.1',
      timestamp: '2024-01-14 16:45',
      user: 'John Doe',
      description: 'Initial model setup',
      changes: 42
    }
  ])

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-gray-800 rounded-lg shadow-xl w-full max-w-3xl max-h-[80vh] flex flex-col">
        <div className="flex items-center justify-between p-4 border-b border-gray-700">
          <div className="flex items-center space-x-2">
            <Clock className="w-5 h-5 text-purple-400" />
            <h2 className="text-lg font-semibold">Version History</h2>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="flex-1 overflow-auto p-6">
          <div className="space-y-3">
            {versions.map((version, idx) => (
              <div
                key={version.id}
                className="p-4 bg-gray-700 rounded-lg hover:bg-gray-650 transition-colors"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-2">
                      <GitBranch className="w-4 h-4 text-purple-400" />
                      <span className="font-semibold">{version.id}</span>
                      {idx === 0 && (
                        <span className="text-xs px-2 py-1 bg-green-900 text-green-300 rounded">
                          Current
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-gray-300 mb-2">{version.description}</p>
                    <div className="flex items-center space-x-4 text-xs text-gray-400">
                      <span>{version.timestamp}</span>
                      <span>by {version.user}</span>
                      <span>{version.changes} changes</span>
                    </div>
                  </div>
                  {idx !== 0 && (
                    <button
                      onClick={() => {
                        onRestore(version.id)
                        onClose()
                      }}
                      className="ml-4 px-3 py-1 bg-purple-600 hover:bg-purple-700 rounded text-sm flex items-center space-x-1"
                    >
                      <RotateCcw className="w-3 h-3" />
                      <span>Restore</span>
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="p-4 border-t border-gray-700 bg-gray-750">
          <div className="bg-yellow-900 bg-opacity-20 border border-yellow-700 rounded p-3">
            <p className="text-sm text-yellow-300">
              Restoring a version will create a new version with the restored state.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
