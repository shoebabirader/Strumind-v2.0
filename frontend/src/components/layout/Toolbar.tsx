import React from 'react'
import {
  Save, FolderOpen, Play, Copy, Trash2, Box, Move,
  Grid, ZoomIn, ZoomOut, RotateCcw, Layers, Zap, Table
} from 'lucide-react'

interface ToolbarProps {
  onNodeDialog?: () => void
  onElementDialog?: () => void
  onMaterialDialog?: () => void
  onLoadDialog?: () => void
  onAnalysisDialog?: () => void
  onTablesPanel?: () => void
}

export default function Toolbar({
  onNodeDialog,
  onElementDialog,
  onMaterialDialog,
  onLoadDialog,
  onAnalysisDialog,
  onTablesPanel
}: ToolbarProps) {
  const tools = [
    { icon: Save, tip: 'Save' },
    { icon: FolderOpen, tip: 'Open' },
    null,
    { icon: Copy, tip: 'Copy' },
    { icon: Trash2, tip: 'Delete' },
    null,
    { icon: Box, tip: 'Add Node', onClick: onNodeDialog },
    { icon: Move, tip: 'Add Element', onClick: onElementDialog },
    { icon: Layers, tip: 'Materials', onClick: onMaterialDialog },
    { icon: Zap, tip: 'Loads', onClick: onLoadDialog },
    { icon: Grid, tip: 'Grid' },
    null,
    { icon: Table, tip: 'Tables', onClick: onTablesPanel },
    null,
    { icon: ZoomIn, tip: 'Zoom In' },
    { icon: ZoomOut, tip: 'Zoom Out' },
    { icon: RotateCcw, tip: 'Reset View' },
    null,
    { icon: Play, tip: 'Run Analysis', highlight: true, onClick: onAnalysisDialog },
  ]

  return (
    <div 
      style={{ background: 'var(--bg-secondary)', borderBottom: '1px solid var(--border-primary)' }} 
      className="px-2 py-2 flex items-center space-x-1"
    >
      {tools.map((tool, idx) =>
        tool === null ? (
          <div key={idx} className="w-px h-6" style={{ background: 'var(--border-secondary)' }} />
        ) : (
          <button
            key={idx}
            onClick={tool.onClick}
            className={`toolbar-button ${tool.highlight ? 'active' : ''}`}
            title={tool.tip}
          >
            <tool.icon className="w-4 h-4" />
          </button>
        )
      )}
    </div>
  )
}
