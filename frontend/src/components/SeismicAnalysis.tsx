import { useState } from 'react'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface SeismicParameters {
  code: string
  zone: string
  importance_factor: number
  response_reduction_factor: number
  soil_type: string
}

export default function SeismicAnalysis() {
  const [parameters, setParameters] = useState<SeismicParameters>({
    code: 'IS1893',
    zone: 'ZONE_IV',
    importance_factor: 1.0,
    response_reduction_factor: 5.0,
    soil_type: 'MEDIUM'
  })

  const [buildingData, setBuildingData] = useState({
    total_weight: 10000,
    building_height: 30,
    building_type: 'RC_MRF'
  })

  const [results, setResults] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('base-shear')

  const calculateBaseShear = async () => {
    setLoading(true)
    try {
      const response = await axios.post(`${API_URL}/api/seismic/base-shear`, {
        parameters,
        ...buildingData
      })
      setResults(response.data.results)
    } catch (error) {
      console.error('Error calculating base shear:', error)
      alert('Error calculating base shear')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow">
        <h2 className="text-2xl font-bold mb-4">Seismic Analysis</h2>
        
        {/* Tabs */}
        <div className="flex gap-2 mb-6 border-b">
          <button
            onClick={() => setActiveTab('base-shear')}
            className={`px-4 py-2 ${activeTab === 'base-shear' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-600'}`}
          >
            Base Shear
          </button>
          <button
            onClick={() => setActiveTab('response-spectrum')}
            className={`px-4 py-2 ${activeTab === 'response-spectrum' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-600'}`}
          >
            Response Spectrum
          </button>
          <button
            onClick={() => setActiveTab('drift-check')}
            className={`px-4 py-2 ${activeTab === 'drift-check' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-600'}`}
          >
            Drift Check
          </button>
        </div>

        {/* Parameters */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          <div>
            <label className="block text-sm font-medium mb-2">Seismic Code</label>
            <select
              value={parameters.code}
              onChange={(e) => setParameters({...parameters, code: e.target.value})}
              className="w-full p-2 border rounded"
            >
              <option value="IS1893">IS 1893:2016 (India)</option>
              <option value="ASCE7">ASCE 7 (USA)</option>
              <option value="EC8">Eurocode 8 (Europe)</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Seismic Zone</label>
            <select
              value={parameters.zone}
              onChange={(e) => setParameters({...parameters, zone: e.target.value})}
              className="w-full p-2 border rounded"
            >
              <option value="ZONE_II">Zone II (Z=0.10)</option>
              <option value="ZONE_III">Zone III (Z=0.16)</option>
              <option value="ZONE_IV">Zone IV (Z=0.24)</option>
              <option value="ZONE_V">Zone V (Z=0.36)</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Importance Factor (I)</label>
            <input
              type="number"
              step="0.1"
              value={parameters.importance_factor}
              onChange={(e) => setParameters({...parameters, importance_factor: parseFloat(e.target.value)})}
              className="w-full p-2 border rounded"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Response Reduction (R)</label>
            <input
              type="number"
              step="0.5"
              value={parameters.response_reduction_factor}
              onChange={(e) => setParameters({...parameters, response_reduction_factor: parseFloat(e.target.value)})}
              className="w-full p-2 border rounded"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Soil Type</label>
            <select
              value={parameters.soil_type}
              onChange={(e) => setParameters({...parameters, soil_type: e.target.value})}
              className="w-full p-2 border rounded"
            >
              <option value="ROCK">Type I - Rock/Hard Soil</option>
              <option value="MEDIUM">Type II - Medium Soil</option>
              <option value="SOFT">Type III - Soft Soil</option>
            </select>
          </div>
        </div>

        {/* Building Data */}
        <div className="grid grid-cols-3 gap-4 mb-6">
          <div>
            <label className="block text-sm font-medium mb-2">Total Weight (kN)</label>
            <input
              type="number"
              value={buildingData.total_weight}
              onChange={(e) => setBuildingData({...buildingData, total_weight: parseFloat(e.target.value)})}
              className="w-full p-2 border rounded"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Building Height (m)</label>
            <input
              type="number"
              value={buildingData.building_height}
              onChange={(e) => setBuildingData({...buildingData, building_height: parseFloat(e.target.value)})}
              className="w-full p-2 border rounded"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Building Type</label>
            <select
              value={buildingData.building_type}
              onChange={(e) => setBuildingData({...buildingData, building_type: e.target.value})}
              className="w-full p-2 border rounded"
            >
              <option value="RC_MRF">RC Moment Frame</option>
              <option value="STEEL_MRF">Steel Moment Frame</option>
              <option value="RC_SHEAR_WALL">RC Shear Wall</option>
            </select>
          </div>
        </div>

        {/* Calculate Button */}
        <button
          onClick={calculateBaseShear}
          disabled={loading}
          className="w-full bg-blue-600 text-white py-3 rounded font-medium hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Calculating...' : 'Calculate Seismic Forces'}
        </button>
      </div>

      {/* Results */}
      {results && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-xl font-bold mb-4">Results</h3>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="p-4 bg-blue-50 rounded">
              <div className="text-sm text-gray-600">Base Shear</div>
              <div className="text-2xl font-bold text-blue-600">
                {results.base_shear?.toFixed(2)} kN
              </div>
            </div>

            <div className="p-4 bg-green-50 rounded">
              <div className="text-sm text-gray-600">Seismic Coefficient (Ah)</div>
              <div className="text-2xl font-bold text-green-600">
                {results.seismic_coefficient?.toFixed(4)}
              </div>
            </div>

            <div className="p-4 bg-purple-50 rounded">
              <div className="text-sm text-gray-600">Time Period</div>
              <div className="text-2xl font-bold text-purple-600">
                {results.time_period?.toFixed(3)} sec
              </div>
            </div>

            <div className="p-4 bg-orange-50 rounded">
              <div className="text-sm text-gray-600">Spectral Acceleration</div>
              <div className="text-2xl font-bold text-orange-600">
                {results.spectral_acceleration?.toFixed(3)}
              </div>
            </div>
          </div>

          <div className="mt-6 p-4 bg-gray-50 rounded">
            <h4 className="font-bold mb-2">Parameters Used:</h4>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div>Zone Factor (Z): {results.zone_factor}</div>
              <div>Importance Factor (I): {results.importance_factor}</div>
              <div>Response Reduction (R): {results.response_reduction}</div>
              <div>Code: {results.code}</div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
