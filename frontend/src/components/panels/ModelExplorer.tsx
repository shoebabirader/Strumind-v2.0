import React, { useState } from 'react'
import { Settings, ChevronRight, ChevronDown, Box, Grid, Layers, Zap, Building } from 'lucide-react'
import { useModel } from '@/contexts/ModelContext'
import { useSelectionContext } from '@/contexts/SelectionContext'
import ContextMenu, { Plus, Edit, Trash2 } from '@/components/ui/ContextMenu'

interface TreeNodeProps {
  id: string
  label: string
  icon?: React.ReactNode
  expanded?: boolean
  onToggle?: () => void
  onContextMenu?: (e: React.MouseEvent) => void
  children?: React.ReactNode
}

function TreeNode({ label, icon, expanded, onToggle, onContextMenu, children }: TreeNodeProps) {
  return (
    <div>
      <div 
        className="tree-node flex items-center space-x-1 justify-between group" 
        onClick={onToggle}
        onContextMenu={onContextMenu}
      >
        <div className="flex items-center space-x-1">
          {onToggle && (expanded ? <ChevronDown className="w-3 h-3" /> : <ChevronRight className="w-3 h-3" />)}
          {icon}
          <span>{label}</span>
        </div>
      </div>
      {expanded && children && (
        <div className="ml-4 border-l pl-2" style={{ borderColor: 'var(--border-primary)' }}>
          {children}
        </div>
      )}
    </div>
  )
}

function TreeLeaf({ label, onClick, onContextMenu }: { label: string; onClick?: () => void; onContextMenu?: (e: React.MouseEvent) => void }) {
  return (
    <div 
      className="tree-node flex items-center space-x-1 pl-4 hover:bg-gray-700 cursor-pointer" 
      onClick={onClick}
      onContextMenu={onContextMenu}
      style={{ color: 'var(--text-secondary)' }}
    >
      <div className="w-3 h-3" />
      <span>{label}</span>
    </div>
  )
}

interface ModelExplorerProps {
  onNodeDialog?: () => void
  onElementDialog?: () => void
  onMaterialDialog?: () => void
  onLoadDialog?: () => void
}

export default function ModelExplorer({ onNodeDialog, onElementDialog, onMaterialDialog, onLoadDialog }: ModelExplorerProps) {
  const { nodes, elements, materials } = useModel()
  const { setSelectedItem } = useSelectionContext()
  const [expandedNodes, setExpandedNodes] = useState(new Set(['model', 'geometry', 'properties']))
  const [contextMenu, setContextMenu] = useState<{ x: number; y: number; type: string } | null>(null)

  const toggleNode = (id: string) => {
    const newExpanded = new Set(expandedNodes)
    newExpanded.has(id) ? newExpanded.delete(id) : newExpanded.add(id)
    setExpandedNodes(newExpanded)
  }

  const handleContextMenu = (e: React.MouseEvent, type: string) => {
    e.preventDefault()
    setContextMenu({ x: e.clientX, y: e.clientY, type })
  }

  const getContextMenuItems = () => {
    if (!contextMenu) return []
    
    switch (contextMenu.type) {
      case 'nodes':
        return [
          { label: 'Add Node', icon: <Plus className="w-4 h-4" />, onClick: () => onNodeDialog?.() }
        ]
      case 'elements':
        return [
          { label: 'Add Element', icon: <Plus className="w-4 h-4" />, onClick: () => onElementDialog?.() }
        ]
      case 'materials':
        return [
          { label: 'Add Material', icon: <Plus className="w-4 h-4" />, onClick: () => onMaterialDialog?.() }
        ]
      case 'loads':
        return [
          { label: 'Add Load', icon: <Plus className="w-4 h-4" />, onClick: () => onLoadDialog?.() }
        ]
      default:
        return []
    }
  }

  return (
    <div className="w-64 flex flex-col" style={{ background: 'var(--bg-secondary)', borderRight: '1px solid var(--border-primary)' }}>
      <div className="panel-header">
        <span>Model Explorer</span>
        <Settings className="w-4 h-4" style={{ color: 'var(--text-tertiary)' }} />
      </div>
      <div className="flex-1 overflow-auto p-2 text-sm">
        <TreeNode 
          id="model" 
          label="Model" 
          icon={<Box className="w-4 h-4" />} 
          expanded={expandedNodes.has('model')} 
          onToggle={() => toggleNode('model')}
        >
          <TreeNode 
            id="geometry" 
            label="Geometry" 
            icon={<Grid className="w-4 h-4" />} 
            expanded={expandedNodes.has('geometry')} 
            onToggle={() => toggleNode('geometry')}
          >
            <TreeLeaf 
              label={`Nodes (${nodes.length})`} 
              onClick={() => setSelectedItem({ type: 'nodes', data: nodes })}
              onContextMenu={(e) => handleContextMenu(e, 'nodes')}
            />
            <TreeLeaf 
              label={`Elements (${elements.length})`}
              onClick={() => setSelectedItem({ type: 'elements', data: elements })}
              onContextMenu={(e) => handleContextMenu(e, 'elements')}
            />
          </TreeNode>
          <TreeNode 
            id="properties" 
            label="Properties" 
            icon={<Layers className="w-4 h-4" />} 
            expanded={expandedNodes.has('properties')} 
            onToggle={() => toggleNode('properties')}
          >
            <TreeLeaf 
              label={`Materials (${materials.length})`}
              onClick={() => setSelectedItem({ type: 'materials', data: materials })}
              onContextMenu={(e) => handleContextMenu(e, 'materials')}
            />
            <TreeLeaf 
              label="Sections"
              onContextMenu={(e) => handleContextMenu(e, 'sections')}
            />
            <TreeLeaf 
              label="Load Patterns"
              onContextMenu={(e) => handleContextMenu(e, 'loads')}
            />
          </TreeNode>
          <TreeNode id="analysis" label="Analysis" icon={<Zap className="w-4 h-4" />}>
            <TreeLeaf label="Static" />
            <TreeLeaf label="Modal" />
            <TreeLeaf label="Pushover" />
          </TreeNode>
          <TreeNode id="design" label="Design" icon={<Building className="w-4 h-4" />}>
            <TreeLeaf label="Concrete" />
            <TreeLeaf label="Steel" />
            <TreeLeaf label="Foundation" />
          </TreeNode>
        </TreeNode>
      </div>
      
      {contextMenu && (
        <ContextMenu
          x={contextMenu.x}
          y={contextMenu.y}
          items={getContextMenuItems()}
          onClose={() => setContextMenu(null)}
        />
      )}
    </div>
  )
}
