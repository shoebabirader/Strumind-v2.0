import React, { createContext, useContext, useState } from 'react'

interface UIContextType {
  leftPanelVisible: boolean
  setLeftPanelVisible: (visible: boolean) => void
  rightPanelVisible: boolean
  setRightPanelVisible: (visible: boolean) => void
  bottomPanelVisible: boolean
  setBottomPanelVisible: (visible: boolean) => void
  activeRightTab: string
  setActiveRightTab: (tab: string) => void
}

const UIContext = createContext<UIContextType | undefined>(undefined)

export function UIProvider({ children }: { children: React.ReactNode }) {
  const [leftPanelVisible, setLeftPanelVisible] = useState(true)
  const [rightPanelVisible, setRightPanelVisible] = useState(true)
  const [bottomPanelVisible, setBottomPanelVisible] = useState(false)
  const [activeRightTab, setActiveRightTab] = useState('properties')

  return (
    <UIContext.Provider
      value={{
        leftPanelVisible,
        setLeftPanelVisible,
        rightPanelVisible,
        setRightPanelVisible,
        bottomPanelVisible,
        setBottomPanelVisible,
        activeRightTab,
        setActiveRightTab,
      }}
    >
      {children}
    </UIContext.Provider>
  )
}

export function useUI() {
  const context = useContext(UIContext)
  if (!context) {
    throw new Error('useUI must be used within UIProvider')
  }
  return context
}
