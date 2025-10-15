import React, { useState, useEffect } from 'react'
import { useRouter } from 'next/router'
import { useAuth } from '@/contexts/AuthContext'
import { useModel } from '@/contexts/ModelContext'
import {
  Save, FolderOpen, Play, Settings, Grid, Eye, Box, Move,
  ZoomIn, ZoomOut, RotateCcw, Copy, Trash2, Plus, Minus,
  ChevronRight, ChevronDown, Layers, Zap, Building, FileText,
  Activity, Maximize2, X, Table
} from 'lucide-react'
import MenuButton from '@/components/ui/MenuButton'
import NodeDialog from '@/components/dialogs/NodeDialog'
import ElementDialog from '@/components/dialogs/ElementDialog'
import MaterialDialog from '@/components/dialogs/MaterialDialog'
import LoadDialog from '@/components/dialogs/LoadDialog'
import AnalysisDialog from '@/components/dialogs/AnalysisDialog'
import NewProjectDialog from '@/components/dialogs/NewProjectDialog'
import DetailingDialog from '@/components/dialogs/DetailingDialog'
import AIAssistantDialog from '@/components/dialogs/AIAssistantDialog'
import ReportDialog from '@/components/dialogs/ReportDialog'
import AdvancedAnalysisDialog from '@/components/dialogs/AdvancedAnalysisDialog'
import SpecializedDesignDialog from '@/components/dialogs/SpecializedDesignDialog'
import VersionDialog from '@/components/dialogs/VersionDialog'
import CollaborationDialog from '@/components/dialogs/CollaborationDialog'
import BIMDialog from '@/components/dialogs/BIMDialog'
import NodesTable from '@/components/tables/NodesTable'
import ElementsTable from '@/components/tables/ElementsTable'
import ResultsTable from '@/components/tables/ResultsTable'
import Viewport3D from '@/components/viewport/Viewport3D'

