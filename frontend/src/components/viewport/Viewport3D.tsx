'use client';

import { useRef, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Grid, GizmoHelper, GizmoViewport } from '@react-three/drei';
import { useNodes } from '@/hooks/useNodes';
import { useElements } from '@/hooks/useElements';
import { useModelStore } from '@/stores/modelStore';

function NodeRenderer({ nodes }: { nodes: any[] }) {
  return (
    <>
      {nodes.map((node) => (
        <mesh key={node.id} position={[node.x, node.y, node.z]}>
          <sphereGeometry args={[0.1, 16, 16]} />
          <meshStandardMaterial color="#3b82f6" />
        </mesh>
      ))}
    </>
  );
}

function ElementRenderer({ elements, nodes }: { elements: any[]; nodes: any[] }) {
  const getNodePosition = (nodeId: number) => {
    const node = nodes.find(n => n.id === nodeId);
    return node ? [node.x, node.y, node.z] : [0, 0, 0];
  };

  return (
    <>
      {elements.map((element) => {
        const start = getNodePosition(element.node_i);
        const end = getNodePosition(element.node_j);
        const midpoint = [
          (start[0] + end[0]) / 2,
          (start[1] + end[1]) / 2,
          (start[2] + end[2]) / 2,
        ];

        return (
          <group key={element.id}>
            <mesh position={midpoint as [number, number, number]}>
              <cylinderGeometry args={[0.05, 0.05, 1, 8]} />
              <meshStandardMaterial color="#10b981" />
            </mesh>
          </group>
        );
      })}
    </>
  );
}

export function Viewport3D() {
  const { currentProject } = useModelStore();
  const { nodes } = useNodes(currentProject?.id);
  const { elements } = useElements(currentProject?.id);

  return (
    <div className="w-full h-full">
      <Canvas camera={{ position: [10, 10, 10], fov: 50 }}>
        <ambientLight intensity={0.5} />
        <directionalLight position={[10, 10, 5]} intensity={1} />
        
        <Grid
          args={[20, 20]}
          cellSize={1}
          cellThickness={0.5}
          cellColor="#6b7280"
          sectionSize={5}
          sectionThickness={1}
          sectionColor="#374151"
          fadeDistance={30}
          fadeStrength={1}
          followCamera={false}
        />

        <NodeRenderer nodes={nodes} />
        <ElementRenderer elements={elements} nodes={nodes} />

        <OrbitControls makeDefault />
        
        <GizmoHelper alignment="bottom-right" margin={[80, 80]}>
          <GizmoViewport axisColors={['#ef4444', '#22c55e', '#3b82f6']} labelColor="white" />
        </GizmoHelper>
      </Canvas>
    </div>
  );
}
