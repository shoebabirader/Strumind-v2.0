import React from 'react'
import { useModel } from '@/contexts/ModelContext'

export default function StatusBar() {
  const { nodes, elements, materials } = useModel()

  return (
    <div 
      style={{ background: 'var(--bg-secondary)', borderTop: '1px solid var(--border-primary)' }} 
      className="px-3 py-1 flex items-center justify-between text-xs"
    >
      <div className="flex items-center space-x-4">
        <span className="status-ready">● Ready</span>
        <span style={{ color: 'var(--text-tertiary)' }}>Units: kN, m, C</span>
      </div>
      <div className="flex items-center space-x-4" style={{ color: 'var(--text-tertiary)' }}>
        <span>Nodes: {nodes.length}</span>
        <span>Elements: {elements.length}</span>
        <span>Materials: {materials.length}</span>
      </div>
    </div>
  )
}
