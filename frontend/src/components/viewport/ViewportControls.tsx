'use client';

import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { Slider } from '@/components/ui/slider';
import { Separator } from '@/components/ui/separator';
import {
  MousePointer2,
  Crosshair,
  Square,
  Hand,
  Box,
  Grid3x3,
  Eye,
  EyeOff,
  Camera,
  ZoomIn,
  ZoomOut,
  Maximize2,
  RotateCcw,
  Play,
  Pause,
  SkipForward,
  SkipBack,
  Settings,
  Ruler,
  Scissors,
  Palette,
  Share2,
  Download,
  HelpCircle,
} from 'lucide-react';

type ViewMode = 'wireframe' | 'solid' | 'shaded' | 'rendered' | 'xray';
type SelectionMode = 'node' | 'element' | 'area' | 'pan';
type ColorMode = 'material' | 'stress' | 'displacement' | 'force';

interface ViewportControlsProps {
  viewMode: ViewMode;
  setViewMode: (mode: ViewMode) => void;
  selectionMode: SelectionMode;
  setSelectionMode: (mode: SelectionMode) => void;
  colorMode: ColorMode;
  setColorMode: (mode: ColorMode) => void;
  showGrid: boolean;
  setShowGrid: (show: boolean) => void;
  showAxes: boolean;
  setShowAxes: (show: boolean) => void;
  showDimensions: boolean;
  setShowDimensions: (show: boolean) => void;
  showLabels: boolean;
  setShowLabels: (show: boolean) => void;
  isAnimating: boolean;
  setIsAnimating: (animating: boolean) => void;
  animationSpeed: number;
  setAnimationSpeed: (speed: number) => void;
  onViewChange: (view: string) => void;
  onZoomExtents: () => void;
  onScreenshot: () => void;
}

