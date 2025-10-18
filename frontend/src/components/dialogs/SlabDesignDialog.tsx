'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { slabDesignApi } from '@/lib/api';

interface SlabDesignDialogProps {
  open: boolean;
  onClose: () => void;
}

export function SlabDesignDialog({ open, onClose }: SlabDesignDialogProps) {
  const [loading, setLoading] = useState(false);
  const { register, handleSubmit } = useForm({
    defaultValues: {
      span: 4,
      width: 3,
      lx: 4,
      ly: 5,
      dead_load: 2,
      live_load: 3,
    },
  });

  const onSubmit = async (data: any) => {
    setLoading(true);
    try {
      await slabDesignApi.oneWay({
        span: data.span,
        width: data.width,
        loads: { dead: data.dead_load, live: data.live_load },
      });
      onClose();
    } catch (error) {
      console.error('Slab design failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>Slab Design</DialogTitle>
        </DialogHeader>
        <Tabs defaultValue="oneway">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="oneway">One-Way</TabsTrigger>
            <TabsTrigger value="twoway">Two-Way</TabsTrigger>
            <TabsTrigger value="flat">Flat Slab</TabsTrigger>
          </TabsList>
          <TabsContent value="oneway">
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="span">Span (m)</Label>
                  <Input id="span" type="number" step="0.1" {...register('span', { valueAsNumber: true })} />
                </div>
                <div>
                  <Label htmlFor="width">Width (m)</Label>
                  <Input id="width" type="number" step="0.1" {...register('width', { valueAsNumber: true })} />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="dead_load">Dead Load (kN/m²)</Label>
                  <Input id="dead_load" type="number" step="0.1" {...register('dead_load', { valueAsNumber: true })} />
                </div>
                <div>
                  <Label htmlFor="live_load">Live Load (kN/m²)</Label>
                  <Input id="live_load" type="number" step="0.1" {...register('live_load', { valueAsNumber: true })} />
                </div>
              </div>
              <DialogFooter>
                <Button type="button" variant="outline" onClick={onClose}>Cancel</Button>
                <Button type="submit" disabled={loading}>{loading ? 'Designing...' : 'Design Slab'}</Button>
              </DialogFooter>
            </form>
          </TabsContent>
          <TabsContent value="twoway">
            <div className="text-sm text-gray-500 p-4">Two-way slab design</div>
          </TabsContent>
          <TabsContent value="flat">
            <div className="text-sm text-gray-500 p-4">Flat slab design with punching shear</div>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
