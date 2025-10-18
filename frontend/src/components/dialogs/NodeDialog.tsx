'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import { useNodes } from '@/hooks/useNodes';
import { useModelStore } from '@/stores/modelStore';

const nodeSchema = z.object({
  x: z.number(),
  y: z.number(),
  z: z.number(),
  restraints: z.object({
    dx: z.boolean(),
    dy: z.boolean(),
    dz: z.boolean(),
    rx: z.boolean(),
    ry: z.boolean(),
    rz: z.boolean(),
  }),
});

type NodeFormData = z.infer<typeof nodeSchema>;

interface NodeDialogProps {
  open: boolean;
  onClose: () => void;
  nodeId?: number;
}

export function NodeDialog({ open, onClose, nodeId }: NodeDialogProps) {
  const { currentProject } = useModelStore();
  const { createNode, updateNode } = useNodes(currentProject?.id);
  const [loading, setLoading] = useState(false);

  const { register, handleSubmit, formState: { errors }, setValue, watch } = useForm<NodeFormData>({
    resolver: zodResolver(nodeSchema),
    defaultValues: {
      x: 0,
      y: 0,
      z: 0,
      restraints: {
        dx: false,
        dy: false,
        dz: false,
        rx: false,
        ry: false,
        rz: false,
      },
    },
  });

  const onSubmit = async (data: NodeFormData) => {
    if (!currentProject) return;
    
    setLoading(true);
    try {
      if (nodeId) {
        await updateNode({ id: nodeId, data: { ...data, project_id: currentProject.id } });
      } else {
        await createNode({ ...data, project_id: currentProject.id });
      }
      onClose();
    } catch (error) {
      console.error('Failed to save node:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>{nodeId ? 'Edit Node' : 'Create Node'}</DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="grid grid-cols-3 gap-4">
            <div>
              <Label htmlFor="x">X Coordinate</Label>
              <Input
                id="x"
                type="number"
                step="0.01"
                {...register('x', { valueAsNumber: true })}
              />
              {errors.x && <p className="text-sm text-red-500">{errors.x.message}</p>}
            </div>
            <div>
              <Label htmlFor="y">Y Coordinate</Label>
              <Input
                id="y"
                type="number"
                step="0.01"
                {...register('y', { valueAsNumber: true })}
              />
              {errors.y && <p className="text-sm text-red-500">{errors.y.message}</p>}
            </div>
            <div>
              <Label htmlFor="z">Z Coordinate</Label>
              <Input
                id="z"
                type="number"
                step="0.01"
                {...register('z', { valueAsNumber: true })}
              />
              {errors.z && <p className="text-sm text-red-500">{errors.z.message}</p>}
            </div>
          </div>

          <div>
            <Label className="mb-2 block">Restraints</Label>
            <div className="grid grid-cols-3 gap-4">
              {['dx', 'dy', 'dz', 'rx', 'ry', 'rz'].map((restraint) => (
                <div key={restraint} className="flex items-center space-x-2">
                  <Checkbox
                    id={restraint}
                    {...register(`restraints.${restraint as keyof typeof nodeSchema.shape.restraints.shape}`)}
                  />
                  <Label htmlFor={restraint} className="text-sm font-normal">
                    {restraint.toUpperCase()}
                  </Label>
                </div>
              ))}
            </div>
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={onClose}>
              Cancel
            </Button>
            <Button type="submit" disabled={loading}>
              {loading ? 'Saving...' : nodeId ? 'Update' : 'Create'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