export function ViewportControls({
  viewMode,
  setViewMode,
  selectionMode,
  setSelectionMode,
  colorMode,
  setColorMode,
  showGrid,
  setShowGrid,
  showAxes,
  setShowAxes,
  showDimensions,
  setShowDimensions,
  showLabels,
  setShowLabels,
  isAnimating,
  setIsAnimating,
  animationSpeed,
  setAnimationSpeed,
  onViewChange,
  onZoomExtents,
  onScreenshot,
}: ViewportControlsProps) {
  return (
    <>
      {/* Top Toolbar */}
      <div className="absolute top-4 right-4 z-10 flex gap-2">
        {/* Selection Mode */}
        <div className="bg-black/50 backdrop-blur-sm rounded-lg p-1 flex gap-1">
          <Button
            size="sm"
            variant={selectionMode === 'node' ? 'default' : 'ghost'}
            onClick={() => setSelectionMode('node')}
            className="h-8 w-8 p-0"
            title="Select Nodes"
          >
            <Crosshair className="w-4 h-4" />
          </Button>
          <Button
            size="sm"
            variant={selectionMode === 'element' ? 'default' : 'ghost'}
            onClick={() => setSelectionMode('element')}
            className="h-8 w-8 p-0"
            title="Select Elements"
          >
            <MousePointer2 className="w-4 h-4" />
          </Button>
          <Button
            size="sm"
            variant={selectionMode === 'area' ? 'default' : 'ghost'}
            onClick={() => setSelectionMode('area')}
            className="h-8 w-8 p-0"
            title="Area Selection"
          >
            <Square className="w-4 h-4" />
          </Button>
          <Button
            size="sm"
            variant={selectionMode === 'pan' ? 'default' : 'ghost'}
            onClick={() => setSelectionMode('pan')}
            className="h-8 w-8 p-0"
            title="Pan Mode"
          >
            <Hand className="w-4 h-4" />
          </Button>
        </div>

        {/* View Mode */}
        <div className="bg-black/50 backdrop-blur-sm rounded-lg p-1">
          <Select value={viewMode} onValueChange={(v) => setViewMode(v as ViewMode)}>
            <SelectTrigger className="h-8 w-32 bg-transparent border-0 text-white">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="wireframe">Wireframe</SelectItem>
              <SelectItem value="solid">Solid</SelectItem>
              <SelectItem value="shaded">Shaded</SelectItem>
              <SelectItem value="rendered">Rendered</SelectItem>
              <SelectItem value="xray">X-Ray</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* Quick Actions */}
        <div className="bg-black/50 backdrop-blur-sm rounded-lg p-1 flex gap-1">
          <Button
            size="sm"
            variant="ghost"
            onClick={onScreenshot}
            className="h-8 w-8 p-0 text-white hover:text-white"
            title="Screenshot"
          >
            <Camera className="w-4 h-4" />
          </Button>
          <Button
            size="sm"
            variant="ghost"
            className="h-8 w-8 p-0 text-white hover:text-white"
            title="Export"
          >
            <Download className="w-4 h-4" />
          </Button>
          <Button
            size="sm"
            variant="ghost"
            className="h-8 w-8 p-0 text-white hover:text-white"
            title="Share"
          >
            <Share2 className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* Right Sidebar - View Controls */}
      <div className="absolute top-20 right-4 z-10 space-y-2">
        {/* Standard Views */}
        <div className="bg-black/50 backdrop-blur-sm rounded-lg p-2 space-y-1">
          <Button
            size="sm"
            variant="ghost"
            onClick={() => onViewChange('isometric')}
            className="w-full justify-start text-white hover:text-white text-xs"
            title="Isometric (I)"
          >
            <Box className="w-3 h-3 mr-2" />
            Isometric
          </Button>
          <Button
            size="sm"
            variant="ghost"
            onClick={() => onViewChange('top')}
            className="w-full justify-start text-white hover:text-white text-xs"
            title="Top View (T)"
          >
            Top
          </Button>
          <Button
            size="sm"
            variant="ghost"
            onClick={() => onViewChange('front')}
            className="w-full justify-start text-white hover:text-white text-xs"
            title="Front View (F)"
          >
            Front
          </Button>
          <Button
            size="sm"
            variant="ghost"
            onClick={() => onViewChange('side')}
            className="w-full justify-start text-white hover:text-white text-xs"
            title="Side View (S)"
          >
            Side
          </Button>
          <Separator className="my-1" />
          <Button
            size="sm"
            variant="ghost"
            className="w-full justify-start text-white hover:text-white text-xs"
            title="Zoom In (+)"
          >
            <ZoomIn className="w-3 h-3 mr-2" />
            Zoom In
          </Button>
          <Button
            size="sm"
            variant="ghost"
            className="w-full justify-start text-white hover:text-white text-xs"
            title="Zoom Out (-)"
          >
            <ZoomOut className="w-3 h-3 mr-2" />
            Zoom Out
          </Button>
          <Button
            size="sm"
            variant="ghost"
            onClick={onZoomExtents}
            className="w-full justify-start text-white hover:text-white text-xs"
            title="Zoom Extents (E)"
          >
            <Maximize2 className="w-3 h-3 mr-2" />
            Extents
          </Button>
          <Button
            size="sm"
            variant="ghost"
            onClick={onZoomExtents}
            className="w-full justify-start text-white hover:text-white text-xs"
            title="Reset View (R)"
          >
            <RotateCcw className="w-3 h-3 mr-2" />
            Reset
          </Button>
        </div>

        {/* Display Options */}
        <Popover>
          <PopoverTrigger asChild>
            <Button
              size="sm"
              variant="ghost"
              className="w-full bg-black/50 backdrop-blur-sm text-white hover:text-white"
            >
              <Settings className="w-4 h-4 mr-2" />
              Display
            </Button>
          </PopoverTrigger>
          <PopoverContent className="w-56" align="end">
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <label className="text-sm">Grid</label>
                <input
                  type="checkbox"
                  checked={showGrid}
                  onChange={(e) => setShowGrid(e.target.checked)}
                  className="w-4 h-4"
                />
              </div>
              <div className="flex items-center justify-between">
                <label className="text-sm">Axes</label>
                <input
                  type="checkbox"
                  checked={showAxes}
                  onChange={(e) => setShowAxes(e.target.checked)}
                  className="w-4 h-4"
                />
              </div>
              <div className="flex items-center justify-between">
                <label className="text-sm">Dimensions</label>
                <input
                  type="checkbox"
                  checked={showDimensions}
                  onChange={(e) => setShowDimensions(e.target.checked)}
                  className="w-4 h-4"
                />
              </div>
              <div className="flex items-center justify-between">
                <label className="text-sm">Labels</label>
                <input
                  type="checkbox"
                  checked={showLabels}
                  onChange={(e) => setShowLabels(e.target.checked)}
                  className="w-4 h-4"
                />
              </div>
            </div>
          </PopoverContent>
        </Popover>

        {/* Tools */}
        <div className="bg-black/50 backdrop-blur-sm rounded-lg p-2 space-y-1">
          <Button
            size="sm"
            variant="ghost"
            className="w-full justify-start text-white hover:text-white text-xs"
            title="Measure"
          >
            <Ruler className="w-3 h-3 mr-2" />
            Measure
          </Button>
          <Button
            size="sm"
            variant="ghost"
            className="w-full justify-start text-white hover:text-white text-xs"
            title="Section Cut"
          >
            <Scissors className="w-3 h-3 mr-2" />
            Section
          </Button>
        </div>

        {/* Color Coding */}
        <Popover>
          <PopoverTrigger asChild>
            <Button
              size="sm"
              variant="ghost"
              className="w-full bg-black/50 backdrop-blur-sm text-white hover:text-white"
            >
              <Palette className="w-4 h-4 mr-2" />
              Color By
            </Button>
          </PopoverTrigger>
          <PopoverContent className="w-56" align="end">
            <div className="space-y-2">
              <Button
                size="sm"
                variant={colorMode === 'material' ? 'default' : 'ghost'}
                onClick={() => setColorMode('material')}
                className="w-full justify-start"
              >
                Material
              </Button>
              <Button
                size="sm"
                variant={colorMode === 'stress' ? 'default' : 'ghost'}
                onClick={() => setColorMode('stress')}
                className="w-full justify-start"
              >
                Stress
              </Button>
              <Button
                size="sm"
                variant={colorMode === 'displacement' ? 'default' : 'ghost'}
                onClick={() => setColorMode('displacement')}
                className="w-full justify-start"
              >
                Displacement
              </Button>
              <Button
                size="sm"
                variant={colorMode === 'force' ? 'default' : 'ghost'}
                onClick={() => setColorMode('force')}
                className="w-full justify-start"
              >
                Force
              </Button>
            </div>
          </PopoverContent>
        </Popover>
      </div>

      {/* Bottom Animation Controls */}
      <div className="absolute bottom-4 right-4 z-10">
        <div className="bg-black/50 backdrop-blur-sm rounded-lg p-2 flex items-center gap-2">
          <Button
            size="sm"
            variant="ghost"
            className="h-8 w-8 p-0 text-white hover:text-white"
            title="Previous Frame"
          >
            <SkipBack className="w-4 h-4" />
          </Button>
          <Button
            size="sm"
            variant="ghost"
            onClick={() => setIsAnimating(!isAnimating)}
            className="h-8 w-8 p-0 text-white hover:text-white"
            title={isAnimating ? 'Pause' : 'Play'}
          >
            {isAnimating ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
          </Button>
          <Button
            size="sm"
            variant="ghost"
            className="h-8 w-8 p-0 text-white hover:text-white"
            title="Next Frame"
          >
            <SkipForward className="w-4 h-4" />
          </Button>
          <Separator orientation="vertical" className="h-6 mx-1" />
          <div className="flex items-center gap-2 px-2">
            <span className="text-white text-xs whitespace-nowrap">Speed:</span>
            <Slider
              value={[animationSpeed]}
              onValueChange={(v) => setAnimationSpeed(v[0])}
              min={0.1}
              max={5}
              step={0.1}
              className="w-24"
            />
            <span className="text-white text-xs w-8">{animationSpeed.toFixed(1)}x</span>
          </div>
        </div>
      </div>

      {/* Keyboard Shortcuts Help */}
      <Popover>
        <PopoverTrigger asChild>
          <Button
            size="sm"
            variant="ghost"
            className="absolute bottom-4 left-48 z-10 bg-black/50 backdrop-blur-sm text-white hover:text-white"
          >
            <HelpCircle className="w-4 h-4 mr-2" />
            Shortcuts (?)
          </Button>
        </PopoverTrigger>
        <PopoverContent className="w-72" align="start">
          <div className="space-y-2">
            <h4 className="font-semibold mb-2">Keyboard Shortcuts</h4>
            <div className="space-y-1 text-sm">
              <div className="flex justify-between">
                <span>Isometric View</span>
                <kbd className="px-2 py-1 bg-zinc-100 rounded">I</kbd>
              </div>
              <div className="flex justify-between">
                <span>Top View</span>
                <kbd className="px-2 py-1 bg-zinc-100 rounded">T</kbd>
              </div>
              <div className="flex justify-between">
                <span>Front View</span>
                <kbd className="px-2 py-1 bg-zinc-100 rounded">F</kbd>
              </div>
              <div className="flex justify-between">
                <span>Side View</span>
                <kbd className="px-2 py-1 bg-zinc-100 rounded">S</kbd>
              </div>
              <div className="flex justify-between">
                <span>Zoom Extents</span>
                <kbd className="px-2 py-1 bg-zinc-100 rounded">E</kbd>
              </div>
              <div className="flex justify-between">
                <span>Reset View</span>
                <kbd className="px-2 py-1 bg-zinc-100 rounded">R</kbd>
              </div>
              <div className="flex justify-between">
                <span>Zoom In/Out</span>
                <kbd className="px-2 py-1 bg-zinc-100 rounded">+/-</kbd>
              </div>
            </div>
          </div>
        </PopoverContent>
      </Popover>
    </>
  );
}
