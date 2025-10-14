import { useState } from 'react'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface Load {
  id: number
  type: 'point' | 'distributed' | 'moment' | 'seismic' | 'wind'
  node?: number
  element?: number
  direction: 'X' | 'Y' | 'Z' | 'MX' | 'MY' | 'MZ'
  magnitude: number
  loadCase: string
}

interface SeismicParams {
  code: string
  zone: string
  importance_factor: number
  response_reduction_factor: number
  soil_type: string
}

interface WindParams {
  code: string
  basic_wind_speed: number
  terrain_category: number
  building_class: string
}

export default function LoadsPanel() {
  const [loads, setLoads] = useState<Load[]>([])
  const [loadCases, setLoadCases] = useState<string[]>(['Dead Load', 'Live Load'])
  const [activeTab, setActiveTab] = useState<'manual' | 'seismic' | 'wind'>('manual')

  // Seismic parameters
  const [seismicParams, setSeismicParams] = useState<SeismicParams>({
    code: 'IS1893',
    zone: 'ZONE_IV',
    importance_factor: 1.0,
    response_reduction_factor: 5.0,
    soil_type: 'MEDIUM'
  })

  // Wind parameters
  const [windParams, setWindParams] = useState<WindParams>({
    code: 'IS875',
    basic_wind_speed: 44.0,
    terrain_category: 2,
    building_class: 'B'
  })

  const [buildingData, setBuildingData] = useState({
    height: 30,
    width: 20,
    total_weight: 10000
  })

  const addLoad = () => {
    const newLoad: Load = {
      id: loads.length + 1,
      type: 'point',
      direction: 'Y',
      magnitude: 0,
      loadCase: loadCases[0],
    }
    setLoads([...loads, newLoad])
  }

  const updateLoad = (id: number, field: string, value: any) => {
    setLoads(loads.map(l => l.id === id ? { ...l, [field]: value } : l))
  }

  const deleteLoad = (id: number) => {
    setLoads(loads.filter(l => l.id !== id))
  }

  const addLoadCase = () => {
    const name = prompt('Enter load case name:')
    if (name) setLoadCases([...loadCases, name])
  }

  const generateSeismicLoads = async () => {
    try {
      const response = await axios.post(`${API_URL}/api/seismic/base-shear`, {
        parameters: seismicParams,
        total_weight: buildingData.total_weight,
        building_height: buildingData.height,
        building_type: 'RC_MRF'
      })

      const baseShear = response.data.results.base_shear

      // Add seismic load cases
      if (!loadCases.includes('Seismic X')) {
        setLoadCases([...loadCases, 'Seismic X', 'Seismic Y'])
      }

      // Add seismic loads
      const seismicLoadX: Load = {
        id: loads.length + 1,
        type: 'seismic',
        direction: 'X',
        magnitude: baseShear,
        loadCase: 'Seismic X'
      }

      const seismicLoadY: Load = {
        id: loads.length + 2,
        type: 'seismic',
        direction: 'Y',
        magnitude: baseShear,
        loadCase: 'Seismic Y'
      }

      setLoads([...loads, seismicLoadX, seismicLoadY])
      alert(`Seismic loads generated! Base Shear: ${baseShear.toFixed(2)} kN`)
    } catch (error) {
      console.error('Error generating seismic loads:', error)
      alert('Error generating seismic loads')
    }
  }

  const generateWindLoads = async () => {
    try {
      const response = await axios.post(`${API_URL}/api/wind/design-pressure`, {
        parameters: windParams,
        height: buildingData.height,
        building_dimensions: {
          width: buildingData.width,
          depth: buildingData.width,
          height: buildingData.height
        }
      })

      const pressure = response.data.results.design_pressure
      const windForce = (pressure * buildingData.height * buildingData.width) / 1000 // kN

      // Add wind load cases
      if (!loadCases.includes('Wind X')) {
        setLoadCases([...loadCases, 'Wind X', 'Wind Y'])
      }

      // Add wind loads
      const windLoadX: Load = {
        id: loads.length + 1,
        type: 'wind',
        direction: 'X',
        magnitude: windForce,
        loadCase: 'Wind X'
      }

      const windLoadY: Load = {
        id: loads.length + 2,
        type: 'wind',
        direction: 'Y',
        magnitude: windForce,
        loadCase: 'Wind Y'
      }

      setLoads([...loads, windLoadX, windLoadY])
      alert(`Wind loads generated! Wind Force: ${windForce.toFixed(2)} kN`)
    } catch (error) {
      console.error('Error generating wind loads:', error)
      alert('Error generating wind loads')
    }
  }

  return (
    <div className="p-4">
      {/* Tabs */}
      <div className="flex gap-2 mb-4 border-b">
        <button
          onClick={() => setActiveTab('manual')}
          className={`px-4 py-2 ${activeTab === 'manual' ? 'border-b-2 border-blue-600 text-blue-600 font-semibold' : 'text-gray-600'}`}
        >
          Manual Loads
        </button>
        <button
          onClick={() => setActiveTab('seismic')}
          className={`px-4 py-2 ${activeTab === 'seismic' ? 'border-b-2 border-blue-600 text-blue-600 font-semibold' : 'text-gray-600'}`}
        >
          Seismic Loads
        </button>
        <button
          onClick={() => setActiveTab('wind')}
          className={`px-4 py-2 ${activeTab === 'wind' ? 'border-b-2 border-blue-600 text-blue-600 font-semibold' : 'text-gray-600'}`}
        >
          Wind Loads
        </button>
      </div>

      {/* Manual Loads Tab */}
      {activeTab === 'manual' && (
        <>
          <div className="flex gap-2 mb-4">
            <button onClick={addLoad} className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
              + Add Load
            </button>
            <button onClick={addLoadCase} className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
              + Add Load Case
            </button>
          </div>

          <div className="mb-4">
            <h3 className="font-bold mb-2">Load Cases:</h3>
            <div className="flex gap-2 flex-wrap">
              {loadCases.map(lc => (
                <span key={lc} className="px-3 py-1 bg-gray-200 rounded text-sm">{lc}</span>
              ))}
            </div>
          </div>
        </>
      )}

      {/* Seismic Loads Tab */}
      {activeTab === 'seismic' && (
        <div className="space-y-4 mb-4">
          <h3 className="font-bold text-lg">Generate Seismic Loads</h3>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Seismic Code</label>
              <select
                value={seismicParams.code}
                onChange={(e) => setSeismicParams({ ...seismicParams, code: e.target.value })}
                className="w-full p-2 border rounded"
              >
                <option value="IS1893">IS 1893:2016 (India)</option>
                <option value="ASCE7">ASCE 7 (USA)</option>
                <option value="EC8">Eurocode 8 (Europe)</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Seismic Zone</label>
              <select
                value={seismicParams.zone}
                onChange={(e) => setSeismicParams({ ...seismicParams, zone: e.target.value })}
                className="w-full p-2 border rounded"
              >
                <option value="ZONE_II">Zone II (Z=0.10)</option>
                <option value="ZONE_III">Zone III (Z=0.16)</option>
                <option value="ZONE_IV">Zone IV (Z=0.24)</option>
                <option value="ZONE_V">Zone V (Z=0.36)</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Importance Factor (I)</label>
              <input
                type="number"
                step="0.1"
                value={seismicParams.importance_factor}
                onChange={(e) => setSeismicParams({ ...seismicParams, importance_factor: parseFloat(e.target.value) })}
                className="w-full p-2 border rounded"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Response Reduction (R)</label>
              <input
                type="number"
                step="0.5"
                value={seismicParams.response_reduction_factor}
                onChange={(e) => setSeismicParams({ ...seismicParams, response_reduction_factor: parseFloat(e.target.value) })}
                className="w-full p-2 border rounded"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Building Height (m)</label>
              <input
                type="number"
                value={buildingData.height}
                onChange={(e) => setBuildingData({ ...buildingData, height: parseFloat(e.target.value) })}
                className="w-full p-2 border rounded"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Total Weight (kN)</label>
              <input
                type="number"
                value={buildingData.total_weight}
                onChange={(e) => setBuildingData({ ...buildingData, total_weight: parseFloat(e.target.value) })}
                className="w-full p-2 border rounded"
              />
            </div>
          </div>

          <button
            onClick={generateSeismicLoads}
            className="w-full bg-blue-600 text-white px-6 py-3 rounded font-semibold hover:bg-blue-700"
          >
            Generate Seismic Loads
          </button>
        </div>
      )}

      {/* Wind Loads Tab */}
      {activeTab === 'wind' && (
        <div className="space-y-4 mb-4">
          <h3 className="font-bold text-lg">Generate Wind Loads</h3>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-1">Wind Code</label>
              <select
                value={windParams.code}
                onChange={(e) => setWindParams({ ...windParams, code: e.target.value })}
                className="w-full p-2 border rounded"
              >
                <option value="IS875">IS 875 Part 3:2015 (India)</option>
                <option value="ASCE7">ASCE 7 (USA)</option>
                <option value="AS1170">AS 1170.2 (Australia)</option>
                <option value="EC1">Eurocode 1 (Europe)</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Basic Wind Speed (m/s)</label>
              <input
                type="number"
                value={windParams.basic_wind_speed}
                onChange={(e) => setWindParams({ ...windParams, basic_wind_speed: parseFloat(e.target.value) })}
                className="w-full p-2 border rounded"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Terrain Category</label>
              <select
                value={windParams.terrain_category}
                onChange={(e) => setWindParams({ ...windParams, terrain_category: parseInt(e.target.value) })}
                className="w-full p-2 border rounded"
              >
                <option value="1">Category 1 - Exposed</option>
                <option value="2">Category 2 - Open</option>
                <option value="3">Category 3 - Suburban</option>
                <option value="4">Category 4 - Urban</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Building Class</label>
              <select
                value={windParams.building_class}
                onChange={(e) => setWindParams({ ...windParams, building_class: e.target.value })}
                className="w-full p-2 border rounded"
              >
                <option value="A">Class A - Temporary</option>
                <option value="B">Class B - Normal</option>
                <option value="C">Class C - Important</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Building Height (m)</label>
              <input
                type="number"
                value={buildingData.height}
                onChange={(e) => setBuildingData({ ...buildingData, height: parseFloat(e.target.value) })}
                className="w-full p-2 border rounded"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">Building Width (m)</label>
              <input
                type="number"
                value={buildingData.width}
                onChange={(e) => setBuildingData({ ...buildingData, width: parseFloat(e.target.value) })}
                className="w-full p-2 border rounded"
              />
            </div>
          </div>

          <button
            onClick={generateWindLoads}
            className="w-full bg-blue-600 text-white px-6 py-3 rounded font-semibold hover:bg-blue-700"
          >
            Generate Wind Loads
          </button>
        </div>
      )}

      {/* Loads Table */}
      <div className="mt-6">
        <h3 className="font-bold mb-2">Applied Loads ({loads.length})</h3>
        <div className="overflow-x-auto">
          <table className="w-full border border-gray-300 rounded">
            <thead className="bg-gray-100">
              <tr>
                <th className="p-2 border text-left">ID</th>
                <th className="p-2 border text-left">Type</th>
                <th className="p-2 border text-left">Node/Element</th>
                <th className="p-2 border text-left">Direction</th>
                <th className="p-2 border text-right">Magnitude</th>
                <th className="p-2 border text-left">Load Case</th>
                <th className="p-2 border text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              {loads.length === 0 ? (
                <tr>
                  <td colSpan={7} className="p-4 text-center text-gray-500">
                    No loads defined. Add manual loads or generate seismic/wind loads.
                  </td>
                </tr>
              ) : (
                loads.map(load => (
                  <tr key={load.id} className="hover:bg-gray-50">
                    <td className="p-2 border">{load.id}</td>
                    <td className="p-2 border">
                      {activeTab === 'manual' ? (
                        <select
                          value={load.type}
                          onChange={(e) => updateLoad(load.id, 'type', e.target.value)}
                          className="w-full p-1 border rounded text-sm"
                        >
                          <option value="point">Point Load</option>
                          <option value="distributed">Distributed Load</option>
                          <option value="moment">Moment</option>
                        </select>
                      ) : (
                        <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs font-semibold">
                          {load.type.toUpperCase()}
                        </span>
                      )}
                    </td>
                    <td className="p-2 border">
                      {load.type === 'seismic' || load.type === 'wind' ? (
                        <span className="text-gray-500 text-sm">Auto-generated</span>
                      ) : (
                        <input
                          type="number"
                          placeholder={load.type === 'point' ? 'Node' : 'Element'}
                          value={load.node || load.element || ''}
                          onChange={(e) => updateLoad(load.id, load.type === 'point' ? 'node' : 'element', parseInt(e.target.value))}
                          className="w-full p-1 border rounded text-sm"
                        />
                      )}
                    </td>
                    <td className="p-2 border">
                      <select
                        value={load.direction}
                        onChange={(e) => updateLoad(load.id, 'direction', e.target.value)}
                        className="w-full p-1 border rounded text-sm"
                      >
                        <option value="X">X</option>
                        <option value="Y">Y</option>
                        <option value="Z">Z</option>
                        <option value="MX">MX</option>
                        <option value="MY">MY</option>
                        <option value="MZ">MZ</option>
                      </select>
                    </td>
                    <td className="p-2 border text-right">
                      <input
                        type="number"
                        value={load.magnitude}
                        onChange={(e) => updateLoad(load.id, 'magnitude', parseFloat(e.target.value))}
                        className="w-full p-1 border rounded text-sm text-right"
                        placeholder="kN or kNm"
                      />
                    </td>
                    <td className="p-2 border">
                      <select
                        value={load.loadCase}
                        onChange={(e) => updateLoad(load.id, 'loadCase', e.target.value)}
                        className="w-full p-1 border rounded text-sm"
                      >
                        {loadCases.map(lc => (
                          <option key={lc} value={lc}>{lc}</option>
                        ))}
                      </select>
                    </td>
                    <td className="p-2 border text-center">
                      <button
                        onClick={() => deleteLoad(load.id)}
                        className="text-red-600 hover:text-red-800 text-sm font-medium"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Summary */}
      {loads.length > 0 && (
        <div className="mt-4 p-4 bg-blue-50 rounded">
          <h4 className="font-semibold mb-2">Load Summary</h4>
          <div className="grid grid-cols-3 gap-4 text-sm">
            <div>
              <span className="text-gray-600">Total Loads:</span>
              <span className="ml-2 font-semibold">{loads.length}</span>
            </div>
            <div>
              <span className="text-gray-600">Load Cases:</span>
              <span className="ml-2 font-semibold">{loadCases.length}</span>
            </div>
            <div>
              <span className="text-gray-600">Auto-Generated:</span>
              <span className="ml-2 font-semibold">
                {loads.filter(l => l.type === 'seismic' || l.type === 'wind').length}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
