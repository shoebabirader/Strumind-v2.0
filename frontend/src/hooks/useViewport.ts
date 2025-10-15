import { useContext } from 'react'
import { ViewportContext } from '@/contexts/ViewportContext'

export function useViewport() {
  const context = useContext(ViewportContext)
  if (!context) {
    throw new Error('useViewport must be used within ViewportProvider')
  }
  return context
}
