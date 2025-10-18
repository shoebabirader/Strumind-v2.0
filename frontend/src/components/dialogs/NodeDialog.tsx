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
  node_id: z.string().min(1, 'Node ID is required'),
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

  const { register, handleSubmit, formState: { errors } } = useForm<NodeFormData>({
    resolver: zodResolver(nodeSchema),
    defaultValues: {
      node_id: '',
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
    if (!currentProject) {
      alert('No project selected. Please create or select a project first.');
      return;
    }
    
    setLoading(true);
    try {
      // Convert restraints object to array format expected by backend
      const restraintsArray = [
        data.restraints.dx,
        data.restraints.dy,
        data.restraints.dz,
        data.restraints.rx,
        data.restraints.ry,
        data.restraints.rz,
      ];
      
      const nodeData: any = {
        node_id: data.node_id,
        x: data.x,
        y: data.y,
        z: data.z,
        restraints: restraintsArray,
        project_id: currentProject.id,
      };
      
      if (nodeId) {
        await updateNode({ id: nodeId, data: nodeData });
      } else {
        await createNode(nodeData);
      }
      onClose();
    } catch (error: any) {
      console.error('Failed to save node:', error);
      
      // Extract error message
      let errorMsg = 'Unknown error';
      if (error?.response?.data?.detail) {
        const detail = error.response.data.detail;
        if (typeof detail === 'string') {
          errorMsg = detail;
        } else if (Array.isArray(detail)) {
          errorMsg = detail.map((e: any) => e.msg || JSON.stringify(e)).join(', ');
        } else {
          errorMsg = JSON.stringify(detail);
        }
      } else if (error?.message) {
        errorMsg = error.message;
      }
      
      alert(`Failed to save node: ${errorMsg}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>{nodeId ? 'Edit Node' : 'Create Node'}</DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <Label htmlFor="node_id">Node ID</Label>
            <Input
              id="node_id"
              type="text"
              placeholder="N1"
              {...register('node_id')}
            />
            {errors.node_id && <p className="text-sm text-red-500">{errors.node_id.message}</p>}
          </div>

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
