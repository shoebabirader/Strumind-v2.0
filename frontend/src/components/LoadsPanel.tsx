import { useState } from 'react'

interface Load {
  id: number
  type: 'point' | 'distributed' | 'moment'
  node?: number
  element?: number
  direction: 'X' | 'Y' | 'Z' | 'MX' | 'MY' | 'MZ'
  magnitude: number
  loadCase: string
}

export default function LoadsPanel() {
  const [loads, setLoads] = useState<Load[]>([])
  const [loadCases, setLoadCases] = useState<string[]>(['Dead Load', 'Live Load', 'Wind Load'])

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

  return (
    <div className="p-4">
      <div className="flex gap-2 mb-4">
        <button onClick={addLoad} className="bg-green-600 text-white px-4 py-2 rounded">
          + Add Load
        </button>
        <button onClick={addLoadCase} className="bg-blue-600 text-white px-4 py-2 rounded">
          + Add Load Case
        </button>
      </div>

      <div className="mb-4">
        <h3 className="font-bold mb-2">Load Cases:</h3>
        <div className="flex gap-2">
          {loadCases.map(lc => (
            <span key={lc} className="px-3 py-1 bg-gray-200 rounded">{lc}</span>
          ))}
        </div>
      </div>

      <table className="w-full border">
        <thead className="bg-gray-100">
          <tr>
            <th className="p-2 border">ID</th>
            <th className="p-2 border">Type</th>
            <th className="p-2 border">Node/Element</th>
            <th className="p-2 border">Direction</th>
            <th className="p-2 border">Magnitude</th>
            <th className="p-2 border">Load Case</th>
            <th className="p-2 border">Actions</th>
          </tr>
        </thead>
        <tbody>
          {loads.map(load => (
            <tr key={load.id}>
              <td className="p-2 border">{load.id}</td>
              <td className="p-2 border">
                <select
                  value={load.type}
                  onChange={(e) => updateLoad(load.id, 'type', e.target.value)}
                  className="w-full p-1 border rounded"
                >
                  <option value="point">Point Load</option>
                  <option value="distributed">Distributed Load</option>
                  <option value="moment">Moment</option>
                </select>
              </td>
              <td className="p-2 border">
                <input
                  type="number"
                  placeholder={load.type === 'point' ? 'Node' : 'Element'}
                  onChange={(e) => updateLoad(load.id, load.type === 'point' ? 'node' : 'element', parseInt(e.target.value))}
                  className="w-full p-1 border rounded"
                />
              </td>
              <td className="p-2 border">
                <select
                  value={load.direction}
                  onChange={(e) => updateLoad(load.id, 'direction', e.target.value)}
                  className="w-full p-1 border rounded"
                >
                  <option value="X">X</option>
                  <option value="Y">Y</option>
                  <option value="Z">Z</option>
                  <option value="MX">MX</option>
                  <option value="MY">MY</option>
                  <option value="MZ">MZ</option>
                </select>
              </td>
              <td className="p-2 border">
                <input
                  type="number"
                  value={load.magnitude}
                  onChange={(e) => updateLoad(load.id, 'magnitude', parseFloat(e.target.value))}
                  className="w-full p-1 border rounded"
                  placeholder="kN or kNm"
                />
              </td>
              <td className="p-2 border">
                <select
                  value={load.loadCase}
                  onChange={(e) => updateLoad(load.id, 'loadCase', e.target.value)}
                  className="w-full p-1 border rounded"
                >
                  {loadCases.map(lc => (
                    <option key={lc} value={lc}>{lc}</option>
                  ))}
                </select>
              </td>
              <td className="p-2 border">
                <button
                  onClick={() => deleteLoad(load.id)}
                  className="text-red-600 hover:underline"
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
