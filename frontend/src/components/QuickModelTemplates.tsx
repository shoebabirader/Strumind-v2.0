import { useState } from 'react'

interface Template {
  name: string
  description: string
  icon: string
}

const templates: Template[] = [
  { name: 'Simple Frame', description: '2D portal frame with 2 columns and 1 beam', icon: '⊓' },
  { name: 'Building Frame', description: '3D multi-story building frame', icon: '🏢' },
  { name: 'Truss', description: '2D truss structure', icon: '△' },
  { name: 'Grid Floor', description: 'Grid of beams and slabs', icon: '⊞' },
  { name: 'Bridge', description: 'Simple bridge structure', icon: '🌉' },
  { name: 'Blank', description: 'Start from scratch', icon: '📄' },
]

export default function QuickModelTemplates({ onSelect }: { onSelect: (template: string) => void }) {
  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-6">Quick Start - Select Template</h2>
      
      <div className="grid grid-cols-3 gap-4">
        {templates.map(template => (
          <button
            key={template.name}
            onClick={() => onSelect(template.name)}
            className="border-2 border-gray-300 rounded-lg p-6 hover:border-blue-600 hover:bg-blue-50 transition"
          >
            <div className="text-4xl mb-2">{template.icon}</div>
            <h3 className="font-bold mb-1">{template.name}</h3>
            <p className="text-sm text-gray-600">{template.description}</p>
          </button>
        ))}
      </div>

      <div className="mt-8 p-4 bg-blue-50 rounded">
        <h3 className="font-bold mb-2">💡 Pro Tip</h3>
        <p className="text-sm">
          Use the AI Assistant to generate models from descriptions or import IFC files from BIM software!
        </p>
      </div>
    </div>
  )
}
