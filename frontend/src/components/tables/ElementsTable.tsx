'use client';

import { useElements } from '@/hooks/useElements';
import { useModelStore } from '@/stores/modelStore';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Pencil, Trash2 } from 'lucide-react';

export function ElementsTable() {
  const { currentProject } = useModelStore();
  const { elements, deleteElement } = useElements(currentProject?.id);

  const handleDelete = async (id: number) => {
    if (confirm('Are you sure you want to delete this element?')) {
      await deleteElement(id);
    }
  };

  const getElementTypeBadge = (type: string) => {
    const colors: Record<string, string> = {
      beam: 'bg-blue-100 text-blue-800',
      column: 'bg-green-100 text-green-800',
      truss: 'bg-yellow-100 text-yellow-800',
      cable: 'bg-purple-100 text-purple-800',
    };
    return colors[type] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>ID</TableHead>
            <TableHead>Type</TableHead>
            <TableHead>Node I</TableHead>
            <TableHead>Node J</TableHead>
            <TableHead>Section</TableHead>
            <TableHead>Material</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {elements.length === 0 ? (
            <TableRow>
              <TableCell colSpan={7} className="text-center text-gray-500">
                No elements created yet
              </TableCell>
            </TableRow>
          ) : (
            elements.map((element) => (
              <TableRow key={element.id}>
                <TableCell className="font-medium">{element.id}</TableCell>
                <TableCell>
                  <Badge className={getElementTypeBadge(element.element_type)}>
                    {element.element_type}
                  </Badge>
                </TableCell>
                <TableCell>{element.node_i}</TableCell>
                <TableCell>{element.node_j}</TableCell>
                <TableCell>{element.section_id}</TableCell>
                <TableCell>{element.material_id}</TableCell>
                <TableCell className="text-right">
                  <div className="flex justify-end space-x-2">
                    <Button size="sm" variant="ghost">
                      <Pencil className="h-4 w-4" />
                    </Button>
                    <Button
                      size="sm"
                      variant="ghost"
                      onClick={() => handleDelete(element.id)}
                    >
                      <Trash2 className="h-4 w-4 text-red-500" />
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
    </div>
  );
}
