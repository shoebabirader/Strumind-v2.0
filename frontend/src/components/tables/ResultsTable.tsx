import React, { useState } from 'react'
import { BarChart3, TrendingUp, Activity } from 'lucide-react'

interface ResultsTableProps {
  results?: any
}

export default function ResultsTable({ results }: ResultsTableProps) {
  const [activeTab, setActiveTab] = useState('displacements')

  const mockDisplacements = [
    { node: 'N1', ux: 0.0, uy: -2.5, uz: 0.0, rx: 0.0, ry: 0.0, rz: 0.001 },
    { node: 'N2', ux: 0.0, uy: -3.2, uz: 0.0, rx: 0.0, ry: 0.0, rz: 0.002 },
    { node: 'N3', ux: 0.0, uy: -2.8, uz: 0.0, rx: 0.0, ry: 0.0, rz: 0.001 },
  ]

  const mockForces = [
    { element: 'E1', fx: 125.5, fy: -45.2, fz: 0.0, mx: 15.3, my: 0.0, mz: 22.1 },
    { element: 'E2', fx: 98.3, fy: -52.1, fz: 0.0, mx: 18.7, my: 0.0, mz: 19.5 },
    { element: 'E3', fx: 110.2, fy: -48.5, fz: 0.0, mx: 16.2, my: 0.0, mz: 20.8 },
  ]

  const mockStresses = [
    { element: 'E1', axial: 125.5, shearY: 15.2, shearZ: 0.0, torsion: 5.3, bendingY: 45.2, bendingZ: 32.1 },
    { element: 'E2', axial: 98.3, shearY: 18.1, shearZ: 0.0, torsion: 4.7, bendingY: 52.1, bendingZ: 28.5 },
    { element: 'E3', axial: 110.2, shearY: 16.5, shearZ: 0.0, torsion: 5.0, bendingY: 48.5, bendingZ: 30.2 },
  ]

  return (
    <div className="panel flex-1 flex flex-col">
      <div className="panel-header">
        <span><BarChart3 className="w-4 h-4 inline mr-2" />Analysis Results</span>
      </div>

      {/* Tabs */}
      <div className="flex border-b" style={{ borderColor: 'var(--border-primary)' }}>
        <button
          onClick={() => setActiveTab('displacements')}
          className={`px-4 py-2 text-sm font-medium transition-colors ${
            activeTab === 'displacements' ? 'border-b-2 border-blue-500' : ''
          }`}
          style={{ color: activeTab === 'displacements' ? 'var(--accent-blue)' : 'var(--text-secondary)' }}
        >
          <Activity className="w-4 h-4 inline mr-1" />
          Displacements
        </button>
        <button
          onClick={() => setActiveTab('forces')}
          className={`px-4 py-2 text-sm font-medium transition-colors ${
            activeTab === 'forces' ? 'border-b-2 border-blue-500' : ''
          }`}
          style={{ color: activeTab === 'forces' ? 'var(--accent-blue)' : 'var(--text-secondary)' }}
        >
          <TrendingUp className="w-4 h-4 inline mr-1" />
          Forces
        </button>
        <button
          onClick={() => setActiveTab('stresses')}
          className={`px-4 py-2 text-sm font-medium transition-colors ${
            activeTab === 'stresses' ? 'border-b-2 border-blue-500' : ''
          }`}
          style={{ color: activeTab === 'stresses' ? 'var(--accent-blue)' : 'var(--text-secondary)' }}
        >
          <BarChart3 className="w-4 h-4 inline mr-1" />
          Stresses
        </button>
      </div>
      
      <div className="flex-1 overflow-auto">
        {activeTab === 'displacements' && (
          <table className="w-full">
            <thead style={{ background: 'var(--bg-tertiary)', position: 'sticky', top: 0 }}>
              <tr>
                <th className="px-4 py-2 text-left text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>Node</th>
                <th className="px-4 py-2 text-right text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>UX (mm)</th>
                <th className="px-4 py-2 text-right text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>UY (mm)</th>
                <th className="px-4 py-2 text-right text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>UZ (mm)</th>
                <th className="px-4 py-2 text-right text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>RX (rad)</th>
                <th className="px-4 py-2 text-right text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>RY (rad)</th>
                <th className="px-4 py-2 text-right text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>RZ (rad)</th>
              </tr>
            </thead>
            <tbody>
              {mockDisplacements.map((disp, idx) => (
                <tr 
                  key={disp.node}
                  className="border-t hover:bg-opacity-50 transition-colors"
                  style={{ 
                    borderColor: 'var(--border-primary)',
                    background: idx % 2 === 0 ? 'transparent' : 'var(--bg-tertiary)'
                  }}
                >
                  <td className="px-4 py-2 text-sm font-medium">{disp.node}</td>
                  <td className="px-4 py-2 text-sm text-right">{disp.ux.toFixed(3)}</td>
                  <td className="px-4 py-2 text-sm text-right">{disp.uy.toFixed(3)}</td>
                  <td className="px-4 py-2 text-sm text-right">{disp.uz.toFixed(3)}</td>
                  <td className="px-4 py-2 text-sm text-right">{disp.rx.toFixed(6)}</td>
                  <td className="px-4 py-2 text-sm text-right">{disp.ry.toFixed(6)}</td>
                  <td className="px-4 py-2 text-sm text-right">{disp.rz.toFixed(6)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

        {activeTab === 'forces' && (
          <table className="w-full">
            <thead style={{ background: 'var(--bg-tertiary)', position: 'sticky', top: 0 }}>
              <tr>
                <th className="px-4 py-2 text-left text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>Element</th>
                <th className="px-4 py-2 text-right text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>FX (kN)</th>
                <th className="px-4 py-2 text-right text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>FY (kN)</th>
                <th className="px-4 py-2 text-right text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>FZ (kN)</th>
                <th className="px-4 py-2 text-right text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>MX (kN·m)</th>
                <th className="px-4 py-2 text-right text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>MY (kN·m)</th>
                <th className="px-4 py-2 text-right text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>MZ (kN·m)</th>
              </tr>
            </thead>
            <tbody>
              {mockForces.map((force, idx) => (
                <tr 
                  key={force.element}
                  className="border-t hover:bg-opacity-50 transition-colors"
                  style={{ 
                    borderColor: 'var(--border-primary)',
                    background: idx % 2 === 0 ? 'transparent' : 'var(--bg-tertiary)'
                  }}
                >
                  <td className="px-4 py-2 text-sm font-medium">{force.element}</td>
                  <td className="px-4 py-2 text-sm text-right">{force.fx.toFixed(2)}</td>
                  <td className="px-4 py-2 text-sm text-right">{force.fy.toFixed(2)}</td>
                  <td className="px-4 py-2 text-sm text-right">{force.fz.toFixed(2)}</td>
                  <td className="px-4 py-2 text-sm text-right">{force.mx.toFixed(2)}</td>
                  <td className="px-4 py-2 text-sm text-right">{force.my.toFixed(2)}</td>
                  <td className="px-4 py-2 text-sm text-right">{force.mz.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

        {activeTab === 'stresses' && (
          <table className="w-full">
            <thead style={{ background: 'var(--bg-tertiary)', position: 'sticky', top: 0 }}>
              <tr>
                <th className="px-4 py-2 text-left text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>Element</th>
                <th className="px-4 py-2 text-right text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>Axial (MPa)</th>
                <th className="px-4 py-2 text-right text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>Shear Y (MPa)</th>
                <th className="px-4 py-2 text-right text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>Shear Z (MPa)</th>
                <th className="px-4 py-2 text-right text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>Torsion (MPa)</th>
                <th className="px-4 py-2 text-right text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>Bending Y (MPa)</th>
                <th className="px-4 py-2 text-right text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>Bending Z (MPa)</th>
              </tr>
            </thead>
            <tbody>
              {mockStresses.map((stress, idx) => (
                <tr 
                  key={stress.element}
                  className="border-t hover:bg-opacity-50 transition-colors"
                  style={{ 
                    borderColor: 'var(--border-primary)',
                    background: idx % 2 === 0 ? 'transparent' : 'var(--bg-tertiary)'
                  }}
                >
                  <td className="px-4 py-2 text-sm font-medium">{stress.element}</td>
                  <td className="px-4 py-2 text-sm text-right">{stress.axial.toFixed(2)}</td>
                  <td className="px-4 py-2 text-sm text-right">{stress.shearY.toFixed(2)}</td>
                  <td className="px-4 py-2 text-sm text-right">{stress.shearZ.toFixed(2)}</td>
                  <td className="px-4 py-2 text-sm text-right">{stress.torsion.toFixed(2)}</td>
                  <td className="px-4 py-2 text-sm text-right">{stress.bendingY.toFixed(2)}</td>
                  <td className="px-4 py-2 text-sm text-right">{stress.bendingZ.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
