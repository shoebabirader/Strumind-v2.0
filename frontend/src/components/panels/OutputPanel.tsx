import React from 'react'
import { Terminal } from 'lucide-react'

export default function OutputPanel() {
  return (
    <div 
      className="h-48 flex flex-col" 
      style={{ background: 'var(--bg-secondary)', borderTop: '1px solid var(--border-primary)' }}
    >
      <div className="panel-header">
        <span><Terminal className="w-4 h-4 inline mr-2" />Output</span>
      </div>
      <div className="flex-1 overflow-auto p-3 font-mono text-xs" style={{ color: 'var(--text-secondary)' }}>
        <div>Ready to analyze...</div>
      </div>
    </div>
  )
}
