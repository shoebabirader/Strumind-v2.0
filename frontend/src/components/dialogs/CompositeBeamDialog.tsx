'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { specializedDesignApi } from '@/lib/api';

interface CompositeBeamDialogProps {
  open: boolean;
  onClose: () => void;
}

export function CompositeBeamDialog({ open, onClose }: CompositeBeamDialogProps) {
  const [loading, setLoading] = useState(false);
  const { register, handleSubmit } = useForm({
    defaultValues: { span: 8, slab_thickness: 0.12, slab_width: 3, dead_load: 5, live_load: 3 },
  });

  const onSubmit = async (data: any) => {
    setLoading(true);
    try {
      await specializedDesignApi.compositeBeam({ ...data, steel_section: { name: 'ISMB300' }, loads: { dead: data.dead_load, live: data.live_load } });
      onClose();
    } catch (error) {
      console.error('Composite beam design failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader><DialogTitle>Composite Beam Design</DialogTitle></DialogHeader>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="grid grid-cols-3 gap-4">
            <div><Label htmlFor="span">Span (m)</Label><Input id="span" type="number" step="0.1" {...register('span', { valueAsNumber: true })} /></div>
            <div><Label htmlFor="slab_thickness">Slab Thick (m)</Label><Input id="slab_thickness" type="number" step="0.01" {...register('slab_thickness', { valueAsNumber: true })} /></div>
            <div><Label htmlFor="slab_width">Slab Width (m)</Label><Input id="slab_width" type="number" step="0.1" {...register('slab_width', { valueAsNumber: true })} /></div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div><Label htmlFor="dead_load">Dead Load (kN/m)</Label><Input id="dead_load" type="number" {...register('dead_load', { valueAsNumber: true })} /></div>
            <div><Label htmlFor="live_load">Live Load (kN/m)</Label><Input id="live_load" type="number" {...register('live_load', { valueAsNumber: true })} /></div>
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={onClose}>Cancel</Button>
            <Button type="submit" disabled={loading}>{loading ? 'Designing...' : 'Design Composite Beam'}</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
