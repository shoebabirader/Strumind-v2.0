import React, { createContext, useContext, useState } from 'react'

interface Node {
  id: string
  x: number
  y: number
  z: number
  restraints: boolean[]
}

interface Element {
  id: string
  nodeI: string
  nodeJ: string
  type: string
  materialId?: string
  sectionType?: string
  width?: number
  height?: number
}

interface Material {
  id: string
  name: string
  E: number
  nu: number
  density: number
}

interface ModelContextType {
  currentProjectId: number | null
  setCurrentProjectId: (id: number | null) => void
  nodes: Node[]
  elements: Element[]
  materials: Material[]
  addNode: (node: Node) => void
  addElement: (element: Element) => void
  addMaterial: (material: Material) => void
  selectedItems: Set<string>
  selectItem: (id: string) => void
  clearSelection: () => void
}

const ModelContext = createContext<ModelContextType | undefined>(undefined)

export function ModelProvider({ children }: { children: React.ReactNode }) {
  const [currentProjectId, setCurrentProjectId] = useState<number | null>(1) // Default to project 1 for now
  const [nodes, setNodes] = useState<Node[]>([])
  const [elements, setElements] = useState<Element[]>([])
  const [materials, setMaterials] = useState<Material[]>([
    { id: 'concrete_m25', name: 'Concrete M25', E: 25000, nu: 0.2, density: 2500 },
    { id: 'steel_fe415', name: 'Steel Fe415', E: 200000, nu: 0.3, density: 7850 },
  ])
  const [selectedItems, setSelectedItems] = useState<Set<string>>(new Set())

  // Load nodes from backend on mount
  React.useEffect(() => {
    if (currentProjectId) {
      loadNodesFromBackend()
      loadElementsFromBackend()
    }
  }, [currentProjectId])

  const loadNodesFromBackend = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/nodes/list/${currentProjectId}`)
      if (response.ok) {
        const data = await response.json()
        setNodes(data)
      }
    } catch (error) {
      console.error('Failed to load nodes:', error)
    }
  }

  const loadElementsFromBackend = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/elements/list/${currentProjectId}`)
      if (response.ok) {
        const data = await response.json()
        setElements(data)
      }
    } catch (error) {
      console.error('Failed to load elements:', error)
    }
  }

  const addNode = (node: Node) => {
    setNodes([...nodes, node])
    loadNodesFromBackend() // Refresh from backend
  }
  const addElement = (element: Element) => {
    setElements([...elements, element])
    loadElementsFromBackend() // Refresh from backend
  }
  const addMaterial = (material: Material) => setMaterials([...materials, material])
  
  const selectItem = (id: string) => {
    const newSelection = new Set(selectedItems)
    if (newSelection.has(id)) {
      newSelection.delete(id)
    } else {
      newSelection.add(id)
    }
    setSelectedItems(newSelection)
  }
  
  const clearSelection = () => setSelectedItems(new Set())

  return (
    <ModelContext.Provider value={{
      currentProjectId, setCurrentProjectId,
      nodes, elements, materials,
      addNode, addElement, addMaterial,
      selectedItems, selectItem, clearSelection
    }}>
      {children}
    </ModelContext.Provider>
  )
}

export function useModel() {
  const context = useContext(ModelContext)
  if (!context) throw new Error('useModel must be used within ModelProvider')
  return context
}
