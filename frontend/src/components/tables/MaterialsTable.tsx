'use client';

import { useMaterials } from '@/hooks/useMaterials';
import { useModelStore } from '@/stores/modelStore';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Pencil, Trash2 } from 'lucide-react';

export function MaterialsTable() {
  const { currentProject } = useModelStore();
  const { materials, deleteMaterial } = useMaterials(currentProject?.id);

  const handleDelete = async (id: number) => {
    if (confirm('Are you sure you want to delete this material?')) {
      await deleteMaterial(id);
    }
  };

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>ID</TableHead>
            <TableHead>Name</TableHead>
            <TableHead>Type</TableHead>
            <TableHead>E (MPa)</TableHead>
            <TableHead>Density</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {materials.length === 0 ? (
            <TableRow>
              <TableCell colSpan={6} className="text-center text-gray-500">
                No materials created yet
              </TableCell>
            </TableRow>
          ) : (
            materials.map((material) => (
              <TableRow key={material.id}>
                <TableCell className="font-medium">{material.id}</TableCell>
                <TableCell>{material.name}</TableCell>
                <TableCell>
                  <Badge variant="outline">{material.material_type}</Badge>
                </TableCell>
                <TableCell>{material.elastic_modulus?.toFixed(0)}</TableCell>
                <TableCell>{material.density}</TableCell>
                <TableCell className="text-right">
                  <div className="flex justify-end space-x-2">
                    <Button size="sm" variant="ghost">
                      <Pencil className="h-4 w-4" />
                    </Button>
                    <Button size="sm" variant="ghost" onClick={() => handleDelete(material.id)}>
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
