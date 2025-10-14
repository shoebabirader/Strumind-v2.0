import { useEffect, useRef, useState } from 'react'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'

interface Enhanced3DViewerProps {
  modelData?: any
  analysisResults?: any
  showGrid?: boolean
  showAxes?: boolean
}

export default function Enhanced3DViewer({ 
  modelData, 
  analysisResults,
  showGrid = true,
  showAxes = true 
}: Enhanced3DViewerProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const sceneRef = useRef<THREE.Scene>()
  const rendererRef = useRef<THREE.WebGLRenderer>()
  const cameraRef = useRef<THREE.PerspectiveCamera>()
  const controlsRef = useRef<OrbitControls>()
  
  const [viewMode, setViewMode] = useState<'3d' | 'plan' | 'elevation'>('3d')
  const [displayMode, setDisplayMode] = useState<'wireframe' | 'solid' | 'rendered'>('solid')
  const [showDeformed, setShowDeformed] = useState(false)

  useEffect(() => {
    if (!containerRef.current) return

    // Scene setup
    const scene = new THREE.Scene()
    scene.background = new THREE.Color(0x1a1a1a)
    sceneRef.current = scene

    // Camera
    const camera = new THREE.PerspectiveCamera(
      60,
      containerRef.current.clientWidth / containerRef.current.clientHeight,
      0.1,
      1000
    )
    camera.position.set(15, 15, 15)
    cameraRef.current = camera

    // Renderer
    const renderer = new THREE.WebGLRenderer({ 
      antialias: true,
      alpha: true 
    })
    renderer.setSize(containerRef.current.clientWidth, containerRef.current.clientHeight)
    renderer.setPixelRatio(window.devicePixelRatio)
    renderer.shadowMap.enabled = true
    renderer.shadowMap.type = THREE.PCFSoftShadowMap
    containerRef.current.appendChild(renderer.domElement)
    rendererRef.current = renderer

    // Controls
    const controls = new OrbitControls(camera, renderer.domElement)
    controls.enableDamping = true
    controls.dampingFactor = 0.05
    controls.screenSpacePanning = false
    controls.minDistance = 5
    controls.maxDistance = 100
    controls.maxPolarAngle = Math.PI / 2
    controlsRef.current = controls

    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5)
    scene.add(ambientLight)

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8)
    directionalLight.position.set(20, 30, 20)
    directionalLight.castShadow = true
    directionalLight.shadow.mapSize.width = 2048
    directionalLight.shadow.mapSize.height = 2048
    scene.add(directionalLight)

    const hemisphereLight = new THREE.HemisphereLight(0xffffff, 0x444444, 0.4)
    scene.add(hemisphereLight)

    // Grid
    if (showGrid) {
      const gridHelper = new THREE.GridHelper(30, 30, 0x444444, 0x222222)
      scene.add(gridHelper)
    }

    // Axes
    if (showAxes) {
      const axesHelper = new THREE.AxesHelper(5)
      scene.add(axesHelper)
      
      // Add axis labels
      addAxisLabels(scene)
    }

    // Add sample structure
    addSampleStructure(scene)

    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate)
      controls.update()
      renderer.render(scene, camera)
    }
    animate()

    // Handle resize
    const handleResize = () => {
      if (!containerRef.current || !camera || !renderer) return
      camera.aspect = containerRef.current.clientWidth / containerRef.current.clientHeight
      camera.updateProjectionMatrix()
      renderer.setSize(containerRef.current.clientWidth, containerRef.current.clientHeight)
    }
    window.addEventListener('resize', handleResize)

    // Cleanup
    return () => {
      window.removeEventListener('resize', handleResize)
      renderer.dispose()
      containerRef.current?.removeChild(renderer.domElement)
    }
  }, [showGrid, showAxes])

  const addAxisLabels = (scene: THREE.Scene) => {
    const loader = new THREE.FontLoader()
    // In production, load actual font and create text labels
    // For now, using simple sprites
  }

  const addSampleStructure = (scene: THREE.Scene) => {
    // Material for concrete
    const concreteMaterial = new THREE.MeshStandardMaterial({ 
      color: 0xcccccc,
      roughness: 0.7,
      metalness: 0.1
    })

    // Material for steel
    const steelMaterial = new THREE.MeshStandardMaterial({ 
      color: 0x888888,
      roughness: 0.3,
      metalness: 0.8
    })

    // Create columns
    const columnGeometry = new THREE.BoxGeometry(0.3, 3, 0.3)
    const positions = [
      [0, 1.5, 0], [6, 1.5, 0], [12, 1.5, 0],
      [0, 1.5, 6], [6, 1.5, 6], [12, 1.5, 6],
      [0, 1.5, 12], [6, 1.5, 12], [12, 1.5, 12]
    ]
    
    positions.forEach((pos, idx) => {
      const column = new THREE.Mesh(columnGeometry, concreteMaterial)
      column.position.set(pos[0], pos[1], pos[2])
      column.castShadow = true
      column.receiveShadow = true
      column.userData = { type: 'column', id: `C${idx + 1}` }
      scene.add(column)
    })

    // Create beams
    const beamGeometry = new THREE.BoxGeometry(6, 0.3, 0.45)
    const beamPositions = [
      // X-direction beams
      [3, 3, 0, 0], [9, 3, 0, 0],
      [3, 3, 6, 0], [9, 3, 6, 0],
      [3, 3, 12, 0], [9, 3, 12, 0],
      // Y-direction beams
      [0, 3, 3, Math.PI/2], [0, 3, 9, Math.PI/2],
      [6, 3, 3, Math.PI/2], [6, 3, 9, Math.PI/2],
      [12, 3, 3, Math.PI/2], [12, 3, 9, Math.PI/2]
    ]

    beamPositions.forEach((pos, idx) => {
      const beam = new THREE.Mesh(beamGeometry, concreteMaterial)
      beam.position.set(pos[0], pos[1], pos[2])
      beam.rotation.y = pos[3]
      beam.castShadow = true
      beam.receiveShadow = true
      beam.userData = { type: 'beam', id: `B${idx + 1}` }
      scene.add(beam)
    })

    // Create slabs
    const slabGeometry = new THREE.BoxGeometry(6, 0.15, 6)
    const slabPositions = [
      [3, 3.15, 3], [9, 3.15, 3],
      [3, 3.15, 9], [9, 3.15, 9]
    ]

    slabPositions.forEach((pos, idx) => {
      const slab = new THREE.Mesh(slabGeometry, concreteMaterial)
      slab.position.set(pos[0], pos[1], pos[2])
      slab.castShadow = true
      slab.receiveShadow = true
      slab.userData = { type: 'slab', id: `S${idx + 1}` }
      scene.add(slab)
    })

    // Add ground plane
    const groundGeometry = new THREE.PlaneGeometry(40, 40)
    const groundMaterial = new THREE.MeshStandardMaterial({ 
      color: 0x333333,
      roughness: 0.8
    })
    const ground = new THREE.Mesh(groundGeometry, groundMaterial)
    ground.rotation.x = -Math.PI / 2
    ground.receiveShadow = true
    scene.add(ground)
  }

  const setView = (view: '3d' | 'plan' | 'elevation' | 'front' | 'side') => {
    if (!cameraRef.current || !controlsRef.current) return

    const camera = cameraRef.current
    const controls = controlsRef.current

    switch (view) {
      case '3d':
        camera.position.set(15, 15, 15)
        break
      case 'plan':
        camera.position.set(6, 30, 6)
        break
      case 'elevation':
        camera.position.set(6, 6, 30)
        break
      case 'front':
        camera.position.set(30, 6, 6)
        break
      case 'side':
        camera.position.set(6, 6, -30)
        break
    }

    controls.target.set(6, 3, 6)
    controls.update()
  }

  const zoomExtents = () => {
    if (!cameraRef.current || !controlsRef.current) return
    setView('3d')
  }

  return (
    <div className="relative w-full h-full">
      {/* 3D Viewport */}
      <div ref={containerRef} className="w-full h-full" />

      {/* View Controls Overlay */}
      <div className="absolute top-4 right-4 bg-white rounded-lg shadow-lg p-2 space-y-2">
        <button 
          onClick={() => setView('3d')}
          className="w-full px-3 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded flex items-center gap-2"
          title="3D View"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
          </svg>
          3D
        </button>
        <button 
          onClick={() => setView('plan')}
          className="w-full px-3 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded"
          title="Plan View"
        >
          Plan
        </button>
        <button 
          onClick={() => setView('elevation')}
          className="w-full px-3 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded"
          title="Elevation"
        >
          Elev
        </button>
        <button 
          onClick={zoomExtents}
          className="w-full px-3 py-2 text-sm bg-blue-500 text-white hover:bg-blue-600 rounded"
          title="Zoom Extents"
        >
          Zoom
        </button>
      </div>

      {/* Display Mode Controls */}
      <div className="absolute bottom-4 left-4 bg-white rounded-lg shadow-lg p-2 flex gap-2">
        <button 
          onClick={() => setDisplayMode('wireframe')}
          className={`px-3 py-2 text-sm rounded ${displayMode === 'wireframe' ? 'bg-blue-500 text-white' : 'bg-gray-100 hover:bg-gray-200'}`}
          title="Wireframe"
        >
          Wire
        </button>
        <button 
          onClick={() => setDisplayMode('solid')}
          className={`px-3 py-2 text-sm rounded ${displayMode === 'solid' ? 'bg-blue-500 text-white' : 'bg-gray-100 hover:bg-gray-200'}`}
          title="Solid"
        >
          Solid
        </button>
        <button 
          onClick={() => setDisplayMode('rendered')}
          className={`px-3 py-2 text-sm rounded ${displayMode === 'rendered' ? 'bg-blue-500 text-white' : 'bg-gray-100 hover:bg-gray-200'}`}
          title="Rendered"
        >
          Render
        </button>
      </div>

      {/* Analysis Display Toggle */}
      {analysisResults && (
        <div className="absolute bottom-4 right-4 bg-white rounded-lg shadow-lg p-2 space-y-2">
          <label className="flex items-center gap-2 px-3 py-2 text-sm cursor-pointer hover:bg-gray-100 rounded">
            <input 
              type="checkbox" 
              checked={showDeformed}
              onChange={(e) => setShowDeformed(e.target.checked)}
            />
            <span>Show Deformed</span>
          </label>
        </div>
      )}

      {/* View Cube (Top Right) */}
      <div className="absolute top-4 left-4 bg-white rounded-lg shadow-lg p-3">
        <div className="grid grid-cols-3 gap-1 w-24 h-24">
          <div className="col-start-2 bg-gray-200 hover:bg-blue-200 cursor-pointer flex items-center justify-center text-xs font-bold" onClick={() => setView('plan')}>
            TOP
          </div>
          <div className="row-start-2 bg-gray-200 hover:bg-blue-200 cursor-pointer flex items-center justify-center text-xs font-bold" onClick={() => setView('side')}>
            L
          </div>
          <div className="row-start-2 col-start-2 bg-blue-500 text-white flex items-center justify-center text-xs font-bold cursor-pointer" onClick={() => setView('3d')}>
            3D
          </div>
          <div className="row-start-2 col-start-3 bg-gray-200 hover:bg-blue-200 cursor-pointer flex items-center justify-center text-xs font-bold" onClick={() => setView('front')}>
            R
          </div>
          <div className="row-start-3 col-start-2 bg-gray-200 hover:bg-blue-200 cursor-pointer flex items-center justify-center text-xs font-bold" onClick={() => setView('elevation')}>
            FRT
          </div>
        </div>
      </div>
    </div>
  )
}
