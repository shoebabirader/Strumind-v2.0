'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
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
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
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
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="lx">Short Span Lx (m)</Label>
                  <Input id="lx" type="number" step="0.1" {...register('lx', { valueAsNumber: true })} />
                </div>
                <div>
                  <Label htmlFor="ly">Long Span Ly (m)</Label>
                  <Input id="ly" type="number" step="0.1" {...register('ly', { valueAsNumber: true })} />
                </div>
                <div>
                  <Label htmlFor="thickness_2way">Thickness (mm)</Label>
                  <Input id="thickness_2way" type="number" defaultValue="150" />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="dead_load_2way">Dead Load (kN/m²)</Label>
                  <Input id="dead_load_2way" type="number" step="0.1" {...register('dead_load', { valueAsNumber: true })} />
                </div>
                <div>
                  <Label htmlFor="live_load_2way">Live Load (kN/m²)</Label>
                  <Input id="live_load_2way" type="number" step="0.1" {...register('live_load', { valueAsNumber: true })} />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>Edge Condition</Label>
                  <Select defaultValue="simply">
                    <SelectTrigger><SelectValue /></SelectTrigger>
                    <SelectContent>
                      <SelectItem value="simply">Simply Supported</SelectItem>
                      <SelectItem value="continuous">Continuous</SelectItem>
                      <SelectItem value="fixed">Fixed</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label>Ly/Lx Ratio</Label>
                  <Input type="number" step="0.1" defaultValue="1.25" disabled />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>Concrete Grade</Label>
                  <Select defaultValue="M25">
                    <SelectTrigger><SelectValue /></SelectTrigger>
                    <SelectContent>
                      <SelectItem value="M20">M20</SelectItem>
                      <SelectItem value="M25">M25</SelectItem>
                      <SelectItem value="M30">M30</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label>Steel Grade</Label>
                  <Select defaultValue="Fe415">
                    <SelectTrigger><SelectValue /></SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Fe415">Fe415</SelectItem>
                      <SelectItem value="Fe500">Fe500</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
              <DialogFooter>
                <Button type="button" variant="outline" onClick={onClose}>Cancel</Button>
                <Button type="submit" disabled={loading}>{loading ? 'Designing...' : 'Design Two-Way Slab'}</Button>
              </DialogFooter>
            </form>
          </TabsContent>
          <TabsContent value="flat">
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="slab_thickness">Slab Thickness (mm)</Label>
                  <Input id="slab_thickness" type="number" defaultValue="200" />
                </div>
                <div>
                  <Label htmlFor="column_size">Column Size (mm)</Label>
                  <Input id="column_size" type="number" defaultValue="400" />
                </div>
                <div>
                  <Label htmlFor="drop_panel">Drop Panel (mm)</Label>
                  <Input id="drop_panel" type="number" defaultValue="100" />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="panel_lx">Panel Lx (m)</Label>
                  <Input id="panel_lx" type="number" step="0.1" defaultValue="6" />
                </div>
                <div>
                  <Label htmlFor="panel_ly">Panel Ly (m)</Label>
                  <Input id="panel_ly" type="number" step="0.1" defaultValue="6" />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="dead_load_flat">Dead Load (kN/m²)</Label>
                  <Input id="dead_load_flat" type="number" step="0.1" defaultValue="2" />
                </div>
                <div>
                  <Label htmlFor="live_load_flat">Live Load (kN/m²)</Label>
                  <Input id="live_load_flat" type="number" step="0.1" defaultValue="4" />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="punching_load">Punching Load (kN)</Label>
                  <Input id="punching_load" type="number" defaultValue="1000" />
                </div>
                <div>
                  <Label>Check Punching Shear</Label>
                  <Select defaultValue="yes">
                    <SelectTrigger><SelectValue /></SelectTrigger>
                    <SelectContent>
                      <SelectItem value="yes">Yes</SelectItem>
                      <SelectItem value="no">No</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
              <DialogFooter>
                <Button type="button" variant="outline" onClick={onClose}>Cancel</Button>
                <Button type="submit" disabled={loading}>{loading ? 'Designing...' : 'Design Flat Slab'}</Button>
              </DialogFooter>
            </form>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
