import { useState } from 'react'
import dynamic from 'next/dynamic'
import AIAssistant from '@/components/AIAssistant'
import ModelBuilder from '@/components/ModelBuilder'
import LoadsPanel from '@/components/LoadsPanel'
import SeismicAnalysis from '@/components/SeismicAnalysis'

const ModelViewer = dynamic(() => import('@/components/ModelViewer'), { ssr: false })

export default function Home() {
  const [activeTab, setActiveTab] = useState('model')
  const [showAI, setShowAI] = useState(false)

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-blue-600 text-white p-4">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold">StruMind</h1>
            <p className="text-sm">AI-Powered Structural Engineering Platform</p>
          </div>
          <button
            onClick={() => setShowAI(!showAI)}
            className="bg-blue-700 px-4 py-2 rounded"
          >
            {showAI ? 'Hide' : 'Show'} AI Assistant
          </button>
        </div>
      </nav>

      <div className="container mx-auto p-6">
        <div className="flex gap-4 mb-6">
          <button
            onClick={() => setActiveTab('model')}
            className={`px-4 py-2 rounded ${activeTab === 'model' ? 'bg-blue-600 text-white' : 'bg-white'}`}
          >
            Model
          </button>
          <button
            onClick={() => setActiveTab('analysis')}
            className={`px-4 py-2 rounded ${activeTab === 'analysis' ? 'bg-blue-600 text-white' : 'bg-white'}`}
          >
            Analysis
          </button>
          <button
            onClick={() => setActiveTab('design')}
            className={`px-4 py-2 rounded ${activeTab === 'design' ? 'bg-blue-600 text-white' : 'bg-white'}`}
          >
            Design
          </button>
          <button
            onClick={() => setActiveTab('detailing')}
            className={`px-4 py-2 rounded ${activeTab === 'detailing' ? 'bg-blue-600 text-white' : 'bg-white'}`}
          >
            Detailing
          </button>
          <button
            onClick={() => setActiveTab('loads')}
            className={`px-4 py-2 rounded ${activeTab === 'loads' ? 'bg-blue-600 text-white' : 'bg-white'}`}
          >
            Loads
          </button>
          <button
            onClick={() => setActiveTab('seismic')}
            className={`px-4 py-2 rounded ${activeTab === 'seismic' ? 'bg-blue-600 text-white' : 'bg-white'}`}
          >
            Seismic
          </button>
          <button
            onClick={() => setActiveTab('bim')}
            className={`px-4 py-2 rounded ${activeTab === 'bim' ? 'bg-blue-600 text-white' : 'bg-white'}`}
          >
            BIM
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className={showAI ? 'lg:col-span-2' : 'lg:col-span-3'}>
            <div className="bg-white rounded-lg shadow p-6">
              {activeTab === 'model' && <ModelTab />}
              {activeTab === 'loads' && <LoadsPanel />}
              {activeTab === 'analysis' && <AnalysisTab />}
              {activeTab === 'seismic' && <SeismicAnalysis />}
              {activeTab === 'design' && <DesignTab />}
              {activeTab === 'detailing' && <DetailingTab />}
              {activeTab === 'bim' && <BIMTab />}
            </div>
          </div>
          {showAI && (
            <div className="lg:col-span-1">
              <AIAssistant />
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

function ModelTab() {
  const [viewMode, setViewMode] = useState<'builder' | 'viewer'>('builder')

  return (
    <div className="h-full flex flex-col">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold">Model Creation</h2>
        <div className="flex gap-2">
          <button
            onClick={() => setViewMode('builder')}
            className={`px-4 py-2 rounded ${viewMode === 'builder' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
          >
            Builder
          </button>
          <button
            onClick={() => setViewMode('viewer')}
            className={`px-4 py-2 rounded ${viewMode === 'viewer' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
          >
            3D Viewer
          </button>
        </div>
      </div>

      <div className="flex-1">
        {viewMode === 'builder' ? (
          <ModelBuilder />
        ) : (
          <div className="h-96">
            <ModelViewer />
          </div>
        )}
      </div>
    </div>
  )
}

function AnalysisTab() {
  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Structural Analysis</h2>
      <div className="space-y-4">
        <select className="w-full p-2 border rounded">
          <option>Static Analysis</option>
          <option>Modal Analysis</option>
          <option>Pushover Analysis</option>
          <option>Time-History Analysis</option>
        </select>
        <button className="bg-blue-600 text-white px-6 py-2 rounded">Run Analysis</button>
      </div>
    </div>
  )
}

function DesignTab() {
  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Design</h2>
      <div className="space-y-4">
        <select className="w-full p-2 border rounded">
          <option>IS 456 (RC)</option>
          <option>ACI 318 (RC)</option>
          <option>IS 800 (Steel)</option>
          <option>AISC (Steel)</option>
        </select>
        <button className="bg-blue-600 text-white px-6 py-2 rounded">Generate Design</button>
        <button className="bg-green-600 text-white px-6 py-2 rounded">AI Optimize</button>
      </div>
    </div>
  )
}

function DetailingTab() {
  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Detailing & BBS</h2>
      <div className="space-y-4">
        <button className="bg-blue-600 text-white px-6 py-2 rounded">Generate Drawings</button>
        <button className="bg-blue-600 text-white px-6 py-2 rounded">Export BBS</button>
        <button className="bg-blue-600 text-white px-6 py-2 rounded">Generate BOQ</button>
      </div>
    </div>
  )
}

function BIMTab() {
  return (
    <div>
      <h2 className="text-xl font-bold mb-4">BIM Integration</h2>
      <div className="space-y-4">
        <button className="bg-blue-600 text-white px-6 py-2 rounded">Import IFC</button>
        <button className="bg-blue-600 text-white px-6 py-2 rounded">Export to IFC</button>
        <button className="bg-blue-600 text-white px-6 py-2 rounded">Sync with Revit</button>
      </div>
    </div>
  )
}
