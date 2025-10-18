'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { specializedDesignApi } from '@/lib/api';

interface StaircaseDialogProps {
  open: boolean;
  onClose: () => void;
}

export function StaircaseDialog({ open, onClose }: StaircaseDialogProps) {
  const [loading, setLoading] = useState(false);
  const { register, handleSubmit, setValue } = useForm({
    defaultValues: {
      stair_type: 'dog_legged',
      waist_thickness: 0.15,
      riser: 0.15,
      tread: 0.3,
    },
  });

  const onSubmit = async (data: any) => {
    setLoading(true);
    try {
      await specializedDesignApi.staircase({ ...data, loads: { dead: 1, live: 3 } });
      onClose();
    } catch (error) {
      console.error('Staircase design failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Staircase Design</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <Label>Staircase Type</Label>
            <Select defaultValue="dog_legged" onValueChange={(v) => setValue('stair_type', v as any)}>
              <SelectTrigger><SelectValue /></SelectTrigger>
              <SelectContent>
                <SelectItem value="dog_legged">Dog-Legged</SelectItem>
                <SelectItem value="cantilever">Cantilever</SelectItem>
                <SelectItem value="spiral">Spiral</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div className="grid grid-cols-3 gap-4">
            <div>
              <Label htmlFor="waist_thickness">Waist (m)</Label>
              <Input id="waist_thickness" type="number" step="0.01" {...register('waist_thickness', { valueAsNumber: true })} />
            </div>
            <div>
              <Label htmlFor="riser">Riser (m)</Label>
              <Input id="riser" type="number" step="0.01" {...register('riser', { valueAsNumber: true })} />
            </div>
            <div>
              <Label htmlFor="tread">Tread (m)</Label>
              <Input id="tread" type="number" step="0.01" {...register('tread', { valueAsNumber: true })} />
            </div>
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={onClose}>Cancel</Button>
            <Button type="submit" disabled={loading}>{loading ? 'Designing...' : 'Design Staircase'}</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