export default function Workspace() {
  const router = useRouter()
  const { user, isAuthenticated, loading: authLoading, logout } = useAuth()
  const { nodes, elements, materials, selectedItems } = useModel()
  
  const [expandedNodes, setExpandedNodes] = useState(new Set(['model', 'geometry', 'properties']))
  const [activeViewport, setActiveViewport] = useState('3d')
  const [activePanel, setActivePanel] = useState<'properties' | 'tables' | 'results'>('properties')
  const [activeTable, setActiveTable] = useState<'nodes' | 'elements'>('nodes')
  const [analysisResults, setAnalysisResults] = useState<any>(null)
  
  // Dialog states
  const [showNodeDialog, setShowNodeDialog] = useState(false)
  const [showElementDialog, setShowElementDialog] = useState(false)
  const [showMaterialDialog, setShowMaterialDialog] = useState(false)
  const [showLoadDialog, setShowLoadDialog] = useState(false)
  const [showAnalysisDialog, setShowAnalysisDialog] = useState(false)
  const [showNewProjectDialog, setShowNewProjectDialog] = useState(false)
  const [showDetailingDialog, setShowDetailingDialog] = useState(false)
  const [showAIDialog, setShowAIDialog] = useState(false)
  const [showReportDialog, setShowReportDialog] = useState(false)
  const [showAdvancedAnalysisDialog, setShowAdvancedAnalysisDialog] = useState(false)
  const [showSpecializedDesignDialog, setShowSpecializedDesignDialog] = useState(false)
  const [showVersionDialog, setShowVersionDialog] = useState(false)
  const [showCollaborationDialog, setShowCollaborationDialog] = useState(false)
  const [showBIMDialog, setShowBIMDialog] = useState(false)

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login')
    }
  }, [isAuthenticated, authLoading, router])

  const toggleNode = (id: string) => {
    const newExpanded = new Set(expandedNodes)
    newExpanded.has(id) ? newExpanded.delete(id) : newExpanded.add(id)
    setExpandedNodes(newExpanded)
  }

  if (authLoading) return <div className="h-screen flex items-center justify-center" style={{ background: 'var(--bg-primary)' }}>
    <div className="text-center">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 mx-auto mb-4" style={{ borderColor: 'var(--accent-blue)' }}></div>
      <p style={{ color: 'var(--text-secondary)' }}>Loading...</p>
    </div>
  </div>

  if (!isAuthenticated) return null

  const handleRunAnalysis = (config: any) => {
    console.log('Analysis completed with config:', config)
    if (config.results) {
      setAnalysisResults(config.results)
    }
    setActivePanel('results')
  }

  const handleCreateProject = async (project: any) => {
    try {
      // Call backend API to create project
      // const response = await projectAPI.create(project)
      console.log('Creating project:', project)
    } catch (error) {
      console.error('Failed to create project:', error)
    }
  }

  return (
    <div className="h-screen flex flex-col" style={{ background: 'var(--bg-primary)', color: 'var(--text-primary)' }}>
      {/* Menu Bar */}
      <div style={{ background: 'var(--bg-secondary)', borderBottom: '1px solid var(--border-primary)' }} className="px-2 py-1 flex items-center justify-between text-xs">
        <div className="flex items-center space-x-4">
          <div className="font-bold text-sm" style={{ color: 'var(--accent-blue)' }}>StruMind Pro</div>
          <MenuButton label="File" items={[
            { label: 'New Project', onClick: () => setShowNewProjectDialog(true) },
            { label: 'Open', onClick: () => setShowNewProjectDialog(true) },
            { label: 'Save' },
            { label: 'Import BIM', onClick: () => setShowBIMDialog(true) },
            { label: 'Export BIM', onClick: () => setShowBIMDialog(true) }
          ]} />
          <MenuButton label="Edit" items={[
            { label: 'Copy' },
            { label: 'Paste' },
            { label: 'Delete' }
          ]} />
          <MenuButton label="Define" items={[
            { label: 'Materials', onClick: () => setShowMaterialDialog(true) },
            { label: 'Sections' },
            { label: 'Load Patterns', onClick: () => setShowLoadDialog(true) }
          ]} />
          <MenuButton label="Analyze" items={[
            { label: 'Run Analysis', onClick: () => setShowAnalysisDialog(true) },
            { label: 'Advanced Analysis', onClick: () => setShowAdvancedAnalysisDialog(true) }
          ]} />
          <MenuButton label="Design" items={[
            { label: 'Concrete Design' },
            { label: 'Steel Design' },
            { label: 'Specialized Design', onClick: () => setShowSpecializedDesignDialog(true) },
            { label: 'Detailing', onClick: () => setShowDetailingDialog(true) }
          ]} />
          <MenuButton label="AI" items={[
            { label: 'AI Assistant', onClick: () => setShowAIDialog(true) },
            { label: 'Auto Model' },
            { label: 'Optimize' }
          ]} />
          <MenuButton label="Tools" items={[
            { label: 'Reports', onClick: () => setShowReportDialog(true) },
            { label: 'Version History', onClick: () => setShowVersionDialog(true) },
            { label: 'Collaboration', onClick: () => setShowCollaborationDialog(true) }
          ]} />
          <button className="px-2 py-1 hover:bg-gray-700 rounded">Help</button>
        </div>
        <div className="flex items-center space-x-3">
          <span style={{ color: 'var(--text-tertiary)' }}>{user?.username}</span>
          <button onClick={logout} className="px-2 py-1 hover:bg-gray-700 rounded">Logout</button>
        </div>
      </div>

      {/* Main Toolbar */}
      <div style={{ background: 'var(--bg-secondary)', borderBottom: '1px solid var(--border-primary)' }} className="px-2 py-2 flex items-center space-x-1">
        {[
          { icon: Save, tip: 'Save' },
          { icon: FolderOpen, tip: 'Open', onClick: () => setShowNewProjectDialog(true) },
          null,
          { icon: Copy, tip: 'Copy' },
          { icon: Trash2, tip: 'Delete' },
          null,
          { icon: Box, tip: 'Add Node', onClick: () => setShowNodeDialog(true) },
          { icon: Move, tip: 'Add Element', onClick: () => setShowElementDialog(true) },
          { icon: Layers, tip: 'Materials', onClick: () => setShowMaterialDialog(true) },
          { icon: Zap, tip: 'Loads', onClick: () => setShowLoadDialog(true) },
          { icon: Grid, tip: 'Grid' },
          null,
          { icon: Table, tip: 'Tables', onClick: () => setActivePanel('tables') },
          { icon: FileText, tip: 'Reports', onClick: () => setShowReportDialog(true) },
          null,
          { icon: ZoomIn, tip: 'Zoom In' },
          { icon: ZoomOut, tip: 'Zoom Out' },
          { icon: RotateCcw, tip: 'Reset View' },
          null,
          { icon: Play, tip: 'Run Analysis', highlight: true, onClick: () => setShowAnalysisDialog(true) },
        ].map((item, idx) =>
          item === null ? (
            <div key={idx} className="w-px h-6" style={{ background: 'var(--border-secondary)' }} />
          ) : (
            <button
              key={idx}
              onClick={item.onClick}
              className={`toolbar-button ${item.highlight ? 'active' : ''}`}
              title={item.tip}
            >
              <item.icon className="w-4 h-4" />
            </button>
          )
        )}
      </div>

      {/* Secondary Toolbar */}
      <div style={{ background: 'var(--bg-tertiary)', borderBottom: '1px solid var(--border-primary)' }} className="px-3 py-1 flex items-center space-x-4 text-xs">
        <div className="flex items-center space-x-2">
          <span style={{ color: 'var(--text-tertiary)' }}>View:</span>
          {['3D', 'XY', 'XZ', 'YZ'].map(v => (
            <button
              key={v}
              onClick={() => setActiveViewport(v.toLowerCase())}
              className={`px-3 py-1 rounded ${activeViewport === v.toLowerCase() ? 'bg-blue-600 text-white' : 'hover:bg-gray-700'}`}
            >
              {v}
            </button>
          ))}
        </div>
        <div className="w-px h-4" style={{ background: 'var(--border-secondary)' }} />
        <div className="flex items-center space-x-2">
          <span style={{ color: 'var(--text-tertiary)' }}>Units:</span>
          <select className="bg-gray-700 border border-gray-600 rounded px-2 py-1">
            <option>kN, m, C</option>
            <option>kip, ft, F</option>
          </select>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Panel - Model Explorer */}
        <div className="w-64 flex flex-col" style={{ background: 'var(--bg-secondary)', borderRight: '1px solid var(--border-primary)' }}>
          <div className="panel-header">
            <span>Model Explorer</span>
            <Settings className="w-4 h-4" style={{ color: 'var(--text-tertiary)' }} />
          </div>
          <div className="flex-1 overflow-auto p-2 text-sm">
            <TreeNode id="model" label="Model" icon={<Box className="w-4 h-4" />} expanded={expandedNodes.has('model')} onToggle={() => toggleNode('model')}>
              <TreeNode id="geometry" label="Geometry" icon={<Grid className="w-4 h-4" />} expanded={expandedNodes.has('geometry')} onToggle={() => toggleNode('geometry')}>
                <TreeLeaf label={`Nodes (${nodes.length})`} />
                <TreeLeaf label={`Elements (${elements.length})`} />
              </TreeNode>
              <TreeNode id="properties" label="Properties" icon={<Layers className="w-4 h-4" />} expanded={expandedNodes.has('properties')} onToggle={() => toggleNode('properties')}>
                <TreeLeaf label={`Materials (${materials.length})`} />
                <TreeLeaf label="Sections" />
                <TreeLeaf label="Load Patterns" />
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
        </div>

        {/* Center - Viewport */}
        <div className="flex-1 flex flex-col">
          <div style={{ background: 'var(--bg-secondary)', borderBottom: '1px solid var(--border-primary)' }} className="px-2 py-1 flex items-center space-x-1 text-xs">
            <button 
              onClick={() => setActiveViewport('3d')}
              className={`px-3 py-1 rounded-t ${activeViewport === '3d' ? 'bg-gray-900 text-white border-t-2 border-blue-500' : 'hover:bg-gray-700'}`}
              style={{ color: activeViewport === '3d' ? 'white' : 'var(--text-tertiary)' }}
            >
              3D View
            </button>
            <button 
              onClick={() => setActiveViewport('xy')}
              className={`px-3 py-1 rounded-t ${activeViewport === 'xy' ? 'bg-gray-900 text-white border-t-2 border-blue-500' : 'hover:bg-gray-700'}`}
              style={{ color: activeViewport === 'xy' ? 'white' : 'var(--text-tertiary)' }}
            >
              Plan View
            </button>
          </div>
          <div className="flex-1 relative">
            <Viewport3D activeView={activeViewport} />
          </div>
        </div>

        {/* Right Panel - Properties/Tables/Results */}
        <div className="w-96 flex flex-col" style={{ background: 'var(--bg-secondary)', borderLeft: '1px solid var(--border-primary)' }}>
          {/* Panel Tabs */}
          <div className="flex border-b" style={{ borderColor: 'var(--border-primary)' }}>
            <button
              onClick={() => setActivePanel('properties')}
              className={`flex-1 px-4 py-2 text-sm font-medium transition-colors ${
                activePanel === 'properties' ? 'border-b-2 border-blue-500' : ''
              }`}
              style={{ color: activePanel === 'properties' ? 'var(--accent-blue)' : 'var(--text-secondary)' }}
            >
              Properties
            </button>
            <button
              onClick={() => setActivePanel('tables')}
              className={`flex-1 px-4 py-2 text-sm font-medium transition-colors ${
                activePanel === 'tables' ? 'border-b-2 border-blue-500' : ''
              }`}
              style={{ color: activePanel === 'tables' ? 'var(--accent-blue)' : 'var(--text-secondary)' }}
            >
              Tables
            </button>
            <button
              onClick={() => setActivePanel('results')}
              className={`flex-1 px-4 py-2 text-sm font-medium transition-colors ${
                activePanel === 'results' ? 'border-b-2 border-blue-500' : ''
              }`}
              style={{ color: activePanel === 'results' ? 'var(--accent-blue)' : 'var(--text-secondary)' }}
            >
              Results
            </button>
          </div>

          {/* Panel Content */}
          <div className="flex-1 overflow-hidden flex flex-col">
            {activePanel === 'properties' && (
              <div className="flex-1 overflow-auto p-3 text-sm">
                {selectedItems.size > 0 ? (
                  <div className="space-y-4">
                    <PropertyGroup title="Selection">
                      <PropertyRow label="Count" value={selectedItems.size} />
                    </PropertyGroup>
                  </div>
                ) : (
                  <div className="text-center py-8" style={{ color: 'var(--text-tertiary)' }}>
                    <Activity className="w-12 h-12 mx-auto mb-2 opacity-50" />
                    <p>No selection</p>
                  </div>
                )}
              </div>
            )}

            {activePanel === 'tables' && (
              <div className="flex-1 flex flex-col">
                <div className="flex border-b" style={{ borderColor: 'var(--border-primary)' }}>
                  <button
                    onClick={() => setActiveTable('nodes')}
                    className={`px-4 py-2 text-xs font-medium ${
                      activeTable === 'nodes' ? 'border-b-2 border-blue-500' : ''
                    }`}
                    style={{ color: activeTable === 'nodes' ? 'var(--accent-blue)' : 'var(--text-secondary)' }}
                  >
                    Nodes
                  </button>
                  <button
                    onClick={() => setActiveTable('elements')}
                    className={`px-4 py-2 text-xs font-medium ${
                      activeTable === 'elements' ? 'border-b-2 border-blue-500' : ''
                    }`}
                    style={{ color: activeTable === 'elements' ? 'var(--accent-blue)' : 'var(--text-secondary)' }}
                  >
                    Elements
                  </button>
                </div>
                <div className="flex-1 overflow-hidden">
                  {activeTable === 'nodes' && <NodesTable onEdit={(node) => console.log('Edit node:', node)} />}
                  {activeTable === 'elements' && <ElementsTable onEdit={(elem) => console.log('Edit element:', elem)} />}
                </div>
              </div>
            )}

            {activePanel === 'results' && (
              <div className="flex-1 overflow-hidden">
                <ResultsTable results={analysisResults} />
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Status Bar */}
      <div style={{ background: 'var(--bg-secondary)', borderTop: '1px solid var(--border-primary)' }} className="px-3 py-1 flex items-center justify-between text-xs">
        <div className="flex items-center space-x-4">
          <span className="status-ready">● Ready</span>
          <span style={{ color: 'var(--text-tertiary)' }}>Units: kN, m, C</span>
        </div>
        <div className="flex items-center space-x-4" style={{ color: 'var(--text-tertiary)' }}>
          <span>Nodes: {nodes.length}</span>
          <span>Elements: {elements.length}</span>
          <span>Materials: {materials.length}</span>
        </div>
      </div>

      {/* Dialogs */}
      <NodeDialog isOpen={showNodeDialog} onClose={() => setShowNodeDialog(false)} />
      <ElementDialog isOpen={showElementDialog} onClose={() => setShowElementDialog(false)} />
      <MaterialDialog isOpen={showMaterialDialog} onClose={() => setShowMaterialDialog(false)} />
      <LoadDialog isOpen={showLoadDialog} onClose={() => setShowLoadDialog(false)} />
      <AnalysisDialog isOpen={showAnalysisDialog} onClose={() => setShowAnalysisDialog(false)} onRunAnalysis={handleRunAnalysis} />
      <NewProjectDialog isOpen={showNewProjectDialog} onClose={() => setShowNewProjectDialog(false)} onCreateProject={handleCreateProject} />
      <DetailingDialog isOpen={showDetailingDialog} onClose={() => setShowDetailingDialog(false)} onSubmit={(data) => console.log('Detailing:', data)} />
      <AIAssistantDialog isOpen={showAIDialog} onClose={() => setShowAIDialog(false)} onSubmit={(data) => console.log('AI:', data)} />
      <ReportDialog isOpen={showReportDialog} onClose={() => setShowReportDialog(false)} onGenerate={(data) => console.log('Report:', data)} />
      <AdvancedAnalysisDialog isOpen={showAdvancedAnalysisDialog} onClose={() => setShowAdvancedAnalysisDialog(false)} onRun={(data) => console.log('Advanced Analysis:', data)} />
      <SpecializedDesignDialog isOpen={showSpecializedDesignDialog} onClose={() => setShowSpecializedDesignDialog(false)} onDesign={(data) => console.log('Specialized Design:', data)} />
      <VersionDialog isOpen={showVersionDialog} onClose={() => setShowVersionDialog(false)} onRestore={(id) => console.log('Restore version:', id)} />
      <CollaborationDialog isOpen={showCollaborationDialog} onClose={() => setShowCollaborationDialog(false)} onShare={(data) => console.log('Share:', data)} />
      <BIMDialog isOpen={showBIMDialog} onClose={() => setShowBIMDialog(false)} onAction={(action, data) => console.log('BIM:', action, data)} />
    </div>
  )
}

