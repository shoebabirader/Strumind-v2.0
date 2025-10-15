import React from 'react'
import { useAuth } from '@/contexts/AuthContext'

export default function MenuBar() {
  const { user, logout } = useAuth()

  const menuItems = ['File', 'Edit', 'View', 'Define', 'Draw', 'Select', 'Assign', 'Analyze', 'Display', 'Design', 'Options', 'Tools', 'Help']

  return (
    <div 
      style={{ background: 'var(--bg-secondary)', borderBottom: '1px solid var(--border-primary)' }} 
      className="px-2 py-1 flex items-center justify-between text-xs"
    >
      <div className="flex items-center space-x-4">
        <div className="font-bold text-sm" style={{ color: 'var(--accent-blue)' }}>
          StruMind Pro
        </div>
        {menuItems.map(item => (
          <button key={item} className="px-2 py-1 hover:bg-gray-700 rounded">
            {item}
          </button>
        ))}
      </div>
      <div className="flex items-center space-x-3">
        <span style={{ color: 'var(--text-tertiary)' }}>{user?.username}</span>
        <button onClick={logout} className="px-2 py-1 hover:bg-gray-700 rounded">
          Logout
        </button>
      </div>
    </div>
  )
}
