'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import { specializedDesignApi } from '@/lib/api';

interface ShearWallDialogProps {
  open: boolean;
  onClose: () => void;
}

export function ShearWallDialog({ open, onClose }: ShearWallDialogProps) {
  const [loading, setLoading] = useState(false);
  const [boundaryElement, setBoundaryElement] = useState(false);
  const { register, handleSubmit } = useForm({
    defaultValues: {
      height: 3,
      length: 4,
      thickness: 0.2,
      axial_load: 1000,
      shear_force: 200,
      moment: 600,
    },
  });

  const onSubmit = async (data: any) => {
    setLoading(true);
    try {
      await specializedDesignApi.shearWall({ ...data, boundary_element: boundaryElement });
      onClose();
    } catch (error) {
      console.error('Shear wall design failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Shear Wall Design</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="grid grid-cols-3 gap-4">
            <div>
              <Label htmlFor="height">Height (m)</Label>
              <Input id="height" type="number" step="0.1" {...register('height', { valueAsNumber: true })} />
            </div>
            <div>
              <Label htmlFor="length">Length (m)</Label>
              <Input id="length" type="number" step="0.1" {...register('length', { valueAsNumber: true })} />
            </div>
            <div>
              <Label htmlFor="thickness">Thickness (m)</Label>
              <Input id="thickness" type="number" step="0.01" {...register('thickness', { valueAsNumber: true })} />
            </div>
          </div>
          <div className="grid grid-cols-3 gap-4">
            <div>
              <Label htmlFor="axial_load">Axial (kN)</Label>
              <Input id="axial_load" type="number" {...register('axial_load', { valueAsNumber: true })} />
            </div>
            <div>
              <Label htmlFor="shear_force">Shear (kN)</Label>
              <Input id="shear_force" type="number" {...register('shear_force', { valueAsNumber: true })} />
            </div>
            <div>
              <Label htmlFor="moment">Moment (kNm)</Label>
              <Input id="moment" type="number" {...register('moment', { valueAsNumber: true })} />
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Checkbox id="boundary" checked={boundaryElement} onCheckedChange={(c) => setBoundaryElement(c as boolean)} />
            <Label htmlFor="boundary" className="font-normal">Include boundary elements</Label>
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={onClose}>Cancel</Button>
            <Button type="submit" disabled={loading}>{loading ? 'Designing...' : 'Design Wall'}</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
