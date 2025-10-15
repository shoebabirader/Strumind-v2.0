import React, { useState } from 'react'
import Viewport3D from '@/components/viewport/Viewport3D'

export default function ViewportPanel() {
  const [activeView, setActiveView] = useState('3d')

  return (
    <div className="flex-1 flex flex-col">
      {/* View Tabs */}
      <div 
        style={{ background: 'var(--bg-secondary)', borderBottom: '1px solid var(--border-primary)' }} 
        className="px-2 py-1 flex items-center space-x-1 text-xs"
      >
        <button className="px-3 py-1 rounded-t bg-gray-900 text-white border-t-2 border-blue-500">
          3D View
        </button>
        <button 
          className="px-3 py-1 rounded-t hover:bg-gray-700" 
          style={{ color: 'var(--text-tertiary)' }}
        >
          Plan View
        </button>
      </div>

      {/* Secondary Toolbar */}
      <div 
        style={{ background: 'var(--bg-tertiary)', borderBottom: '1px solid var(--border-primary)' }} 
        className="px-3 py-1 flex items-center space-x-4 text-xs"
      >
        <div className="flex items-center space-x-2">
          <span style={{ color: 'var(--text-tertiary)' }}>View:</span>
          {['3D', 'XY', 'XZ', 'YZ'].map(v => (
            <button
              key={v}
              onClick={() => setActiveView(v.toLowerCase())}
              className={`px-3 py-1 rounded ${
                activeView === v.toLowerCase() ? 'bg-blue-600 text-white' : 'hover:bg-gray-700'
              }`}
            >
              {v}
            </button>
          ))}
        </div>
        <div className="w-px h-4" style={{ background: 'var(--border-secondary)' }} />
        <div className="flex items-center space-x-2">
          <span style={{ color: 'var(--text-tertiary)' }}>Units:</span>
          <select className="bg-gray-700 border border-gray-600 rounded px-2 py-1">
            <option>kN, m, C</option>
            <option>kip, ft, F</option>
          </select>
        </div>
      </div>

      {/* Viewport */}
      <div className="flex-1 overflow-hidden">
        <Viewport3D activeView={activeView} />
      </div>
    </div>
  )
}
