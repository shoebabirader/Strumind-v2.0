import { useState } from 'react'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface WindParameters {
  code: string
  basic_wind_speed: number
  terrain_category: number
  building_class: string
  risk_coefficient: number
  topography_factor: number
}

export default function WindAnalysis() {
  const [parameters, setParameters] = useState<WindParameters>({
    code: 'IS875',
    basic_wind_speed: 44.0,
    terrain_category: 2,
    building_class: 'B',
    risk_coefficient: 1.0,
    topography_factor: 1.0
  })

  const [buildingData, setBuildingData] = useState({
    height: 30,
    width: 20,
    depth: 20,
    mass_per_floor: 100000
  })

  const [results, setResults] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('pressure')

  const calculateWindPressure = async () => {
    setLoading(true)
    try {
      const response = await axios.post(`${API_URL}/api/wind/design-pressure`, {
        parameters,
        height: buildingData.height,
        building_dimensions: {
          width: buildingData.width,
          depth: buildingData.depth,
          height: buildingData.height
        }
      })
      setResults(response.data.results)
    } catch (error) {
      console.error('Error calculating wind pressure:', error)
      alert('Error calculating wind pressure')
    } finally {
      setLoading(false)
    }
  }

  const calculateDynamicResponse = async (type: 'along' | 'across') => {
    setLoading(true)
    try {
      const endpoint = type === 'along' ? 'along-wind-response' : 'across-wind-response'
      const response = await axios.post(`${API_URL}/api/wind/${endpoint}`, {
        parameters,
        ...buildingData,
        damping_ratio: 0.01
      })
      setResults(response.data.results)
    } catch (error) {
      console.error(`Error calculating ${type}-wind response:`, error)
      alert(`Error calculating ${type}-wind response`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-2xl font-bold mb-4">Wind Load Analysis</h2>
        
        {/* Tabs */}
        <div className="flex gap-2 mb-6 border-b">
          <button
            onClick={() => setActiveTab('pressure')}
            className={`px-4 py-2 ${activeTab === 'pressure' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-600'}`}
          >
            Wind Pressure
          </button>
          <button
            onClick={() => setActiveTab('dynamic')}
            className={`px-4 py-2 ${activeTab === 'dynamic' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-600'}`}
          >
            Dynamic Response
          </button>
          <button
            onClick={() => setActiveTab('cladding')}
            className={`px-4 py-2 ${activeTab === 'cladding' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-600'}`}
          >
            Cladding
          </button>
        </div>

        {/* Parameters */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div>
            <label className="block text-sm font-medium mb-2">Wind Code</label>
            <select
              value={parameters.code}
              onChange={(e) => setParameters({...parameters, code: e.target.value})}
              className="w-full p-2 border rounded"
            >
              <option value="IS875">IS 875 Part 3:2015 (India)</option>
              <option value="ASCE7">ASCE 7 (USA)</option>
              <option value="AS1170">AS 1170.2 (Australia)</option>
              <option value="EC1">Eurocode 1 (Europe)</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">
              Basic Wind Speed ({parameters.code === 'ASCE7' ? 'mph' : 'm/s'})
            </label>
            <input
              type="number"
              step="1"
              value={parameters.basic_wind_speed}
              onChange={(e) => setParameters({...parameters, basic_wind_speed: parseFloat(e.target.value)})}
              className="w-full p-2 border rounded"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Terrain Category</label>
            <select
              value={parameters.terrain_category}
              onChange={(e) => setParameters({...parameters, terrain_category: parseInt(e.target.value)})}
              className="w-full p-2 border rounded"
            >
              <option value="1">Category 1 - Exposed open terrain</option>
              <option value="2">Category 2 - Open with scattered obstructions</option>
              <option value="3">Category 3 - Numerous obstructions</option>
              <option value="4">Category 4 - Large closely spaced obstructions</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Building Class</label>
            <select
              value={parameters.building_class}
              onChange={(e) => setParameters({...parameters, building_class: e.target.value})}
              className="w-full p-2 border rounded"
            >
              <option value="A">Class A - Temporary structures</option>
              <option value="B">Class B - Normal buildings</option>
              <option value="C">Class C - Important buildings</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Risk Coefficient (k1)</label>
            <input
              type="number"
              step="0.1"
              value={parameters.risk_coefficient}
              onChange={(e) => setParameters({...parameters, risk_coefficient: parseFloat(e.target.value)})}
              className="w-full p-2 border rounded"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Topography Factor (k3)</label>
            <input
              type="number"
              step="0.1"
              value={parameters.topography_factor}
              onChange={(e) => setParameters({...parameters, topography_factor: parseFloat(e.target.value)})}
              className="w-full p-2 border rounded"
            />
          </div>
        </div>

        {/* Building Data */}
        <div className="grid grid-cols-4 gap-4 mb-6">
          <div>
            <label className="block text-sm font-medium mb-2">Height (m)</label>
            <input
              type="number"
              value={buildingData.height}
              onChange={(e) => setBuildingData({...buildingData, height: parseFloat(e.target.value)})}
              className="w-full p-2 border rounded"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Width (m)</label>
            <input
              type="number"
              value={buildingData.width}
              onChange={(e) => setBuildingData({...buildingData, width: parseFloat(e.target.value)})}
              className="w-full p-2 border rounded"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Depth (m)</label>
            <input
              type="number"
              value={buildingData.depth}
              onChange={(e) => setBuildingData({...buildingData, depth: parseFloat(e.target.value)})}
              className="w-full p-2 border rounded"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Mass/Floor (kg)</label>
            <input
              type="number"
              value={buildingData.mass_per_floor}
              onChange={(e) => setBuildingData({...buildingData, mass_per_floor: parseFloat(e.target.value)})}
              className="w-full p-2 border rounded"
            />
          </div>
        </div>

        {/* Calculate Buttons */}
        <div className="flex gap-4">
          {activeTab === 'pressure' && (
            <button
              onClick={calculateWindPressure}
              disabled={loading}
              className="flex-1 bg-blue-600 text-white py-3 rounded font-medium hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? 'Calculating...' : 'Calculate Wind Pressure'}
            </button>
          )}
          {activeTab === 'dynamic' && (
            <>
              <button
                onClick={() => calculateDynamicResponse('along')}
                disabled={loading}
                className="flex-1 bg-blue-600 text-white py-3 rounded font-medium hover:bg-blue-700 disabled:opacity-50"
              >
                {loading ? 'Calculating...' : 'Along-Wind Response'}
              </button>
              <button
                onClick={() => calculateDynamicResponse('across')}
                disabled={loading}
                className="flex-1 bg-green-600 text-white py-3 rounded font-medium hover:bg-green-700 disabled:opacity-50"
              >
                {loading ? 'Calculating...' : 'Across-Wind Response'}
              </button>
            </>
          )}
        </div>
      </div>

      {/* Results */}
      {results && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-xl font-bold mb-4">Results</h3>
          
          {activeTab === 'pressure' && (
            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 bg-blue-50 rounded">
                <div className="text-sm text-gray-600">Design Pressure</div>
                <div className="text-2xl font-bold text-blue-600">
                  {results.design_pressure?.toFixed(2)} N/m²
                </div>
              </div>

              <div className="p-4 bg-green-50 rounded">
                <div className="text-sm text-gray-600">Design Wind Speed</div>
                <div className="text-2xl font-bold text-green-600">
                  {results.design_wind_speed?.toFixed(2)} m/s
                </div>
              </div>

              <div className="p-4 bg-purple-50 rounded">
                <div className="text-sm text-gray-600">Terrain Factor (k2)</div>
                <div className="text-2xl font-bold text-purple-600">
                  {results.terrain_height_factor?.toFixed(3)}
                </div>
              </div>

              <div className="p-4 bg-orange-50 rounded">
                <div className="text-sm text-gray-600">Pressure Coefficient</div>
                <div className="text-2xl font-bold text-orange-600">
                  {results.net_pressure_coeff?.toFixed(3)}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'dynamic' && results.peak_force && (
            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 bg-blue-50 rounded">
                <div className="text-sm text-gray-600">Peak Force</div>
                <div className="text-2xl font-bold text-blue-600">
                  {results.peak_force?.toFixed(2)} kN
                </div>
              </div>

              <div className="p-4 bg-green-50 rounded">
                <div className="text-sm text-gray-600">Displacement</div>
                <div className="text-2xl font-bold text-green-600">
                  {results.displacement?.toFixed(2)} mm
                </div>
              </div>

              <div className="p-4 bg-purple-50 rounded">
                <div className="text-sm text-gray-600">Natural Frequency</div>
                <div className="text-2xl font-bold text-purple-600">
                  {results.natural_frequency?.toFixed(3)} Hz
                </div>
              </div>

              <div className="p-4 bg-orange-50 rounded">
                <div className="text-sm text-gray-600">Gust Factor</div>
                <div className="text-2xl font-bold text-orange-600">
                  {results.gust_factor?.toFixed(3)}
                </div>
              </div>

              {results.is_critical !== undefined && (
                <div className={`col-span-2 p-4 rounded ${results.is_critical ? 'bg-red-50' : 'bg-green-50'}`}>
                  <div className="text-sm text-gray-600">Status</div>
                  <div className={`text-lg font-bold ${results.is_critical ? 'text-red-600' : 'text-green-600'}`}>
                    {results.recommendation}
                  </div>
                </div>
              )}
            </div>
          )}

          <div className="mt-6 p-4 bg-gray-50 rounded">
            <h4 className="font-bold mb-2">Parameters Used:</h4>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div>Code: {results.code}</div>
              <div>Height: {results.height} m</div>
              {results.basic_wind_speed && <div>Basic Wind Speed: {results.basic_wind_speed} m/s</div>}
              {results.damping_ratio && <div>Damping Ratio: {results.damping_ratio}</div>}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
