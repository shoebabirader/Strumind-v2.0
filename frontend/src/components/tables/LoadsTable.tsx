'use client';

import { useLoads } from '@/hooks/useLoads';
import { useModelStore } from '@/stores/modelStore';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Pencil, Trash2 } from 'lucide-react';

export function LoadsTable() {
  const { currentProject } = useModelStore();
  const { loads, deleteLoad } = useLoads(currentProject?.id);

  const handleDelete = async (id: number) => {
    if (confirm('Are you sure you want to delete this load?')) {
      await deleteLoad(id);
    }
  };

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>ID</TableHead>
            <TableHead>Load Case</TableHead>
            <TableHead>Type</TableHead>
            <TableHead>Fx</TableHead>
            <TableHead>Fy</TableHead>
            <TableHead>Fz</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {loads.length === 0 ? (
            <TableRow>
              <TableCell colSpan={7} className="text-center text-gray-500">
                No loads applied yet
              </TableCell>
            </TableRow>
          ) : (
            loads.map((load) => (
              <TableRow key={load.id}>
                <TableCell className="font-medium">{load.id}</TableCell>
                <TableCell>
                  <Badge>{load.load_case}</Badge>
                </TableCell>
                <TableCell>{load.load_type}</TableCell>
                <TableCell>{load.values.fx?.toFixed(2) || 0}</TableCell>
                <TableCell>{load.values.fy?.toFixed(2) || 0}</TableCell>
                <TableCell>{load.values.fz?.toFixed(2) || 0}</TableCell>
                <TableCell className="text-right">
                  <div className="flex justify-end space-x-2">
                    <Button size="sm" variant="ghost">
                      <Pencil className="h-4 w-4" />
                    </Button>
                    <Button size="sm" variant="ghost" onClick={() => handleDelete(load.id)}>
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
