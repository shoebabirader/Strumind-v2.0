import React from 'react'

export default function AxisHelper() {
  return (
    <div className="absolute bottom-4 left-4 panel px-3 py-2 text-xs flex space-x-3">
      <div className="flex items-center space-x-1">
        <div className="w-3 h-0.5" style={{ background: 'var(--axis-x)' }}></div>
        <span style={{ color: 'var(--axis-x)' }}>X</span>
      </div>
      <div className="flex items-center space-x-1">
        <div className="w-3 h-0.5" style={{ background: 'var(--axis-y)' }}></div>
        <span style={{ color: 'var(--axis-y)' }}>Y</span>
      </div>
      <div className="flex items-center space-x-1">
        <div className="w-3 h-0.5" style={{ background: 'var(--axis-z)' }}></div>
        <span style={{ color: 'var(--axis-z)' }}>Z</span>
      </div>
    </div>
  )
}
