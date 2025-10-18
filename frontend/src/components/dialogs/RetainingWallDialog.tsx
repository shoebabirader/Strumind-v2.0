'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { specializedDesignApi } from '@/lib/api';

interface RetainingWallDialogProps {
  open: boolean;
  onClose: () => void;
}

export function RetainingWallDialog({ open, onClose }: RetainingWallDialogProps) {
  const [loading, setLoading] = useState(false);
  const { register, handleSubmit, setValue } = useForm({
    defaultValues: {
      wall_type: 'cantilever',
      height: 4,
      surcharge: 10,
    },
  });

  const onSubmit = async (data: any) => {
    setLoading(true);
    try {
      await specializedDesignApi.retainingWall({ ...data, soil_properties: {} });
      onClose();
    } catch (error) {
      console.error('Retaining wall design failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Retaining Wall Design</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <Label>Wall Type</Label>
            <Select defaultValue="cantilever" onValueChange={(v) => setValue('wall_type', v as any)}>
              <SelectTrigger><SelectValue /></SelectTrigger>
              <SelectContent>
                <SelectItem value="cantilever">Cantilever</SelectItem>
                <SelectItem value="gravity">Gravity</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="height">Height (m)</Label>
              <Input id="height" type="number" step="0.1" {...register('height', { valueAsNumber: true })} />
            </div>
            <div>
              <Label htmlFor="surcharge">Surcharge (kN/m²)</Label>
              <Input id="surcharge" type="number" {...register('surcharge', { valueAsNumber: true })} />
            </div>
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
