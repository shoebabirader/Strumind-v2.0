import { useState } from 'react'
import dynamic from 'next/dynamic'
import ProfessionalLayout from '@/components/ProfessionalLayout'
import IndustryDashboard from '@/components/IndustryDashboard'
import AdvancedDesignPanel from '@/components/AdvancedDesignPanel'
import ResultsVisualization from '@/components/ResultsVisualization'
import '../styles/professional.css'

const Enhanced3DViewer = dynamic(() => import('@/components/Enhanced3DViewer'), { ssr: false })

export default function ProfessionalView() {
  const [activeSection, setActiveSection] = useState<'dashboard' | 'model' | 'analysis' | 'design' | 'results' | 'settings'>('dashboard')

  const handleNavigate = (section: string) => {
    setActiveSection(section as any)
  }

  const renderContent = () => {
    switch (activeSection) {
      case 'dashboard':
        return <IndustryDashboard onNavigate={handleNavigate} />
      
      case 'model':
        return (
          <div className="h-full">
            <Enhanced3DViewer showGrid={true} showAxes={true} />
          </div>
        )
      
      case 'analysis':
        return (
          <div className="h-full bg-slate-50 p-6">
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
              <h2 className="text-2xl font-bold text-slate-900 mb-4">Analysis Module</h2>
              <p className="text-slate-600">Run static, modal, response spectrum, and advanced analyses</p>
            </div>
          </div>
        )
      
      case 'design':
        return <AdvancedDesignPanel />
      
      case 'results':
        return <ResultsVisualization />
      
      case 'settings':
        return (
          <div className="h-full bg-slate-50 p-6">
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
              <h2 className="text-2xl font-bold text-slate-900 mb-4">Settings</h2>
              <p className="text-slate-600">Configure design codes, units, and preferences</p>
            </div>
          </div>
        )
      
      default:
        return <IndustryDashboard onNavigate={handleNavigate} />
    }
  }

  return (
    <div className="h-screen overflow-hidden">
      {renderContent()}
    </div>
  )
}
