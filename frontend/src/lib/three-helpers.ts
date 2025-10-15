// Three.js helper utilities
// This file will contain Three.js specific helper functions

export interface Vector3 {
  x: number
  y: number
  z: number
}

export interface Node3D {
  id: string
  position: Vector3
  restraints: boolean[]
}

export interface Element3D {
  id: string
  nodeI: string
  nodeJ: string
  type: string
}

// Helper to create a basic scene setup
export function createSceneSetup() {
  return {
    camera: {
      position: { x: 10, y: 10, z: 10 },
      lookAt: { x: 0, y: 0, z: 0 },
    },
    lights: [
      { type: 'ambient', intensity: 0.5 },
      { type: 'directional', position: { x: 10, y: 10, z: 10 }, intensity: 0.8 },
    ],
  }
}

// Helper to convert nodes to 3D positions
export function nodesToPositions(nodes: any[]): Vector3[] {
  return nodes.map(node => ({
    x: node.x,
    y: node.y,
    z: node.z,
  }))
}

// Helper to calculate bounding box
export function calculateBoundingBox(nodes: any[]) {
  if (nodes.length === 0) {
    return { min: { x: 0, y: 0, z: 0 }, max: { x: 0, y: 0, z: 0 } }
  }

  const positions = nodesToPositions(nodes)
  const min = { x: Infinity, y: Infinity, z: Infinity }
  const max = { x: -Infinity, y: -Infinity, z: -Infinity }

  positions.forEach(pos => {
    min.x = Math.min(min.x, pos.x)
    min.y = Math.min(min.y, pos.y)
    min.z = Math.min(min.z, pos.z)
    max.x = Math.max(max.x, pos.x)
    max.y = Math.max(max.y, pos.y)
    max.z = Math.max(max.z, pos.z)
  })

  return { min, max }
}

// Helper to calculate center point
export function calculateCenter(nodes: any[]): Vector3 {
  const bbox = calculateBoundingBox(nodes)
  return {
    x: (bbox.min.x + bbox.max.x) / 2,
    y: (bbox.min.y + bbox.max.y) / 2,
    z: (bbox.min.z + bbox.max.z) / 2,
  }
}
