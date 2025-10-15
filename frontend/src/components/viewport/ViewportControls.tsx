import React from 'react'
import { ZoomIn, ZoomOut, Maximize2, RotateCcw, Move, MousePointer } from 'lucide-react'

interface ViewportControlsProps {
  onZoomIn: () => void
  onZoomOut: () => void
  onFit: () => void
  onReset: () => void
}

export default function ViewportControls({ onZoomIn, onZoomOut, onFit, onReset }: ViewportControlsProps) {
  return (
    <div className="absolute bottom-4 right-4 flex flex-col space-y-2">
      <button
        onClick={onZoomIn}
        className="toolbar-button w-10 h-10 flex items-center justify-center"
        title="Zoom In"
        style={{ background: 'var(--bg-secondary)' }}
      >
        <ZoomIn className="w-5 h-5" />
      </button>
      <button
        onClick={onZoomOut}
        className="toolbar-button w-10 h-10 flex items-center justify-center"
        title="Zoom Out"
        style={{ background: 'var(--bg-secondary)' }}
      >
        <ZoomOut className="w-5 h-5" />
      </button>
      <button
        onClick={onFit}
        className="toolbar-button w-10 h-10 flex items-center justify-center"
        title="Fit to View"
        style={{ background: 'var(--bg-secondary)' }}
      >
        <Maximize2 className="w-5 h-5" />
      </button>
      <button
        onClick={onReset}
        className="toolbar-button w-10 h-10 flex items-center justify-center"
        title="Reset View"
        style={{ background: 'var(--bg-secondary)' }}
      >
        <RotateCcw className="w-5 h-5" />
      </button>
      
      <div className="h-px" style={{ background: 'var(--border-primary)' }} />
      
      <button
        className="toolbar-button w-10 h-10 flex items-center justify-center"
        title="Select"
        style={{ background: 'var(--bg-secondary)' }}
      >
        <MousePointer className="w-5 h-5" />
      </button>
      <button
        className="toolbar-button w-10 h-10 flex items-center justify-center"
        title="Pan"
        style={{ background: 'var(--bg-secondary)' }}
      >
        <Move className="w-5 h-5" />
      </button>
    </div>
  )
}
