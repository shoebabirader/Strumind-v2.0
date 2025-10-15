import React, { useState } from 'react'
import { Activity } from 'lucide-react'
import { useModel } from '@/contexts/ModelContext'
import NodesTable from '@/components/tables/NodesTable'
import ElementsTable from '@/components/tables/ElementsTable'
import ResultsTable from '@/components/tables/ResultsTable'

interface PropertiesPanelProps {
  analysisResults?: any
}

export default function PropertiesPanel({ analysisResults }: PropertiesPanelProps) {
  const { selectedItems } = useModel()
  const [activePanel, setActivePanel] = useState<'properties' | 'tables' | 'results'>('properties')
  const [activeTable, setActiveTable] = useState<'nodes' | 'elements'>('nodes')

  return (
    <div className="w-96 flex flex-col" style={{ background: 'var(--bg-secondary)', borderLeft: '1px solid var(--border-primary)' }}>
      {/* Panel Tabs */}
      <div className="flex border-b" style={{ borderColor: 'var(--border-primary)' }}>
        <button
          onClick={() => setActivePanel('properties')}
          className={`flex-1 px-4 py-2 text-sm font-medium transition-colors ${
            activePanel === 'properties' ? 'border-b-2 border-blue-500' : ''
          }`}
          style={{ color: activePanel === 'properties' ? 'var(--accent-blue)' : 'var(--text-secondary)' }}
        >
          Properties
        </button>
        <button
          onClick={() => setActivePanel('tables')}
          className={`flex-1 px-4 py-2 text-sm font-medium transition-colors ${
            activePanel === 'tables' ? 'border-b-2 border-blue-500' : ''
          }`}
          style={{ color: activePanel === 'tables' ? 'var(--accent-blue)' : 'var(--text-secondary)' }}
        >
          Tables
        </button>
        <button
          onClick={() => setActivePanel('results')}
          className={`flex-1 px-4 py-2 text-sm font-medium transition-colors ${
            activePanel === 'results' ? 'border-b-2 border-blue-500' : ''
          }`}
          style={{ color: activePanel === 'results' ? 'var(--accent-blue)' : 'var(--text-secondary)' }}
        >
          Results
        </button>
      </div>

      {/* Panel Content */}
      <div className="flex-1 overflow-hidden flex flex-col">
        {activePanel === 'properties' && (
          <div className="flex-1 overflow-auto p-3 text-sm">
            {selectedItems.size > 0 ? (
              <div className="space-y-4">
                <div>
                  <div className="text-xs font-semibold mb-2 uppercase" style={{ color: 'var(--text-tertiary)' }}>Selection</div>
                  <div className="flex justify-between py-1 text-xs">
                    <span style={{ color: 'var(--text-secondary)' }}>Count:</span>
                    <span>{selectedItems.size}</span>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-8" style={{ color: 'var(--text-tertiary)' }}>
                <Activity className="w-12 h-12 mx-auto mb-2 opacity-50" />
                <p>No selection</p>
              </div>
            )}
          </div>
        )}

        {activePanel === 'tables' && (
          <div className="flex-1 flex flex-col">
            <div className="flex border-b" style={{ borderColor: 'var(--border-primary)' }}>
              <button
                onClick={() => setActiveTable('nodes')}
                className={`px-4 py-2 text-xs font-medium ${
                  activeTable === 'nodes' ? 'border-b-2 border-blue-500' : ''
                }`}
                style={{ color: activeTable === 'nodes' ? 'var(--accent-blue)' : 'var(--text-secondary)' }}
              >
                Nodes
              </button>
              <button
                onClick={() => setActiveTable('elements')}
                className={`px-4 py-2 text-xs font-medium ${
                  activeTable === 'elements' ? 'border-b-2 border-blue-500' : ''
                }`}
                style={{ color: activeTable === 'elements' ? 'var(--accent-blue)' : 'var(--text-secondary)' }}
              >
                Elements
              </button>
            </div>
            <div className="flex-1 overflow-hidden">
              {activeTable === 'nodes' && <NodesTable onEdit={(node) => console.log('Edit node:', node)} />}
              {activeTable === 'elements' && <ElementsTable onEdit={(elem) => console.log('Edit element:', elem)} />}
            </div>
          </div>
        )}

        {activePanel === 'results' && (
          <div className="flex-1 overflow-hidden">
            <ResultsTable results={analysisResults} />
          </div>
        )}
      </div>
    </div>
  )
}
