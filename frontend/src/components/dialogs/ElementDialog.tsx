'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useElements } from '@/hooks/useElements';
import { useModelStore } from '@/stores/modelStore';

const elementSchema = z.object({
  node_i: z.number().min(1, 'Start node is required'),
  node_j: z.number().min(1, 'End node is required'),
  section_id: z.number().min(1, 'Section is required'),
  material_id: z.number().min(1, 'Material is required'),
  element_type: z.enum(['beam', 'column', 'truss', 'cable']),
});

type ElementFormData = z.infer<typeof elementSchema>;

interface ElementDialogProps {
  open: boolean;
  onClose: () => void;
  elementId?: number;
}

export function ElementDialog({ open, onClose, elementId }: ElementDialogProps) {
  const { currentProject } = useModelStore();
  const { createElement, updateElement } = useElements(currentProject?.id);
  const [loading, setLoading] = useState(false);

  const { register, handleSubmit, formState: { errors }, setValue, watch } = useForm<ElementFormData>({
    resolver: zodResolver(elementSchema),
    defaultValues: {
      node_i: 0,
      node_j: 0,
      section_id: 0,
      material_id: 0,
      element_type: 'beam',
    },
  });

  const onSubmit = async (data: ElementFormData) => {
    if (!currentProject) return;
    
    setLoading(true);
    try {
      if (elementId) {
        await updateElement({ id: elementId, data: { ...data, project_id: currentProject.id } });
      } else {
        await createElement({ ...data, project_id: currentProject.id });
      }
      onClose();
    } catch (error) {
      console.error('Failed to save element:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>{elementId ? 'Edit Element' : 'Create Element'}</DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="node_i">Start Node ID</Label>
              <Input
                id="node_i"
                type="number"
                {...register('node_i', { valueAsNumber: true })}
              />
              {errors.node_i && <p className="text-sm text-red-500">{errors.node_i.message}</p>}
            </div>
            <div>
              <Label htmlFor="node_j">End Node ID</Label>
              <Input
                id="node_j"
                type="number"
                {...register('node_j', { valueAsNumber: true })}
              />
              {errors.node_j && <p className="text-sm text-red-500">{errors.node_j.message}</p>}
            </div>
          </div>

          <div>
            <Label htmlFor="element_type">Element Type</Label>
            <Select
              onValueChange={(value) => setValue('element_type', value as any)}
              defaultValue="beam"
            >
              <SelectTrigger>
                <SelectValue placeholder="Select element type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="beam">Beam</SelectItem>
                <SelectItem value="column">Column</SelectItem>
                <SelectItem value="truss">Truss</SelectItem>
                <SelectItem value="cable">Cable</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="section_id">Section ID</Label>
              <Input
                id="section_id"
                type="number"
                {...register('section_id', { valueAsNumber: true })}
              />
              {errors.section_id && <p className="text-sm text-red-500">{errors.section_id.message}</p>}
            </div>
            <div>
              <Label htmlFor="material_id">Material ID</Label>
              <Input
                id="material_id"
                type="number"
                {...register('material_id', { valueAsNumber: true })}
              />
              {errors.material_id && <p className="text-sm text-red-500">{errors.material_id.message}</p>}
            </div>
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={onClose}>
              Cancel
            </Button>
            <Button type="submit" disabled={loading}>
              {loading ? 'Saving...' : elementId ? 'Update' : 'Create'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
