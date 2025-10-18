'use client';

import { useModelStore } from '@/stores/modelStore';
import { useNodes } from '@/hooks/useNodes';
import { useElements } from '@/hooks/useElements';
import { Badge } from '@/components/ui/badge';

export function StatusBar() {
  const { currentProject } = useModelStore();
  const { nodes } = useNodes(currentProject?.id);
  const { elements } = useElements(currentProject?.id);

  return (
    <footer className="h-8 bg-white border-t border-gray-200 flex items-center justify-between px-4 text-xs">
      <div className="flex items-center space-x-6 text-gray-600">
        <span>Nodes: {nodes.length}</span>
        <span>Elements: {elements.length}</span>
        <span>Materials: 0</span>
        <span>Loads: 0</span>
      </div>
      
      <div className="flex items-center space-x-4">
        <Badge variant="outline">Ready</Badge>
        <span className="text-gray-500">Units: SI (kN, m)</span>
      </div>
    </footer>
  );
}
