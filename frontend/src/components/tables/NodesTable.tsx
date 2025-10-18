'use client';

import { useNodes } from '@/hooks/useNodes';
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
import { Pencil, Trash2 } from 'lucide-react';

export function NodesTable() {
  const { currentProject } = useModelStore();
  const { nodes, deleteNode } = useNodes(currentProject?.id);

  const handleDelete = async (id: number) => {
    if (confirm('Are you sure you want to delete this node?')) {
      await deleteNode(id);
    }
  };

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>ID</TableHead>
            <TableHead>X</TableHead>
            <TableHead>Y</TableHead>
            <TableHead>Z</TableHead>
            <TableHead>Restraints</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {nodes.length === 0 ? (
            <TableRow>
              <TableCell colSpan={6} className="text-center text-gray-500">
                No nodes created yet
              </TableCell>
            </TableRow>
          ) : (
            nodes.map((node) => (
              <TableRow key={node.id}>
                <TableCell className="font-medium">{node.id}</TableCell>
                <TableCell>{node.x.toFixed(2)}</TableCell>
                <TableCell>{node.y.toFixed(2)}</TableCell>
                <TableCell>{node.z.toFixed(2)}</TableCell>
                <TableCell>
                  {node.restraints ? (
                    <span className="text-xs">
                      {Object.entries(node.restraints)
                        .filter(([_, v]) => v)
                        .map(([k]) => k.toUpperCase())
                        .join(', ') || 'Free'}
                    </span>
                  ) : (
                    'Free'
                  )}
                </TableCell>
                <TableCell className="text-right">
                  <div className="flex justify-end space-x-2">
                    <Button size="sm" variant="ghost">
                      <Pencil className="h-4 w-4" />
                    </Button>
                    <Button
                      size="sm"
                      variant="ghost"
                      onClick={() => handleDelete(node.id)}
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
