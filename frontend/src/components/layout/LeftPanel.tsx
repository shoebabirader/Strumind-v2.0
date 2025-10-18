'use client';

import { useModelStore } from '@/stores/modelStore';
import { useNodes } from '@/hooks/useNodes';
import { useElements } from '@/hooks/useElements';
import { Button } from '@/components/ui/button';
import { ChevronRight, ChevronDown } from 'lucide-react';
import { useState } from 'react';

export function LeftPanel() {
  const { currentProject } = useModelStore();
  const { nodes } = useNodes(currentProject?.id);
  const { elements } = useElements(currentProject?.id);
  
  const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>({
    nodes: true,
    elements: true,
    materials: false,
    loads: false,
    sections: false,
  });

  const toggleSection = (section: string) => {
    setExpandedSections(prev => ({ ...prev, [section]: !prev[section] }));
  };

  return (
    <aside className="w-64 bg-white border-r border-gray-200 overflow-y-auto">
      <div className="p-4">
        <h2 className="text-sm font-semibold text-gray-700 mb-3">Model Explorer</h2>
        
        <div className="space-y-1">
          {/* Nodes Section */}
          <div>
            <Button
              variant="ghost"
              size="sm"
              className="w-full justify-start"
              onClick={() => toggleSection('nodes')}
            >
              {expandedSections.nodes ? (
                <ChevronDown className="h-4 w-4 mr-2" />
              ) : (
                <ChevronRight className="h-4 w-4 mr-2" />
              )}
              📁 Nodes ({nodes.length})
            </Button>
            {expandedSections.nodes && (
              <div className="ml-6 mt-1 space-y-1">
                {nodes.slice(0, 10).map((node) => (
                  <div key={node.id} className="text-xs text-gray-600 py-1">
                    Node {node.id}: ({node.x}, {node.y}, {node.z})
                  </div>
                ))}
                {nodes.length > 10 && (
                  <div className="text-xs text-gray-400">
                    +{nodes.length - 10} more...
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Elements Section */}
          <div>
            <Button
              variant="ghost"
              size="sm"
              className="w-full justify-start"
              onClick={() => toggleSection('elements')}
            >
              {expandedSections.elements ? (
                <ChevronDown className="h-4 w-4 mr-2" />
              ) : (
                <ChevronRight className="h-4 w-4 mr-2" />
              )}
              📐 Elements ({elements.length})
            </Button>
            {expandedSections.elements && (
              <div className="ml-6 mt-1 space-y-1">
                {elements.slice(0, 10).map((element) => (
                  <div key={element.id} className="text-xs text-gray-600 py-1">
                    Element {element.id}: {element.element_type}
                  </div>
                ))}
                {elements.length > 10 && (
                  <div className="text-xs text-gray-400">
                    +{elements.length - 10} more...
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Other Sections */}
          <Button variant="ghost" size="sm" className="w-full justify-start">
            <ChevronRight className="h-4 w-4 mr-2" />
            🔧 Materials (0)
          </Button>
          
          <Button variant="ghost" size="sm" className="w-full justify-start">
            <ChevronRight className="h-4 w-4 mr-2" />
            ⚡ Loads (0)
          </Button>
          
          <Button variant="ghost" size="sm" className="w-full justify-start">
            <ChevronRight className="h-4 w-4 mr-2" />
            📊 Sections (0)
          </Button>
        </div>
      </div>
    </aside>
  );
}
