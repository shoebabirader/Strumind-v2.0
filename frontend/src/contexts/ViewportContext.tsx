import React, { createContext, useContext, useState } from 'react'

interface ViewportContextType {
  activeView: string
  setActiveView: (view: string) => void
  zoom: number
  setZoom: (zoom: number) => void
  rotation: { x: number; y: number; z: number }
  setRotation: (rotation: { x: number; y: number; z: number }) => void
  showGrid: boolean
  setShowGrid: (show: boolean) => void
  showAxes: boolean
  setShowAxes: (show: boolean) => void
}

const ViewportContext = createContext<ViewportContextType | undefined>(undefined)

export function ViewportProvider({ children }: { children: React.ReactNode }) {
  const [activeView, setActiveView] = useState('3d')
  const [zoom, setZoom] = useState(1)
  const [rotation, setRotation] = useState({ x: 0, y: 0, z: 0 })
  const [showGrid, setShowGrid] = useState(true)
  const [showAxes, setShowAxes] = useState(true)

  return (
    <ViewportContext.Provider
      value={{
        activeView,
        setActiveView,
        zoom,
        setZoom,
        rotation,
        setRotation,
        showGrid,
        setShowGrid,
        showAxes,
        setShowAxes,
      }}
    >
      {children}
    </ViewportContext.Provider>
  )
}

export function useViewport() {
  const context = useContext(ViewportContext)
  if (!context) {
    throw new Error('useViewport must be used within ViewportProvider')
  }
  return context
}
