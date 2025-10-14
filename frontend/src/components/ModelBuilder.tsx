import { useState } from 'react'
import { modelAPI } from '@/lib/api'

interface Node {
  id: number
  x: number
  y: number
  z: number
  restraints: boolean[]
}

interface Element {
  id: number
  type: 'beam' | 'column' | 'truss' | 'slab' | 'shell'
  nodes: number[]
  material: string
  section: string
}

interface Material {
  name: string
  E: number
  poisson: number
  density: number
  grade: string
}

interface Section {
  name: string
  type: 'rectangular' | 'circular' | 'I-section' | 'custom'
  properties: any
}

export default function ModelBuilder() {
  const [nodes, setNodes] = useState<Node[]>([])
  const [elements, setElements] = useState<Element[]>([])
  const [materials, setMaterials] = useState<Material[]>([
    { name: 'Concrete M25', E: 25e9, poisson: 0.2, density: 2500, grade: 'M25' },
    { name: 'Steel Fe415', E: 200e9, poisson: 0.3, density: 7850, grade: 'Fe415' },
  ])
  const [sections, setSections] = useState<Section[]>([
    { name: '300x450', type: 'rectangular', properties: { width: 300, depth: 450 } },
    { name: '300x300', type: 'rectangular', properties: { width: 300, depth: 300 } },
  ])

  const [activeTab, setActiveTab] = useState<'nodes' | 'elements' | 'materials' | 'sections'>('nodes')
  const [selectedNodes, setSelectedNodes] = useState<number[]>([])

  // Node operations
  const addNode = () => {
    const newNode: Node = {
      id: nodes.length + 1,
      x: 0,
      y: 0,
      z: 0,
      restraints: [false, false, false, false, false, false], // ux, uy, uz, rx, ry, rz
    }
    setNodes([...nodes, newNode])
  }

  const updateNode = (id: number, field: string, value: any) => {
    setNodes(nodes.map(n => n.id === id ? { ...n, [field]: value } : n))
  }

  const deleteNode = (id: number) => {
    setNodes(nodes.filter(n => n.id !== id))
    setElements(elements.filter(e => !e.nodes.includes(id)))
  }

  // Element operations
  const addElement = () => {
    if (selectedNodes.length < 2) {
      alert('Select at least 2 nodes to create an element')
      return
    }

    const newElement: Element = {
      id: elements.length + 1,
      type: 'beam',
      nodes: [...selectedNodes],
      material: materials[0]?.name || '',
      section: sections[0]?.name || '',
    }
    setElements([...elements, newElement])
    setSelectedNodes([])
  }

  const updateElement = (id: number, field: string, value: any) => {
    setElements(elements.map(e => e.id === id ? { ...e, [field]: value } : e))
  }

  const deleteElement = (id: number) => {
    setElements(elements.filter(e => e.id !== id))
  }

  // Material operations
  const addMaterial = () => {
    const newMaterial: Material = {
      name: `Material ${materials.length + 1}`,
      E: 25e9,
      poisson: 0.2,
      density: 2500,
      grade: 'M25',
    }
    setMaterials([...materials, newMaterial])
  }

  // Section operations
  const addSection = () => {
    const newSection: Section = {
      name: `Section ${sections.length + 1}`,
      type: 'rectangular',
      properties: { width: 300, depth: 450 },
    }
    setSections([...sections, newSection])
  }

  // Save model
  const saveModel = async () => {
    try {
      const modelData = {
        project_id: 1, // TODO: Get from context
        geometry_data: { nodes, elements },
        materials: materials.reduce((acc, m) => ({ ...acc, [m.name]: m }), {}),
        sections: sections.reduce((acc, s) => ({ ...acc, [s.name]: s }), {}),
      }
      
      const response = await modelAPI.create(modelData)
      alert('Model saved successfully!')
      console.log('Model ID:', response.data.id)
    } catch (error) {
      alert('Failed to save model')
      console.error(error)
    }
  }

  return (
    <div className="h-full flex flex-col">
      {/* Toolbar */}
      <div className="bg-gray-100 p-3 border-b flex gap-2">
        <button onClick={saveModel} className="bg-blue-600 text-white px-4 py-2 rounded">
          Save Model
        </button>
        <button onClick={() => { setNodes([]); setElements([]) }} className="bg-red-600 text-white px-4 py-2 rounded">
          Clear All
        </button>
        <div className="ml-auto text-sm text-gray-600">
          Nodes: {nodes.length} | Elements: {elements.length}
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b">
        {(['nodes', 'elements', 'materials', 'sections'] as const).map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-6 py-3 capitalize ${
              activeTab === tab ? 'bg-white border-b-2 border-blue-600' : 'bg-gray-50'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Content */}
      <div className="flex-1 overflow-auto p-4">
        {activeTab === 'nodes' && (
          <NodesPanel
            nodes={nodes}
            selectedNodes={selectedNodes}
            onAdd={addNode}
            onUpdate={updateNode}
            onDelete={deleteNode}
            onSelect={setSelectedNodes}
          />
        )}
        {activeTab === 'elements' && (
          <ElementsPanel
            elements={elements}
            materials={materials}
            sections={sections}
            onAdd={addElement}
            onUpdate={updateElement}
            onDelete={deleteElement}
          />
        )}
        {activeTab === 'materials' && (
          <MaterialsPanel materials={materials} onAdd={addMaterial} />
        )}
        {activeTab === 'sections' && (
          <SectionsPanel sections={sections} onAdd={addSection} />
        )}
      </div>
    </div>
  )
}

function NodesPanel({ nodes, selectedNodes, onAdd, onUpdate, onDelete, onSelect }: any) {
  return (
    <div>
      <button onClick={onAdd} className="bg-green-600 text-white px-4 py-2 rounded mb-4">
        + Add Node
      </button>

      <div className="overflow-x-auto">
        <table className="w-full border">
          <thead className="bg-gray-100">
            <tr>
              <th className="p-2 border">Select</th>
              <th className="p-2 border">ID</th>
              <th className="p-2 border">X (mm)</th>
              <th className="p-2 border">Y (mm)</th>
              <th className="p-2 border">Z (mm)</th>
              <th className="p-2 border">Restraints</th>
              <th className="p-2 border">Actions</th>
            </tr>
          </thead>
          <tbody>
            {nodes.map((node: Node) => (
              <tr key={node.id} className={selectedNodes.includes(node.id) ? 'bg-blue-50' : ''}>
                <td className="p-2 border text-center">
                  <input
                    type="checkbox"
                    checked={selectedNodes.includes(node.id)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        onSelect([...selectedNodes, node.id])
                      } else {
                        onSelect(selectedNodes.filter((id: number) => id !== node.id))
                      }
                    }}
                  />
                </td>
                <td className="p-2 border">{node.id}</td>
                <td className="p-2 border">
                  <input
                    type="number"
                    value={node.x}
                    onChange={(e) => onUpdate(node.id, 'x', parseFloat(e.target.value))}
                    className="w-full p-1 border rounded"
                  />
                </td>
                <td className="p-2 border">
                  <input
                    type="number"
                    value={node.y}
                    onChange={(e) => onUpdate(node.id, 'y', parseFloat(e.target.value))}
                    className="w-full p-1 border rounded"
                  />
                </td>
                <td className="p-2 border">
                  <input
                    type="number"
                    value={node.z}
                    onChange={(e) => onUpdate(node.id, 'z', parseFloat(e.target.value))}
                    className="w-full p-1 border rounded"
                  />
                </td>
                <td className="p-2 border text-xs">
                  {['Ux', 'Uy', 'Uz', 'Rx', 'Ry', 'Rz'].map((dof, i) => (
                    <label key={dof} className="inline-flex items-center mr-2">
                      <input
                        type="checkbox"
                        checked={node.restraints[i]}
                        onChange={(e) => {
                          const newRestraints = [...node.restraints]
                          newRestraints[i] = e.target.checked
                          onUpdate(node.id, 'restraints', newRestraints)
                        }}
                      />
                      <span className="ml-1">{dof}</span>
                    </label>
                  ))}
                </td>
                <td className="p-2 border">
                  <button
                    onClick={() => onDelete(node.id)}
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
    </div>
  )
}

function ElementsPanel({ elements, materials, sections, onAdd, onUpdate, onDelete }: any) {
  return (
    <div>
      <button onClick={onAdd} className="bg-green-600 text-white px-4 py-2 rounded mb-4">
        + Add Element (Select nodes first)
      </button>

      <div className="overflow-x-auto">
        <table className="w-full border">
          <thead className="bg-gray-100">
            <tr>
              <th className="p-2 border">ID</th>
              <th className="p-2 border">Type</th>
              <th className="p-2 border">Nodes</th>
              <th className="p-2 border">Material</th>
              <th className="p-2 border">Section</th>
              <th className="p-2 border">Actions</th>
            </tr>
          </thead>
          <tbody>
            {elements.map((elem: Element) => (
              <tr key={elem.id}>
                <td className="p-2 border">{elem.id}</td>
                <td className="p-2 border">
                  <select
                    value={elem.type}
                    onChange={(e) => onUpdate(elem.id, 'type', e.target.value)}
                    className="w-full p-1 border rounded"
                  >
                    <option value="beam">Beam</option>
                    <option value="column">Column</option>
                    <option value="truss">Truss</option>
                    <option value="slab">Slab</option>
                    <option value="shell">Shell</option>
                  </select>
                </td>
                <td className="p-2 border">{elem.nodes.join(', ')}</td>
                <td className="p-2 border">
                  <select
                    value={elem.material}
                    onChange={(e) => onUpdate(elem.id, 'material', e.target.value)}
                    className="w-full p-1 border rounded"
                  >
                    {materials.map((m: Material) => (
                      <option key={m.name} value={m.name}>{m.name}</option>
                    ))}
                  </select>
                </td>
                <td className="p-2 border">
                  <select
                    value={elem.section}
                    onChange={(e) => onUpdate(elem.id, 'section', e.target.value)}
                    className="w-full p-1 border rounded"
                  >
                    {sections.map((s: Section) => (
                      <option key={s.name} value={s.name}>{s.name}</option>
                    ))}
                  </select>
                </td>
                <td className="p-2 border">
                  <button
                    onClick={() => onDelete(elem.id)}
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
    </div>
  )
}

function MaterialsPanel({ materials, onAdd }: any) {
  return (
    <div>
      <button onClick={onAdd} className="bg-green-600 text-white px-4 py-2 rounded mb-4">
        + Add Material
      </button>

      <div className="grid gap-4">
        {materials.map((mat: Material) => (
          <div key={mat.name} className="border p-4 rounded">
            <h3 className="font-bold mb-2">{mat.name}</h3>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div>Young's Modulus (E): {(mat.E / 1e9).toFixed(0)} GPa</div>
              <div>Poisson's Ratio: {mat.poisson}</div>
              <div>Density: {mat.density} kg/m³</div>
              <div>Grade: {mat.grade}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

function SectionsPanel({ sections, onAdd }: any) {
  return (
    <div>
      <button onClick={onAdd} className="bg-green-600 text-white px-4 py-2 rounded mb-4">
        + Add Section
      </button>

      <div className="grid gap-4">
        {sections.map((sec: Section) => (
          <div key={sec.name} className="border p-4 rounded">
            <h3 className="font-bold mb-2">{sec.name}</h3>
            <div className="text-sm">
              <div>Type: {sec.type}</div>
              {sec.type === 'rectangular' && (
                <>
                  <div>Width: {sec.properties.width} mm</div>
                  <div>Depth: {sec.properties.depth} mm</div>
                </>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
