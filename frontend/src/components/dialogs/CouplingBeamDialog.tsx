'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { specializedDesignApi } from '@/lib/api';

interface CouplingBeamDialogProps {
  open: boolean;
  onClose: () => void;
}

export function CouplingBeamDialog({ open, onClose }: CouplingBeamDialogProps) {
  const [loading, setLoading] = useState(false);
  const { register, handleSubmit } = useForm({
    defaultValues: { span: 2, depth: 0.4, width: 0.3, shear_force: 150, moment: 100 },
  });

  const onSubmit = async (data: any) => {
    setLoading(true);
    try {
      await specializedDesignApi.couplingBeam(data);
      onClose();
    } catch (error) {
      console.error('Coupling beam design failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader><DialogTitle>Coupling Beam Design</DialogTitle></DialogHeader>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="grid grid-cols-3 gap-4">
            <div><Label htmlFor="span">Span (m)</Label><Input id="span" type="number" step="0.1" {...register('span', { valueAsNumber: true })} /></div>
            <div><Label htmlFor="depth">Depth (m)</Label><Input id="depth" type="number" step="0.01" {...register('depth', { valueAsNumber: true })} /></div>
            <div><Label htmlFor="width">Width (m)</Label><Input id="width" type="number" step="0.01" {...register('width', { valueAsNumber: true })} /></div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div><Label htmlFor="shear_force">Shear (kN)</Label><Input id="shear_force" type="number" {...register('shear_force', { valueAsNumber: true })} /></div>
            <div><Label htmlFor="moment">Moment (kNm)</Label><Input id="moment" type="number" {...register('moment', { valueAsNumber: true })} /></div>
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={onClose}>Cancel</Button>
            <Button type="submit" disabled={loading}>{loading ? 'Designing...' : 'Design Beam'}</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
