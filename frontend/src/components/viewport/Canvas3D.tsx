'use client';

import { useRef, useState, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Grid, GizmoHelper, GizmoViewport, PerspectiveCamera } from '@react-three/drei';
import { useNodes } from '@/hooks/useNodes';
import { useElements } from '@/hooks/useElements';
import { useModelStore } from '@/stores/modelStore';
import { ViewportControls } from './ViewportControls';
import { Button } from '@/components/ui/button';
import { Info } from 'lucide-react';

type ViewMode = 'wireframe' | 'solid' | 'shaded' | 'rendered' | 'xray';
type SelectionMode = 'node' | 'element' | 'area' | 'pan';
type ColorMode = 'material' | 'stress' | 'displacement' | 'force';

function NodeRenderer({ nodes, selectionMode }: { nodes: any[]; selectionMode: SelectionMode }) {
  return (
    <>
      {nodes.map((node) => (
        <mesh key={node.id} position={[node.x, node.y, node.z]}>
          <sphereGeometry args={[0.15, 16, 16]} />
          <meshStandardMaterial 
            color={selectionMode === 'node' ? '#3b82f6' : '#6b7280'} 
            emissive={selectionMode === 'node' ? '#1e40af' : '#000000'}
            emissiveIntensity={0.2}
          />
        </mesh>
      ))}
    </>
  );
}

function ElementRenderer({ 
  elements, 
  nodes, 
  viewMode,
  selectionMode 
}: { 
  elements: any[]; 
  nodes: any[];
  viewMode: ViewMode;
  selectionMode: SelectionMode;
}) {
  const getNodePosition = (nodeId: number) => {
    const node = nodes.find(n => n.id === nodeId);
    return node ? [node.x, node.y, node.z] : [0, 0, 0];
  };

  const getElementColor = () => {
    if (selectionMode === 'element') return '#10b981';
    return '#6b7280';
  };

  const isWireframe = viewMode === 'wireframe';
  const opacity = viewMode === 'xray' ? 0.3 : 1;

  return (
    <>
      {elements.map((element) => {
        const start = getNodePosition(element.node_i);
        const end = getNodePosition(element.node_j);
        const length = Math.sqrt(
          Math.pow(end[0] - start[0], 2) +
          Math.pow(end[1] - start[1], 2) +
          Math.pow(end[2] - start[2], 2)
        );
        const midpoint = [
          (start[0] + end[0]) / 2,
          (start[1] + end[1]) / 2,
          (start[2] + end[2]) / 2,
        ];

        return (
          <group key={element.id}>
            <mesh position={midpoint as [number, number, number]}>
              <cylinderGeometry args={[0.08, 0.08, length, 8]} />
              <meshStandardMaterial 
                color={getElementColor()}
                wireframe={isWireframe}
                transparent={viewMode === 'xray'}
                opacity={opacity}
                metalness={viewMode === 'rendered' ? 0.3 : 0}
                roughness={viewMode === 'rendered' ? 0.7 : 1}
              />
            </mesh>
          </group>
        );
      })}
    </>
  );
}

