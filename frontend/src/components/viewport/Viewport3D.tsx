import React, { useRef, useEffect } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, Grid, PerspectiveCamera } from '@react-three/drei'
import { useModel } from '@/contexts/ModelContext'
import ViewportControls from './ViewportControls'
import * as THREE from 'three'

interface Viewport3DProps {
  activeView?: string
}

// Node component to render individual nodes
function Node({ position, id, isSelected }: { position: [number, number, number]; id: string; isSelected: boolean }) {
  return (
    <mesh position={position}>
      <sphereGeometry args={[0.2, 16, 16]} />
      <meshStandardMaterial color={isSelected ? '#3b82f6' : '#10b981'} />
      <group>
        {/* Node label */}
        <mesh position={[0, 0.5, 0]}>
          <meshBasicMaterial color="white" />
        </mesh>
      </group>
    </mesh>
  )
}

// Element component to render beams/columns
function Element({ start, end, id }: { start: [number, number, number]; end: [number, number, number]; id: string }) {
  const ref = useRef<THREE.Mesh>(null)
  
  useEffect(() => {
    if (ref.current) {
      const startVec = new THREE.Vector3(...start)
      const endVec = new THREE.Vector3(...end)
      const direction = new THREE.Vector3().subVectors(endVec, startVec)
      const length = direction.length()
      
      ref.current.position.copy(startVec.clone().add(direction.clone().multiplyScalar(0.5)))
      ref.current.lookAt(endVec)
      ref.current.scale.set(0.1, 0.1, length)
    }
  }, [start, end])

  return (
    <mesh ref={ref}>
      <cylinderGeometry args={[1, 1, 1, 8]} />
      <meshStandardMaterial color="#64748b" />
    </mesh>
  )
}

// Scene component with all 3D objects
function Scene() {
  const { nodes, elements, selectedItems } = useModel()
  const controlsRef = useRef<any>()

  return (
    <>
      {/* Lighting */}
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} intensity={1} />
      <directionalLight position={[-10, -10, -5]} intensity={0.3} />

      {/* Grid */}
      <Grid
        args={[100, 100]}
        cellSize={1}
        cellThickness={0.5}
        cellColor="#334155"
        sectionSize={5}
        sectionThickness={1}
        sectionColor="#475569"
        fadeDistance={50}
        fadeStrength={1}
        followCamera={false}
        infiniteGrid={true}
      />

      {/* Axes Helper */}
      <axesHelper args={[5]} />

      {/* Render Nodes */}
      {nodes.map((node: any) => (
        <Node
          key={node.node_id || node.id}
          position={[node.x, node.z, -node.y]} // Convert to Three.js coordinates (Y-up)
          id={node.node_id || node.id}
          isSelected={selectedItems.has(node.node_id || node.id)}
        />
      ))}

      {/* Render Elements */}
      {elements.map((element: any) => {
        const startNode = nodes.find((n: any) => (n.node_id || n.id) === element.nodeI)
        const endNode = nodes.find((n: any) => (n.node_id || n.id) === element.nodeJ)
        
        if (startNode && endNode) {
          return (
            <Element
              key={element.id}
              start={[startNode.x, startNode.z, -startNode.y]}
              end={[endNode.x, endNode.z, -endNode.y]}
              id={element.id}
            />
          )
        }
        return null
      })}

      {/* Camera Controls */}
      <OrbitControls
        ref={controlsRef}
        enableDamping
        dampingFactor={0.05}
        rotateSpeed={0.5}
        zoomSpeed={0.8}
        panSpeed={0.5}
        minDistance={1}
        maxDistance={100}
      />
    </>
  )
}

export default function Viewport3D({ activeView = '3d' }: Viewport3DProps) {
  const { nodes, elements } = useModel()
  const canvasRef = useRef<HTMLDivElement>(null)

  return (
    <div ref={canvasRef} className="relative w-full h-full" style={{ background: '#0f172a' }}>
      <Canvas
        camera={{ position: [10, 10, 10], fov: 50 }}
        style={{ width: '100%', height: '100%' }}
      >
        <Scene />
      </Canvas>

      {/* Info Overlay */}
      <div className="absolute top-4 left-4 panel px-3 py-2 text-xs">
        <div style={{ color: 'var(--text-secondary)' }}>
          <div>Nodes: {nodes.length}</div>
          <div>Elements: {elements.length}</div>
          <div className="mt-2 text-xs" style={{ color: 'var(--text-tertiary)' }}>
            🖱️ Left-click + drag: Rotate
            <br />
            🖱️ Right-click + drag: Pan
            <br />
            🖱️ Scroll: Zoom
          </div>
        </div>
      </div>

      {/* Viewport Controls */}
      <ViewportControls
        onZoomIn={() => console.log('Zoom in')}
        onZoomOut={() => console.log('Zoom out')}
        onFit={() => console.log('Fit')}
        onReset={() => console.log('Reset')}
      />

      {/* Coordinate Axes Label */}
      <div className="absolute bottom-4 left-4 panel px-3 py-2 text-xs flex space-x-3">
        <span style={{ color: '#ef4444' }}>X</span>
        <span style={{ color: '#10b981' }}>Y</span>
        <span style={{ color: '#3b82f6' }}>Z</span>
      </div>
    </div>
  )
}
