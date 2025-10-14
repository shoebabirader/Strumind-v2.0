import React, { useState } from 'react'
import { advancedAnalysisAPI, specializedDesignAPI, serviceabilityAPI } from '../lib/api'
import { Box, Layers, Home, ArrowUpDown, Columns, CheckCircle, AlertCircle, Loader } from 'lucide-react'

export default function AdvancedDesignPanel() {
  const [activeModule, setActiveModule] = useState('slab')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)

  const modules = [
    { id: 'slab', label: 'Slab Design', icon: Layers },
    { id: 'wall', label: 'Shear Wall', icon: Box },
    { id: 'retaining', label: 'Retaining Wall', icon: Home },
    { id: 'staircase', label: 'Staircase', icon: ArrowUpDown },
    { id: 'composite', label: 'Composite', icon: Columns },
  ]

  const handleSlabDesign = async (formData: any) => {
    setLoading(true)
    try {
      const response = await advancedAnalysisAPI.slabDesign(formData)
      setResult(response.data.results)
    } catch (error) {
      console.error('Design error:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleShearWallDesign = async (formData: any) => {
    setLoading(true)
    try {
      const response = await specializedDesignAPI.shearWall(formData)
      setResult(response.data.results)
    } catch (error) {
      console.error('Design error:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="h-full bg-slate-50 flex">
      {/* Module Selector */}
      <div className="w-64 bg-white border-r border-slate-200 p-4">
        <h3 className="text-sm font-semibold text-slate-900 mb-4 uppercase tracking-wide">Design Modules</h3>
        <div className="space-y-1">
          {modules.map((module) => (
            <button
              key={module.id}
              onClick={() => {
                setActiveModule(module.id)
                setResult(null)
              }}
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-all ${
                activeModule === module.id
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-slate-700 hover:bg-slate-100'
              }`}
            >
              <module.icon className="w-5 h-5" />
              <span className="font-medium">{module.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Design Form */}
      <div className="flex-1 overflow-auto p-6">
        {activeModule === 'slab' && (
          <SlabDesignForm onSubmit={handleSlabDesign} loading={loading} result={result} />
        )}
        {activeModule === 'wall' && (
          <ShearWallDesignForm onSubmit={handleShearWallDesign} loading={loading} result={result} />
        )}
        {activeModule === 'retaining' && (
          <RetainingWallForm loading={loading} result={result} />
        )}
        {activeModule === 'staircase' && (
          <StaircaseForm loading={loading} result={result} />
        )}
        {activeModule === 'composite' && (
          <CompositeForm loading={loading} result={result} />
        )}
      </div>
    </div>
  )
}

function SlabDesignForm({ onSubmit, loading, result }: any) {
  const [formData, setFormData] = useState({
    slab_type: 'two_way',
    span_x: 5000,
    span_y: 6000,
    thickness: 150,
    dead_load: 2.0,
    live_load: 3.0,
    support_condition: 'all_edges_supported'
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit({
      ...formData,
      loads: {
        dead: formData.dead_load,
        live: formData.live_load
      }
    })
  }

  return (
    <div className="max-w-4xl">
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 mb-6">
        <h2 className="text-2xl font-bold text-slate-900 mb-2">Slab Design</h2>
        <p className="text-slate-600">Design one-way, two-way, or flat slabs per code requirements</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">Geometry</h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Slab Type</label>
              <select
                value={formData.slab_type}
                onChange={(e) => setFormData({ ...formData, slab_type: e.target.value })}
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="one_way">One-Way Slab</option>
                <option value="two_way">Two-Way Slab</option>
                <option value="flat_slab">Flat Slab</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Support Condition</label>
              <select
                value={formData.support_condition}
                onChange={(e) => setFormData({ ...formData, support_condition: e.target.value })}
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="simply_supported">Simply Supported</option>
                <option value="all_edges_supported">All Edges Supported</option>
                <option value="continuous">Continuous</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Span X (mm)</label>
              <input
                type="number"
                value={formData.span_x}
                onChange={(e) => setFormData({ ...formData, span_x: Number(e.target.value) })}
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Span Y (mm)</label>
              <input
                type="number"
                value={formData.span_y}
                onChange={(e) => setFormData({ ...formData, span_y: Number(e.target.value) })}
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Thickness (mm)</label>
              <input
                type="number"
                value={formData.thickness}
                onChange={(e) => setFormData({ ...formData, thickness: Number(e.target.value) })}
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">Loads</h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Dead Load (kN/m²)</label>
              <input
                type="number"
                step="0.1"
                value={formData.dead_load}
                onChange={(e) => setFormData({ ...formData, dead_load: Number(e.target.value) })}
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Live Load (kN/m²)</label>
              <input
                type="number"
                step="0.1"
                value={formData.live_load}
                onChange={(e) => setFormData({ ...formData, live_load: Number(e.target.value) })}
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
        >
          {loading ? (
            <>
              <Loader className="w-5 h-5 animate-spin" />
              <span>Designing...</span>
            </>
          ) : (
            <span>Design Slab</span>
          )}
        </button>
      </form>

      {result && (
        <div className="mt-6 bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <div className="flex items-center space-x-2 mb-4">
            {result.status === 'OK' ? (
              <CheckCircle className="w-6 h-6 text-green-600" />
            ) : (
              <AlertCircle className="w-6 h-6 text-red-600" />
            )}
            <h3 className="text-lg font-semibold text-slate-900">Design Results</h3>
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="p-4 bg-blue-50 rounded-lg">
              <div className="text-sm text-slate-600 mb-1">X-Direction Steel</div>
              <div className="text-lg font-bold text-blue-600">
                {result.x_direction_steel?.designation || 'N/A'}
              </div>
            </div>
            <div className="p-4 bg-purple-50 rounded-lg">
              <div className="text-sm text-slate-600 mb-1">Y-Direction Steel</div>
              <div className="text-lg font-bold text-purple-600">
                {result.y_direction_steel?.designation || 'N/A'}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

function ShearWallDesignForm({ onSubmit, loading, result }: any) {
  const [formData, setFormData] = useState({
    height: 12000,
    length: 4000,
    thickness: 250,
    axial_load: 2000,
    shear_force: 500,
    moment: 3000,
    boundary_element: true
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(formData)
  }

  return (
    <div className="max-w-4xl">
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 mb-6">
        <h2 className="text-2xl font-bold text-slate-900 mb-2">Shear Wall Design</h2>
        <p className="text-slate-600">Design RC shear walls with boundary elements</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">Geometry & Loads</h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Height (mm)</label>
              <input
                type="number"
                value={formData.height}
                onChange={(e) => setFormData({ ...formData, height: Number(e.target.value) })}
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Length (mm)</label>
              <input
                type="number"
                value={formData.length}
                onChange={(e) => setFormData({ ...formData, length: Number(e.target.value) })}
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Thickness (mm)</label>
              <input
                type="number"
                value={formData.thickness}
                onChange={(e) => setFormData({ ...formData, thickness: Number(e.target.value) })}
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Axial Load (kN)</label>
              <input
                type="number"
                value={formData.axial_load}
                onChange={(e) => setFormData({ ...formData, axial_load: Number(e.target.value) })}
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Shear Force (kN)</label>
              <input
                type="number"
                value={formData.shear_force}
                onChange={(e) => setFormData({ ...formData, shear_force: Number(e.target.value) })}
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Moment (kNm)</label>
              <input
                type="number"
                value={formData.moment}
                onChange={(e) => setFormData({ ...formData, moment: Number(e.target.value) })}
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
          <div className="mt-4">
            <label className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={formData.boundary_element}
                onChange={(e) => setFormData({ ...formData, boundary_element: e.target.checked })}
                className="w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
              />
              <span className="text-sm font-medium text-slate-700">Include Boundary Elements</span>
            </label>
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors disabled:opacity-50"
        >
          {loading ? 'Designing...' : 'Design Shear Wall'}
        </button>
      </form>

      {result && (
        <div className="mt-6 bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">Design Results</h3>
          <div className="space-y-2 text-sm">
            <p><span className="font-medium">Status:</span> {result.overall_status || result.status}</p>
            <p><span className="font-medium">Classification:</span> {result.classification}</p>
          </div>
        </div>
      )}
    </div>
  )
}

function RetainingWallForm({ loading, result }: any) {
  const [formData, setFormData] = useState({
    wall_type: 'cantilever',
    height: 4000,
    stem_thickness_top: 200,
    stem_thickness_bottom: 300,
    base_width: 2500,
    base_thickness: 400,
    toe_length: 800,
    surcharge: 10
  })

  return (
    <div className="max-w-4xl">
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 mb-6">
        <h2 className="text-2xl font-bold text-slate-900 mb-2">Retaining Wall Design</h2>
        <p className="text-slate-600">Design cantilever and gravity retaining walls</p>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <h3 className="text-lg font-semibold text-slate-900 mb-4">Geometry</h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">Wall Type</label>
            <select
              value={formData.wall_type}
              onChange={(e) => setFormData({ ...formData, wall_type: e.target.value })}
              className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="cantilever">Cantilever</option>
              <option value="gravity">Gravity</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">Height (mm)</label>
            <input
              type="number"
              value={formData.height}
              onChange={(e) => setFormData({ ...formData, height: Number(e.target.value) })}
              className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
      </div>
    </div>
  )
}

function StaircaseForm({ loading, result }: any) {
  const [formData, setFormData] = useState({
    stair_type: 'dog_legged',
    flight_length: 3000,
    flight_width: 1200,
    waist_thickness: 150,
    riser: 150,
    tread: 300
  })

  return (
    <div className="max-w-4xl">
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 mb-6">
        <h2 className="text-2xl font-bold text-slate-900 mb-2">Staircase Design</h2>
        <p className="text-slate-600">Design dog-legged, cantilever, and spiral staircases</p>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <h3 className="text-lg font-semibold text-slate-900 mb-4">Geometry</h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">Stair Type</label>
            <select
              value={formData.stair_type}
              onChange={(e) => setFormData({ ...formData, stair_type: e.target.value })}
              className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="dog_legged">Dog-Legged</option>
              <option value="cantilever">Cantilever</option>
              <option value="spiral">Spiral</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">Riser (mm)</label>
            <input
              type="number"
              value={formData.riser}
              onChange={(e) => setFormData({ ...formData, riser: Number(e.target.value) })}
              className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
      </div>
    </div>
  )
}

function CompositeForm({ loading, result }: any) {
  const [formData, setFormData] = useState({
    span: 8000,
    slab_thickness: 120,
    slab_width: 2000
  })

  return (
    <div className="max-w-4xl">
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 mb-6">
        <h2 className="text-2xl font-bold text-slate-900 mb-2">Composite Design</h2>
        <p className="text-slate-600">Design steel-concrete composite beams and columns</p>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <h3 className="text-lg font-semibold text-slate-900 mb-4">Geometry</h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">Span (mm)</label>
            <input
              type="number"
              value={formData.span}
              onChange={(e) => setFormData({ ...formData, span: Number(e.target.value) })}
              className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">Slab Thickness (mm)</label>
            <input
              type="number"
              value={formData.slab_thickness}
              onChange={(e) => setFormData({ ...formData, slab_thickness: Number(e.target.value) })}
              className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
      </div>
    </div>
  )
}
