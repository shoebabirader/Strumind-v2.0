import { useState, useCallback } from 'react'

export function useSelection() {
  const [selectedItems, setSelectedItems] = useState<Set<string>>(new Set())

  const selectItem = useCallback((id: string) => {
    setSelectedItems(prev => {
      const newSet = new Set(prev)
      if (newSet.has(id)) {
        newSet.delete(id)
      } else {
        newSet.add(id)
      }
      return newSet
    })
  }, [])

  const selectMultiple = useCallback((ids: string[]) => {
    setSelectedItems(new Set(ids))
  }, [])

  const clearSelection = useCallback(() => {
    setSelectedItems(new Set())
  }, [])

  const isSelected = useCallback((id: string) => {
    return selectedItems.has(id)
  }, [selectedItems])

  return {
    selectedItems,
    selectItem,
    selectMultiple,
    clearSelection,
    isSelected,
  }
}
