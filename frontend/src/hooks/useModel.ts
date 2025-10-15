import { useContext } from 'react'
import { ModelContext } from '@/contexts/ModelContext'

export function useModel() {
  const context = useContext(ModelContext)
  if (!context) {
    throw new Error('useModel must be used within ModelProvider')
  }
  return context
}
