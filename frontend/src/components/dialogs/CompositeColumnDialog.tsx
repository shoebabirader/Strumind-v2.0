'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { specializedDesignApi } from '@/lib/api';

interface CompositeColumnDialogProps {
  open: boolean;
  onClose: () => void;
}

export function CompositeColumnDialog({ open, onClose }: CompositeColumnDialogProps) {
  const [loading, setLoading] = useState(false);
  const { register, handleSubmit } = useForm({
    defaultValues: { height: 3.5, axial_load: 2000, moment: 150 },
  });

  const onSubmit = async (data: any) => {
    setLoading(true);
    try {
      await specializedDesignApi.compositeColumn({ ...data, steel_section: { name: 'ISHB300' }, concrete_dimensions: { width: 400, depth: 400 } });
      onClose();
    } catch (error) {
      console.error('Composite column design failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader><DialogTitle>Composite Column Design</DialogTitle></DialogHeader>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="grid grid-cols-3 gap-4">
            <div><Label htmlFor="height">Height (m)</Label><Input id="height" type="number" step="0.1" {...register('height', { valueAsNumber: true })} /></div>
            <div><Label htmlFor="axial_load">Axial (kN)</Label><Input id="axial_load" type="number" {...register('axial_load', { valueAsNumber: true })} /></div>
            <div><Label htmlFor="moment">Moment (kNm)</Label><Input id="moment" type="number" {...register('moment', { valueAsNumber: true })} /></div>
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={onClose}>Cancel</Button>
            <Button type="submit" disabled={loading}>{loading ? 'Designing...' : 'Design Column'}</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
