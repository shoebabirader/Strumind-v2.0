// Geometry calculation utilities

export interface Point3D {
  x: number
  y: number
  z: number
}

// Calculate distance between two points
export function distance(p1: Point3D, p2: Point3D): number {
  const dx = p2.x - p1.x
  const dy = p2.y - p1.y
  const dz = p2.z - p1.z
  return Math.sqrt(dx * dx + dy * dy + dz * dz)
}

// Calculate element length
export function elementLength(nodeI: Point3D, nodeJ: Point3D): number {
  return distance(nodeI, nodeJ)
}

// Calculate direction cosines
export function directionCosines(nodeI: Point3D, nodeJ: Point3D) {
  const length = distance(nodeI, nodeJ)
  if (length === 0) return { cx: 0, cy: 0, cz: 0 }

  return {
    cx: (nodeJ.x - nodeI.x) / length,
    cy: (nodeJ.y - nodeI.y) / length,
    cz: (nodeJ.z - nodeI.z) / length,
  }
}

// Calculate midpoint
export function midpoint(p1: Point3D, p2: Point3D): Point3D {
  return {
    x: (p1.x + p2.x) / 2,
    y: (p1.y + p2.y) / 2,
    z: (p1.z + p2.z) / 2,
  }
}

// Calculate cross product
export function crossProduct(v1: Point3D, v2: Point3D): Point3D {
  return {
    x: v1.y * v2.z - v1.z * v2.y,
    y: v1.z * v2.x - v1.x * v2.z,
    z: v1.x * v2.y - v1.y * v2.x,
  }
}

// Calculate dot product
export function dotProduct(v1: Point3D, v2: Point3D): number {
  return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z
}

// Normalize vector
export function normalize(v: Point3D): Point3D {
  const length = Math.sqrt(v.x * v.x + v.y * v.y + v.z * v.z)
  if (length === 0) return { x: 0, y: 0, z: 0 }

  return {
    x: v.x / length,
    y: v.y / length,
    z: v.z / length,
  }
}

// Calculate angle between two vectors (in radians)
export function angleBetween(v1: Point3D, v2: Point3D): number {
  const dot = dotProduct(normalize(v1), normalize(v2))
  return Math.acos(Math.max(-1, Math.min(1, dot)))
}

// Convert degrees to radians
export function toRadians(degrees: number): number {
  return degrees * (Math.PI / 180)
}

// Convert radians to degrees
export function toDegrees(radians: number): number {
  return radians * (180 / Math.PI)
}
