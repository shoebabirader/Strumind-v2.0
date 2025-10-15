import React from 'react'
import { Edit2, Trash2, MapPin } from 'lucide-react'
import { useModel } from '@/contexts/ModelContext'

interface NodesTableProps {
  onEdit?: (node: any) => void
}

export default function NodesTable({ onEdit }: NodesTableProps) {
  const { nodes } = useModel()

  return (
    <div className="panel flex-1 flex flex-col">
      <div className="panel-header">
        <span><MapPin className="w-4 h-4 inline mr-2" />Nodes ({nodes.length})</span>
      </div>
      
      <div className="flex-1 overflow-auto">
        <table className="w-full">
          <thead style={{ background: 'var(--bg-tertiary)', position: 'sticky', top: 0 }}>
            <tr>
              <th className="px-4 py-2 text-left text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>ID</th>
              <th className="px-4 py-2 text-right text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>X (m)</th>
              <th className="px-4 py-2 text-right text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>Y (m)</th>
              <th className="px-4 py-2 text-right text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>Z (m)</th>
              <th className="px-4 py-2 text-center text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>Restraints</th>
              <th className="px-4 py-2 text-center text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {nodes.map((node, idx) => (
              <tr 
                key={node.id}
                className="border-t hover:bg-opacity-50 transition-colors"
                style={{ 
                  borderColor: 'var(--border-primary)',
                  background: idx % 2 === 0 ? 'transparent' : 'var(--bg-tertiary)'
                }}
              >
                <td className="px-4 py-2 text-sm font-medium">{node.id}</td>
                <td className="px-4 py-2 text-sm text-right">{node.x.toFixed(3)}</td>
                <td className="px-4 py-2 text-sm text-right">{node.y.toFixed(3)}</td>
                <td className="px-4 py-2 text-sm text-right">{node.z.toFixed(3)}</td>
                <td className="px-4 py-2 text-center">
                  <div className="flex justify-center space-x-1">
                    {node.restraints?.map((r: boolean, i: number) => (
                      <span
                        key={i}
                        className="w-5 h-5 rounded text-xs flex items-center justify-center"
                        style={{
                          background: r ? 'var(--accent-red)' : 'var(--bg-tertiary)',
                          color: r ? 'white' : 'var(--text-tertiary)'
                        }}
                        title={['UX', 'UY', 'UZ', 'RX', 'RY', 'RZ'][i]}
                      >
                        {['UX', 'UY', 'UZ', 'RX', 'RY', 'RZ'][i][1]}
                      </span>
                    ))}
                  </div>
                </td>
                <td className="px-4 py-2">
                  <div className="flex justify-center space-x-2">
                    <button
                      onClick={() => onEdit?.(node)}
                      className="toolbar-button"
                      title="Edit"
                    >
                      <Edit2 className="w-3 h-3" />
                    </button>
                    <button
                      className="toolbar-button"
                      title="Delete"
                    >
                      <Trash2 className="w-3 h-3" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        
        {nodes.length === 0 && (
          <div className="flex items-center justify-center h-32" style={{ color: 'var(--text-tertiary)' }}>
            No nodes defined. Click "Add Node" to create one.
          </div>
        )}
      </div>
    </div>
  )
}
