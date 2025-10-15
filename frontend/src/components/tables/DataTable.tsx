import React from 'react'

interface Column {
  key: string
  label: string
  align?: 'left' | 'center' | 'right'
  render?: (value: any, row: any) => React.ReactNode
}

interface DataTableProps {
  columns: Column[]
  data: any[]
  onRowClick?: (row: any) => void
  emptyMessage?: string
}

export default function DataTable({ columns, data, onRowClick, emptyMessage = 'No data available' }: DataTableProps) {
  return (
    <div className="flex-1 overflow-auto">
      <table className="w-full">
        <thead style={{ background: 'var(--bg-tertiary)', position: 'sticky', top: 0 }}>
          <tr>
            {columns.map((col) => (
              <th
                key={col.key}
                className={`px-4 py-2 text-${col.align || 'left'} text-xs font-medium`}
                style={{ color: 'var(--text-secondary)' }}
              >
                {col.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, idx) => (
            <tr
              key={idx}
              onClick={() => onRowClick?.(row)}
              className={`border-t hover:bg-opacity-50 transition-colors ${onRowClick ? 'cursor-pointer' : ''}`}
              style={{
                borderColor: 'var(--border-primary)',
                background: idx % 2 === 0 ? 'transparent' : 'var(--bg-tertiary)'
              }}
            >
              {columns.map((col) => (
                <td
                  key={col.key}
                  className={`px-4 py-2 text-sm text-${col.align || 'left'}`}
                >
                  {col.render ? col.render(row[col.key], row) : row[col.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>

      {data.length === 0 && (
        <div className="flex items-center justify-center h-32" style={{ color: 'var(--text-tertiary)' }}>
          {emptyMessage}
        </div>
      )}
    </div>
  )
}
