import React, { useState, createContext, useContext } from 'react'

interface SelectionContextType {
  selectedItem: { type: string; data: any } | null
  setSelectedItem: (item: { type: string; data: any } | null) => void
}

const SelectionContext = createContext<SelectionContextType | undefined>(undefined)

export function SelectionProvider({ children }: { children: React.ReactNode }) {
  const [selectedItem, setSelectedItem] = useState<{ type: string; data: any } | null>(null)

  return (
    <SelectionContext.Provider value={{ selectedItem, setSelectedItem }}>
      {children}
    </SelectionContext.Provider>
  )
}

export function useSelectionContext() {
  const context = useContext(SelectionContext)
  if (!context) {
    throw new Error('useSelectionContext must be used within SelectionProvider')
  }
  return context
}