function TreeNode({ id, label, icon, expanded, onToggle, children }: any) {
  return (
    <div>
      <div className="tree-node flex items-center space-x-1" onClick={onToggle}>
        {onToggle && (expanded ? <ChevronDown className="w-3 h-3" /> : <ChevronRight className="w-3 h-3" />)}
        {icon}
        <span>{label}</span>
      </div>
      {expanded && children && <div className="ml-4 border-l pl-2" style={{ borderColor: 'var(--border-primary)' }}>{children}</div>}
    </div>
  )
}

function TreeLeaf({ label, onClick }: any) {
  return (
    <div className="tree-node flex items-center space-x-1 pl-4" onClick={onClick} style={{ color: 'var(--text-secondary)' }}>
      <div className="w-3 h-3" />
      <span>{label}</span>
    </div>
  )
}

function PropertyGroup({ title, children }: any) {
  return (
    <div>
      <div className="text-xs font-semibold mb-2 uppercase" style={{ color: 'var(--text-tertiary)' }}>{title}</div>
      {children}
    </div>
  )
}

function PropertyRow({ label, value }: any) {
  return (
    <div className="flex justify-between py-1 text-xs">
      <span style={{ color: 'var(--text-secondary)' }}>{label}:</span>
      <span>{value}</span>
    </div>
  )
}
