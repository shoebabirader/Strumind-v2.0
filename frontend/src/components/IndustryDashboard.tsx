import React, { useState } from 'react'
import { 
  LayoutDashboard, 
  Box, 
  Layers, 
  Activity, 
  FileText, 
  Settings,
  Play,
  Save,
  Download,
  Upload,
  Zap,
  TrendingUp,
  AlertCircle,
  CheckCircle,
  Clock
} from 'lucide-react'

interface DashboardProps {
  onNavigate: (section: string) => void
}

export default function IndustryDashboard({ onNavigate }: DashboardProps) {
  const [activeProject, setActiveProject] = useState('Building Design - Tower A')

  const quickStats = [
    { label: 'Total Nodes', value: '1,247', icon: Box, color: 'blue' },
    { label: 'Elements', value: '2,891', icon: Layers, color: 'green' },
    { label: 'Load Cases', value: '12', icon: Activity, color: 'purple' },
    { label: 'Analyses Run', value: '8', icon: TrendingUp, color: 'orange' },
  ]

  const recentAnalyses = [
    { name: 'Static Analysis', status: 'completed', time: '2 min ago', result: 'Pass' },
    { name: 'Modal Analysis', status: 'completed', time: '5 min ago', result: 'Pass' },
    { name: 'Response Spectrum', status: 'running', time: 'In progress', result: '-' },
    { name: 'P-Delta Analysis', status: 'pending', time: 'Queued', result: '-' },
  ]

  const designModules = [
    { name: 'RC Beam Design', icon: Box, count: 45, status: 'OK' },
    { name: 'RC Column Design', icon: Box, count: 32, status: 'OK' },
    { name: 'Slab Design', icon: Layers, count: 8, status: 'Review' },
    { name: 'Foundation Design', icon: Box, count: 12, status: 'OK' },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Top Navigation Bar */}
      <nav className="bg-white border-b border-slate-200 shadow-sm">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <Zap className="w-8 h-8 text-blue-600" />
                <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  StruMind
                </span>
              </div>
              <div className="h-8 w-px bg-slate-300" />
              <span className="text-sm text-slate-600 font-medium">{activeProject}</span>
            </div>
            
            <div className="flex items-center space-x-2">
              <button className="px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100 rounded-lg transition-colors">
                <Upload className="w-4 h-4 inline mr-2" />
                Import
              </button>
              <button className="px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100 rounded-lg transition-colors">
                <Download className="w-4 h-4 inline mr-2" />
                Export
              </button>
              <button className="px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100 rounded-lg transition-colors">
                <Save className="w-4 h-4 inline mr-2" />
                Save
              </button>
              <button className="px-4 py-2 bg-blue-600 text-white text-sm font-medium hover:bg-blue-700 rounded-lg transition-colors shadow-sm">
                <Play className="w-4 h-4 inline mr-2" />
                Run Analysis
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="flex h-[calc(100vh-73px)]">
        {/* Sidebar */}
        <aside className="w-64 bg-white border-r border-slate-200 shadow-sm">
          <div className="p-4 space-y-1">
            {[
              { icon: LayoutDashboard, label: 'Dashboard', id: 'dashboard' },
              { icon: Box, label: 'Model Builder', id: 'model' },
              { icon: Activity, label: 'Analysis', id: 'analysis' },
              { icon: Layers, label: 'Design', id: 'design' },
              { icon: FileText, label: 'Results', id: 'results' },
              { icon: Settings, label: 'Settings', id: 'settings' },
            ].map((item) => (
              <button
                key={item.id}
                onClick={() => onNavigate(item.id)}
                className="w-full flex items-center space-x-3 px-4 py-3 text-slate-700 hover:bg-blue-50 hover:text-blue-600 rounded-lg transition-all group"
              >
                <item.icon className="w-5 h-5 group-hover:scale-110 transition-transform" />
                <span className="font-medium">{item.label}</span>
              </button>
            ))}
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 overflow-auto p-6">
          {/* Quick Stats */}
          <div className="grid grid-cols-4 gap-6 mb-6">
            {quickStats.map((stat, idx) => (
              <div key={idx} className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 hover:shadow-md transition-shadow">
                <div className="flex items-center justify-between mb-4">
                  <div className={`p-3 rounded-lg bg-${stat.color}-50`}>
                    <stat.icon className={`w-6 h-6 text-${stat.color}-600`} />
                  </div>
                </div>
                <div className="text-3xl font-bold text-slate-900 mb-1">{stat.value}</div>
                <div className="text-sm text-slate-600">{stat.label}</div>
              </div>
            ))}
          </div>

          <div className="grid grid-cols-2 gap-6">
            {/* Recent Analyses */}
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
              <h3 className="text-lg font-semibold text-slate-900 mb-4">Recent Analyses</h3>
              <div className="space-y-3">
                {recentAnalyses.map((analysis, idx) => (
                  <div key={idx} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg hover:bg-slate-100 transition-colors">
                    <div className="flex items-center space-x-3">
                      {analysis.status === 'completed' && <CheckCircle className="w-5 h-5 text-green-600" />}
                      {analysis.status === 'running' && <Clock className="w-5 h-5 text-blue-600 animate-spin" />}
                      {analysis.status === 'pending' && <AlertCircle className="w-5 h-5 text-slate-400" />}
                      <div>
                        <div className="font-medium text-slate-900">{analysis.name}</div>
                        <div className="text-xs text-slate-500">{analysis.time}</div>
                      </div>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                      analysis.result === 'Pass' ? 'bg-green-100 text-green-700' : 'bg-slate-100 text-slate-600'
                    }`}>
                      {analysis.result}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Design Modules */}
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
              <h3 className="text-lg font-semibold text-slate-900 mb-4">Design Modules</h3>
              <div className="space-y-3">
                {designModules.map((module, idx) => (
                  <div key={idx} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg hover:bg-slate-100 transition-colors cursor-pointer">
                    <div className="flex items-center space-x-3">
                      <module.icon className="w-5 h-5 text-slate-600" />
                      <div>
                        <div className="font-medium text-slate-900">{module.name}</div>
                        <div className="text-xs text-slate-500">{module.count} members</div>
                      </div>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                      module.status === 'OK' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'
                    }`}>
                      {module.status}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="mt-6 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl shadow-lg p-6 text-white">
            <h3 className="text-xl font-semibold mb-4">Quick Actions</h3>
            <div className="grid grid-cols-4 gap-4">
              {[
                { label: 'New Model', icon: Box },
                { label: 'Run Analysis', icon: Play },
                { label: 'View Results', icon: FileText },
                { label: 'Generate Report', icon: Download },
              ].map((action, idx) => (
                <button
                  key={idx}
                  className="bg-white/10 hover:bg-white/20 backdrop-blur-sm rounded-lg p-4 transition-all hover:scale-105"
                >
                  <action.icon className="w-6 h-6 mx-auto mb-2" />
                  <div className="text-sm font-medium">{action.label}</div>
                </button>
              ))}
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}