export function Canvas3D() {
  const { currentProject } = useModelStore();
  const { nodes } = useNodes(currentProject?.id);
  const { elements } = useElements(currentProject?.id);
  
  const [viewMode, setViewMode] = useState<ViewMode>('shaded');
  const [selectionMode, setSelectionMode] = useState<SelectionMode>('node');
  const [colorMode, setColorMode] = useState<ColorMode>('material');
  const [showGrid, setShowGrid] = useState(true);
  const [showAxes, setShowAxes] = useState(true);
  const [showDimensions, setShowDimensions] = useState(false);
  const [showLabels, setShowLabels] = useState(false);
  const [isAnimating, setIsAnimating] = useState(false);
  const [animationSpeed, setAnimationSpeed] = useState(1);
  const [showStats, setShowStats] = useState(true);

  const cameraRef = useRef<any>();
  const controlsRef = useRef<any>();

  const handleViewChange = (view: string) => {
    if (!cameraRef.current || !controlsRef.current) return;

    const distance = 15;
    const positions: Record<string, [number, number, number]> = {
      isometric: [distance, distance, distance],
      top: [0, distance, 0],
      front: [0, 0, distance],
      side: [distance, 0, 0],
    };

    const pos = positions[view];
    if (pos) {
      cameraRef.current.position.set(...pos);
      controlsRef.current.target.set(0, 0, 0);
      controlsRef.current.update();
    }
  };

  const handleZoomExtents = () => {
    if (!controlsRef.current) return;
    controlsRef.current.reset();
  };

  const handleScreenshot = () => {
    // Screenshot functionality
    console.log('Screenshot captured');
  };

  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      switch(e.key.toLowerCase()) {
        case 'i': handleViewChange('isometric'); break;
        case 't': handleViewChange('top'); break;
        case 'f': handleViewChange('front'); break;
        case 's': handleViewChange('side'); break;
        case 'e': handleZoomExtents(); break;
        case 'r': handleZoomExtents(); break;
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, []);

  return (
    <div className="relative w-full h-full bg-zinc-900">
      {/* Viewport Controls */}
      <ViewportControls
        viewMode={viewMode}
        setViewMode={setViewMode}
        selectionMode={selectionMode}
        setSelectionMode={setSelectionMode}
        colorMode={colorMode}
        setColorMode={setColorMode}
        showGrid={showGrid}
        setShowGrid={setShowGrid}
        showAxes={showAxes}
        setShowAxes={setShowAxes}
        showDimensions={showDimensions}
        setShowDimensions={setShowDimensions}
        showLabels={showLabels}
        setShowLabels={setShowLabels}
        isAnimating={isAnimating}
        setIsAnimating={setIsAnimating}
        animationSpeed={animationSpeed}
        setAnimationSpeed={setAnimationSpeed}
        onViewChange={handleViewChange}
        onZoomExtents={handleZoomExtents}
        onScreenshot={handleScreenshot}
      />

      {/* Stats Display */}
      {showStats && (
        <div className="absolute top-4 left-4 bg-black/50 backdrop-blur-sm text-white px-4 py-2 rounded-lg text-sm space-y-1">
          <div className="flex items-center gap-2">
            <Info className="w-4 h-4" />
            <span className="font-semibold">Model Info</span>
          </div>
          <div>Nodes: {nodes.length}</div>
          <div>Elements: {elements.length}</div>
          <div>View: {viewMode}</div>
        </div>
      )}

      {/* Axis Legend */}
      {showAxes && (
        <div className="absolute bottom-4 left-4 bg-black/50 backdrop-blur-sm text-white px-4 py-2 rounded-lg text-sm">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <div className="w-4 h-1 bg-red-500"></div>
              <span>X-Axis</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-1 bg-green-500"></div>
              <span>Y-Axis</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-1 bg-blue-500"></div>
              <span>Z-Axis</span>
            </div>
          </div>
        </div>
      )}

      {/* 3D Canvas */}
      <Canvas shadows>
        <PerspectiveCamera ref={cameraRef} makeDefault position={[10, 10, 10]} fov={50} />
        
        <ambientLight intensity={0.4} />
        <directionalLight 
          position={[10, 10, 5]} 
          intensity={viewMode === 'rendered' ? 1.2 : 0.8}
          castShadow={viewMode === 'rendered'}
        />
        <pointLight position={[-10, -10, -5]} intensity={0.3} />
        
        {showGrid && (
          <Grid
            args={[30, 30]}
            cellSize={1}
            cellThickness={0.5}
            cellColor="#4b5563"
            sectionSize={5}
            sectionThickness={1}
            sectionColor="#6b7280"
            fadeDistance={50}
            fadeStrength={1}
            followCamera={false}
          />
        )}

        <NodeRenderer nodes={nodes} selectionMode={selectionMode} />
        <ElementRenderer 
          elements={elements} 
          nodes={nodes}
          viewMode={viewMode}
          selectionMode={selectionMode}
        />

        <OrbitControls 
          ref={controlsRef}
          makeDefault 
          enableDamping
          dampingFactor={0.05}
        />
        
        {showAxes && (
          <GizmoHelper alignment="bottom-right" margin={[80, 80]}>
            <GizmoViewport 
              axisColors={['#ef4444', '#22c55e', '#3b82f6']} 
              labelColor="white"
            />
          </GizmoHelper>
        )}
      </Canvas>

      {/* Empty State */}
      {nodes.length === 0 && elements.length === 0 && (
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div className="text-center text-zinc-400">
            <p className="text-lg mb-2">No model loaded</p>
            <p className="text-sm">Create nodes and elements to start building</p>
          </div>
        </div>
      )}
    </div>
  );
}
