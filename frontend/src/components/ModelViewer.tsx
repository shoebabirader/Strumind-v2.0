import { useEffect, useRef } from 'react'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'

interface ModelViewerProps {
  modelData?: any
  analysisResults?: any
}

export default function ModelViewer({ modelData, analysisResults }: ModelViewerProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const sceneRef = useRef<THREE.Scene>()
  const rendererRef = useRef<THREE.WebGLRenderer>()

  useEffect(() => {
    if (!containerRef.current) return

    // Scene setup
    const scene = new THREE.Scene()
    scene.background = new THREE.Color(0xf0f0f0)
    sceneRef.current = scene

    // Camera
    const camera = new THREE.PerspectiveCamera(
      75,
      containerRef.current.clientWidth / containerRef.current.clientHeight,
      0.1,
      1000
    )
    camera.position.set(10, 10, 10)

    // Renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true })
    renderer.setSize(containerRef.current.clientWidth, containerRef.current.clientHeight)
    containerRef.current.appendChild(renderer.domElement)
    rendererRef.current = renderer

    // Controls
    const controls = new OrbitControls(camera, renderer.domElement)
    controls.enableDamping = true

    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6)
    scene.add(ambientLight)
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8)
    directionalLight.position.set(10, 10, 5)
    scene.add(directionalLight)

    // Grid
    const gridHelper = new THREE.GridHelper(20, 20)
    scene.add(gridHelper)

    // Add sample structure
    addSampleStructure(scene)

    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate)
      controls.update()
      renderer.render(scene, camera)
    }
    animate()

    // Cleanup
    return () => {
      renderer.dispose()
      containerRef.current?.removeChild(renderer.domElement)
    }
  }, [])

  const addSampleStructure = (scene: THREE.Scene) => {
    const material = new THREE.MeshStandardMaterial({ color: 0xcccccc })

    // Columns
    const columnGeometry = new THREE.BoxGeometry(0.3, 3, 0.3)
    const positions = [
      [0, 1.5, 0], [5, 1.5, 0], [0, 1.5, 5], [5, 1.5, 5]
    ]
    positions.forEach(pos => {
      const column = new THREE.Mesh(columnGeometry, material)
      column.position.set(pos[0], pos[1], pos[2])
      scene.add(column)
    })

    // Beams
    const beamGeometry = new THREE.BoxGeometry(5, 0.3, 0.3)
    const beam1 = new THREE.Mesh(beamGeometry, material)
    beam1.position.set(2.5, 3, 0)
    scene.add(beam1)
  }

  return <div ref={containerRef} className="w-full h-full" />
}
