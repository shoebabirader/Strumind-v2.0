import React from 'react'
import { Edit2, Trash2, Box } from 'lucide-react'
import { useModel } from '@/contexts/ModelContext'

interface ElementsTableProps {
  onEdit?: (element: any) => void
}

export default function ElementsTable({ onEdit }: ElementsTableProps) {
  const { elements } = useModel()

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'beam': return 'var(--accent-blue)'
      case 'column': return 'var(--accent-red)'
      case 'brace': return 'var(--accent-green)'
      case 'truss': return 'var(--accent-purple)'
      default: return 'var(--text-tertiary)'
    }
  }

  return (
    <div className="panel flex-1 flex flex-col">
      <div className="panel-header">
        <span><Box className="w-4 h-4 inline mr-2" />Elements ({elements.length})</span>
      </div>
      
      <div className="flex-1 overflow-auto">
        <table className="w-full">
          <thead style={{ background: 'var(--bg-tertiary)', position: 'sticky', top: 0 }}>
            <tr>
              <th className="px-4 py-2 text-left text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>ID</th>
              <th className="px-4 py-2 text-center text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>Type</th>
              <th className="px-4 py-2 text-center text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>Node I</th>
              <th className="px-4 py-2 text-center text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>Node J</th>
              <th className="px-4 py-2 text-center text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>Material</th>
              <th className="px-4 py-2 text-center text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>Section</th>
              <th className="px-4 py-2 text-center text-xs font-medium" style={{ color: 'var(--text-secondary)' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {elements.map((element, idx) => (
              <tr 
                key={element.id}
                className="border-t hover:bg-opacity-50 transition-colors"
                style={{ 
                  borderColor: 'var(--border-primary)',
                  background: idx % 2 === 0 ? 'transparent' : 'var(--bg-tertiary)'
                }}
              >
                <td className="px-4 py-2 text-sm font-medium">{element.id}</td>
                <td className="px-4 py-2 text-center">
                  <span
                    className="px-2 py-1 rounded text-xs font-medium"
                    style={{ background: getTypeColor(element.type), color: 'white' }}
                  >
                    {element.type}
                  </span>
                </td>
                <td className="px-4 py-2 text-sm text-center">{element.nodeI}</td>
                <td className="px-4 py-2 text-sm text-center">{element.nodeJ}</td>
                <td className="px-4 py-2 text-sm text-center">{element.materialId}</td>
                <td className="px-4 py-2 text-sm text-center">
                  {element.sectionType} ({element.width}×{element.height})
                </td>
                <td className="px-4 py-2">
                  <div className="flex justify-center space-x-2">
                    <button
                      onClick={() => onEdit?.(element)}
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
        
        {elements.length === 0 && (
          <div className="flex items-center justify-center h-32" style={{ color: 'var(--text-tertiary)' }}>
            No elements defined. Click "Add Element" to create one.
          </div>
        )}
      </div>
    </div>
  )
}
