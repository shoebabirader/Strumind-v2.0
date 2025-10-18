'use client';

import { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';
import { useNodes } from '@/hooks/useNodes';
import { useElements } from '@/hooks/useElements';
import { useModelStore } from '@/stores/modelStore';
import { ViewportControls } from './ViewportControls';
import { Info } from 'lucide-react';

// Dynamically import the Canvas3D client component to avoid SSR issues
const Canvas3DClient = dynamic(() => import('./Canvas3DClient').then(mod => mod.Canvas3DClient), { 
  ssr: false,
  loading: () => (
    <div className="w-full h-full flex items-center justify-center bg-zinc-900">
      <div className="text-zinc-400">Loading 3D viewport...</div>
    </div>
  )
});

type ViewMode = 'wireframe' | 'solid' | 'shaded' | 'rendered' | 'xray';
type SelectionMode = 'node' | 'element' | 'area' | 'pan';
type ColorMode = 'material' | 'stress' | 'displacement' | 'force';

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
  const [isMounted, setIsMounted] = useState(false);

  // Ensure component only renders on client
  useEffect(() => {
    setIsMounted(true);
  }, []);

  const handleViewChange = (view: string) => {
    // View change logic handled by Canvas3DClient
    console.log('View changed to:', view);
  };

  const handleZoomExtents = () => {
    console.log('Zoom extents');
  };

  const handleScreenshot = () => {
    console.log('Screenshot captured');
  };

  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      if (!e.key) return; // Guard against undefined key
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

  // Show loading state until mounted
  if (!isMounted) {
    return (
      <div className="relative w-full h-full bg-zinc-900 flex items-center justify-center">
        <div className="text-zinc-400">Loading 3D viewport...</div>
      </div>
    );
  }

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
        <div className="absolute top-4 left-4 bg-black/50 backdrop-blur-sm text-white px-4 py-2 rounded-lg text-sm space-y-1 z-10">
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
        <div className="absolute bottom-4 left-4 bg-black/50 backdrop-blur-sm text-white px-4 py-2 rounded-lg text-sm z-10">
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

      {/* Enhanced 2D/3D Canvas Viewer */}
      <canvas
        ref={(canvas) => {
          if (!canvas || !isMounted) return;
          
          const ctx = canvas.getContext('2d');
          if (!ctx) return;
          
          // Set canvas size
          canvas.width = canvas.offsetWidth;
          canvas.height = canvas.offsetHeight;
          
          // Clear canvas
          ctx.fillStyle = '#18181b'; // zinc-900
          ctx.fillRect(0, 0, canvas.width, canvas.height);
          
          // Draw grid
          if (showGrid) {
            ctx.strokeStyle = '#3f3f46'; // zinc-700
            ctx.lineWidth = 0.5;
            const gridSize = 50;
            
            for (let x = 0; x < canvas.width; x += gridSize) {
              ctx.beginPath();
              ctx.moveTo(x, 0);
              ctx.lineTo(x, canvas.height);
              ctx.stroke();
            }
            
            for (let y = 0; y < canvas.height; y += gridSize) {
              ctx.beginPath();
              ctx.moveTo(0, y);
              ctx.lineTo(canvas.width, y);
              ctx.stroke();
            }
          }
          
          // Draw axes
          if (showAxes) {
            const centerX = canvas.width / 2;
            const centerY = canvas.height / 2;
            const axisLength = 100;
            
            // X-axis (red)
            ctx.strokeStyle = '#ef4444';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.lineTo(centerX + axisLength, centerY);
            ctx.stroke();
            ctx.fillStyle = '#ef4444';
            ctx.font = '14px sans-serif';
            ctx.fillText('X', centerX + axisLength + 10, centerY);
            
            // Y-axis (green)
            ctx.strokeStyle = '#22c55e';
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.lineTo(centerX, centerY - axisLength);
            ctx.stroke();
            ctx.fillStyle = '#22c55e';
            ctx.fillText('Y', centerX, centerY - axisLength - 10);
            
            // Z-axis (blue) - diagonal for 3D effect
            ctx.strokeStyle = '#3b82f6';
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.lineTo(centerX - axisLength * 0.7, centerY + axisLength * 0.7);
            ctx.stroke();
            ctx.fillStyle = '#3b82f6';
            ctx.fillText('Z', centerX - axisLength * 0.7 - 20, centerY + axisLength * 0.7 + 10);
          }
          
          // Draw nodes
          if (nodes.length > 0) {
            const scale = 50;
            const offsetX = canvas.width / 2;
            const offsetY = canvas.height / 2;
            
            nodes.forEach((node) => {
              const x = offsetX + node.x * scale;
              const y = offsetY - node.y * scale; // Invert Y for screen coordinates
              
              // Draw node
              ctx.fillStyle = selectionMode === 'node' ? '#3b82f6' : '#6b7280';
              ctx.beginPath();
              ctx.arc(x, y, 6, 0, Math.PI * 2);
              ctx.fill();
              
              // Draw node label
              if (showLabels) {
                ctx.fillStyle = '#ffffff';
                ctx.font = '10px sans-serif';
                ctx.fillText(`N${node.id}`, x + 10, y - 10);
              }
            });
          }
          
          // Draw elements
          if (elements.length > 0 && nodes.length > 0) {
            const scale = 50;
            const offsetX = canvas.width / 2;
            const offsetY = canvas.height / 2;
            
            elements.forEach((element) => {
              const nodeI = nodes.find(n => n.id === element.node_i);
              const nodeJ = nodes.find(n => n.id === element.node_j);
              
              if (nodeI && nodeJ) {
                const x1 = offsetX + nodeI.x * scale;
                const y1 = offsetY - nodeI.y * scale;
                const x2 = offsetX + nodeJ.x * scale;
                const y2 = offsetY - nodeJ.y * scale;
                
                // Draw element
                ctx.strokeStyle = selectionMode === 'element' ? '#10b981' : '#9ca3af';
                ctx.lineWidth = viewMode === 'wireframe' ? 1 : 3;
                ctx.beginPath();
                ctx.moveTo(x1, y1);
                ctx.lineTo(x2, y2);
                ctx.stroke();
                
                // Draw element label
                if (showLabels) {
                  const midX = (x1 + x2) / 2;
                  const midY = (y1 + y2) / 2;
                  ctx.fillStyle = '#ffffff';
                  ctx.font = '10px sans-serif';
                  ctx.fillText(`E${element.id}`, midX + 5, midY - 5);
                }
              }
            });
          }
          
          // Draw empty state
          if (nodes.length === 0 && elements.length === 0) {
            ctx.fillStyle = '#71717a';
            ctx.font = '16px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('No model loaded', canvas.width / 2, canvas.height / 2 - 20);
            ctx.font = '12px sans-serif';
            ctx.fillText('Create nodes and elements to start building', canvas.width / 2, canvas.height / 2 + 10);
          }
        }}
        className="w-full h-full"
      />

      {/* Empty State */}
      {nodes.length === 0 && elements.length === 0 && (
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none z-10">
          <div className="text-center text-zinc-400">
            <p className="text-lg mb-2">No model loaded</p>
            <p className="text-sm">Create nodes and elements to start building</p>
          </div>
        </div>
      )}
    </div>
  );
}
