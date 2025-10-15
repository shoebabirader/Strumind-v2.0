import React, { useState } from 'react'
import { X, Users, Share2, UserPlus } from 'lucide-react'

interface CollaborationDialogProps {
  isOpen: boolean
  onClose: () => void
  onShare: (data: any) => void
}

export default function CollaborationDialog({ isOpen, onClose, onShare }: CollaborationDialogProps) {
  const [email, setEmail] = useState('')
  const [permission, setPermission] = useState<'view' | 'edit' | 'admin'>('view')
  const [activeUsers] = useState([
    { id: 1, name: 'John Doe', email: 'john@example.com', status: 'online', role: 'admin' },
    { id: 2, name: 'Jane Smith', email: 'jane@example.com', status: 'online', role: 'edit' }
  ])

  if (!isOpen) return null

  const handleShare = () => {
    onShare({ email, permission })
    setEmail('')
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-gray-800 rounded-lg shadow-xl w-full max-w-2xl">
        <div className="flex items-center justify-between p-4 border-b border-gray-700">
          <div className="flex items-center space-x-2">
            <Users className="w-5 h-5 text-blue-400" />
            <h2 className="text-lg font-semibold">Collaboration</h2>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6 space-y-6">
          <div>
            <h3 className="text-sm font-semibold mb-3 flex items-center space-x-2">
              <Share2 className="w-4 h-4" />
              <span>Share Project</span>
            </h3>
            <div className="flex space-x-2">
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter email address"
                className="flex-1 px-3 py-2 bg-gray-700 border border-gray-600 rounded"
              />
              <select
                value={permission}
                onChange={(e) => setPermission(e.target.value as any)}
                className="px-3 py-2 bg-gray-700 border border-gray-600 rounded"
              >
                <option value="view">View Only</option>
                <option value="edit">Can Edit</option>
                <option value="admin">Admin</option>
              </select>
              <button
                onClick={handleShare}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded flex items-center space-x-2"
              >
                <UserPlus className="w-4 h-4" />
                <span>Invite</span>
              </button>
            </div>
          </div>

          <div>
            <h3 className="text-sm font-semibold mb-3 flex items-center space-x-2">
              <Users className="w-4 h-4" />
              <span>Active Users ({activeUsers.length})</span>
            </h3>
            <div className="space-y-2">
              {activeUsers.map((user) => (
                <div
                  key={user.id}
                  className="flex items-center justify-between p-3 bg-gray-700 rounded"
                >
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                      {user.name.charAt(0)}
                    </div>
                    <div>
                      <div className="text-sm font-medium">{user.name}</div>
                      <div className="text-xs text-gray-400">{user.email}</div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-xs px-2 py-1 bg-green-900 text-green-300 rounded">
                      {user.status}
                    </span>
                    <span className="text-xs px-2 py-1 bg-gray-600 rounded">
                      {user.role}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-blue-900 bg-opacity-20 border border-blue-700 rounded p-4">
            <p className="text-sm text-blue-300">
              Real-time collaboration is enabled. Changes made by other users will appear instantly.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
