import React, { useState } from 'react'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { TrendingUp, Activity, Layers, Download, Filter } from 'lucide-react'

interface ResultsVisualizationProps {
  results?: any
}

export default function ResultsVisualization({ results }: ResultsVisualizationProps) {
  const [activeTab, setActiveTab] = useState('diagrams')
  const [selectedElement, setSelectedElement] = useState('E1')

  // Sample data for moment diagram
  const momentData = [
    { station: 0, moment: 0 },
    { station: 0.25, moment: 45 },
    { station: 0.5, moment: 75 },
    { station: 0.75, moment: 45 },
    { station: 1.0, moment: 0 },
  ]

  // Sample data for shear diagram
  const shearData = [
    { station: 0, shear: 50 },
    { station: 0.5, shear: 50 },
    { station: 0.5, shear: -50 },
    { station: 1.0, shear: -50 },
  ]

  // Sample deflection data
  const deflectionData = [
    { station: 0, deflection: 0 },
    { station: 0.25, deflection: -8 },
    { station: 0.5, deflection: -12 },
    { station: 0.75, deflection: -8 },
    { station: 1.0, deflection: 0 },
  ]

  const tabs = [
    { id: 'diagrams', label: 'Force Diagrams', icon: Activity },
    { id: 'deflection', label: 'Deflection', icon: TrendingUp },
    { id: 'stresses', label: 'Stresses', icon: Layers },
  ]

  return (
    <div className="h-full bg-slate-50">
      {/* Header */}
      <div className="bg-white border-b border-slate-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-slate-900">Analysis Results</h2>
            <p className="text-sm text-slate-600 mt-1">Visualize and analyze structural behavior</p>
          </div>
          <div className="flex items-center space-x-2">
            <button className="px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100 rounded-lg transition-colors flex items-center space-x-2">
              <Filter className="w-4 h-4" />
              <span>Filter</span>
            </button>
            <button className="px-4 py-2 bg-blue-600 text-white text-sm font-medium hover:bg-blue-700 rounded-lg transition-colors flex items-center space-x-2">
              <Download className="w-4 h-4" />
              <span>Export</span>
            </button>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex space-x-1 mt-4">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-medium transition-all ${
                activeTab === tab.id
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              <tab.icon className="w-4 h-4" />
              <span>{tab.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div className="p-6">
        {activeTab === 'diagrams' && (
          <div className="space-y-6">
            {/* Element Selector */}
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-4">
              <label className="block text-sm font-medium text-slate-700 mb-2">
                Select Element
              </label>
              <select
                value={selectedElement}
                onChange={(e) => setSelectedElement(e.target.value)}
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="E1">Element E1 - Beam (6m)</option>
                <option value="E2">Element E2 - Beam (8m)</option>
                <option value="E3">Element E3 - Column (3m)</option>
              </select>
            </div>

            {/* Moment Diagram */}
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-slate-900">Bending Moment Diagram</h3>
                <div className="flex items-center space-x-4 text-sm">
                  <span className="text-slate-600">Max: <span className="font-semibold text-blue-600">75.0 kNm</span></span>
                  <span className="text-slate-600">Min: <span className="font-semibold text-red-600">0.0 kNm</span></span>
                </div>
              </div>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={momentData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                  <XAxis 
                    dataKey="station" 
                    label={{ value: 'Position along span', position: 'insideBottom', offset: -5 }}
                    stroke="#64748b"
                  />
                  <YAxis 
                    label={{ value: 'Moment (kNm)', angle: -90, position: 'insideLeft' }}
                    stroke="#64748b"
                  />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#fff', border: '1px solid #e2e8f0', borderRadius: '8px' }}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="moment" 
                    stroke="#3b82f6" 
                    strokeWidth={3}
                    dot={{ fill: '#3b82f6', r: 4 }}
                    activeDot={{ r: 6 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Shear Force Diagram */}
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-slate-900">Shear Force Diagram</h3>
                <div className="flex items-center space-x-4 text-sm">
                  <span className="text-slate-600">Max: <span className="font-semibold text-green-600">50.0 kN</span></span>
                  <span className="text-slate-600">Min: <span className="font-semibold text-red-600">-50.0 kN</span></span>
                </div>
              </div>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={shearData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                  <XAxis 
                    dataKey="station" 
                    label={{ value: 'Position along span', position: 'insideBottom', offset: -5 }}
                    stroke="#64748b"
                  />
                  <YAxis 
                    label={{ value: 'Shear Force (kN)', angle: -90, position: 'insideLeft' }}
                    stroke="#64748b"
                  />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#fff', border: '1px solid #e2e8f0', borderRadius: '8px' }}
                  />
                  <Line 
                    type="stepAfter" 
                    dataKey="shear" 
                    stroke="#10b981" 
                    strokeWidth={3}
                    dot={{ fill: '#10b981', r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        {activeTab === 'deflection' && (
          <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-slate-900">Deflection Curve</h3>
              <div className="flex items-center space-x-4 text-sm">
                <span className="text-slate-600">Max Deflection: <span className="font-semibold text-purple-600">12.0 mm</span></span>
                <span className="text-slate-600">Limit (L/360): <span className="font-semibold text-slate-900">16.7 mm</span></span>
                <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium">PASS</span>
              </div>
            </div>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={deflectionData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis 
                  dataKey="station" 
                  label={{ value: 'Position along span', position: 'insideBottom', offset: -5 }}
                  stroke="#64748b"
                />
                <YAxis 
                  label={{ value: 'Deflection (mm)', angle: -90, position: 'insideLeft' }}
                  stroke="#64748b"
                />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#fff', border: '1px solid #e2e8f0', borderRadius: '8px' }}
                />
                <Line 
                  type="monotone" 
                  dataKey="deflection" 
                  stroke="#8b5cf6" 
                  strokeWidth={3}
                  dot={{ fill: '#8b5cf6', r: 4 }}
                  activeDot={{ r: 6 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}

        {activeTab === 'stresses' && (
          <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
            <h3 className="text-lg font-semibold text-slate-900 mb-4">Stress Distribution</h3>
            <div className="grid grid-cols-2 gap-6">
              <div className="space-y-4">
                <div className="p-4 bg-blue-50 rounded-lg">
                  <div className="text-sm text-slate-600 mb-1">Maximum Tensile Stress</div>
                  <div className="text-2xl font-bold text-blue-600">185.5 MPa</div>
                  <div className="text-xs text-slate-500 mt-1">Location: Bottom fiber at mid-span</div>
                </div>
                <div className="p-4 bg-red-50 rounded-lg">
                  <div className="text-sm text-slate-600 mb-1">Maximum Compressive Stress</div>
                  <div className="text-2xl font-bold text-red-600">-165.2 MPa</div>
                  <div className="text-xs text-slate-500 mt-1">Location: Top fiber at mid-span</div>
                </div>
              </div>
              <div className="space-y-4">
                <div className="p-4 bg-green-50 rounded-lg">
                  <div className="text-sm text-slate-600 mb-1">Allowable Stress</div>
                  <div className="text-2xl font-bold text-green-600">250.0 MPa</div>
                  <div className="text-xs text-slate-500 mt-1">Per IS 456:2000</div>
                </div>
                <div className="p-4 bg-purple-50 rounded-lg">
                  <div className="text-sm text-slate-600 mb-1">Utilization Ratio</div>
                  <div className="text-2xl font-bold text-purple-600">74.2%</div>
                  <div className="text-xs text-slate-500 mt-1">Status: Safe</div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
