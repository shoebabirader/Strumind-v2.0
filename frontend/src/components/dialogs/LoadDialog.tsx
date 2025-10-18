'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useLoads } from '@/hooks/useLoads';
import { useModelStore } from '@/stores/modelStore';

interface LoadDialogProps {
  open: boolean;
  onClose: () => void;
}

export function LoadDialog({ open, onClose }: LoadDialogProps) {
  const { currentProject } = useModelStore();
  const { createLoad } = useLoads(currentProject?.id);
  const [loading, setLoading] = useState(false);
  const [loadType, setLoadType] = useState<'nodal' | 'element'>('nodal');
  
  const { register, handleSubmit, setValue } = useForm({
    defaultValues: {
      load_case: 'dead',
      node_id: 0,
      element_id: 0,
      fx: 0,
      fy: 0,
      fz: 0,
      mx: 0,
      my: 0,
      mz: 0,
      w1: 0,
      w2: 0,
      direction: 'y',
    },
  });

  const onSubmit = async (data: any) => {
    if (!currentProject) return;

    setLoading(true);
    try {
      await createLoad({
        ...data,
        project_id: currentProject.id,
        load_type: loadType,
      });
      onClose();
    } catch (error) {
      console.error('Failed to create load:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>Apply Load</DialogTitle>
        </DialogHeader>

        <Tabs value={loadType} onValueChange={(v) => setLoadType(v as any)}>
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="nodal">Nodal Load</TabsTrigger>
            <TabsTrigger value="element">Element Load</TabsTrigger>
          </TabsList>

          <TabsContent value="nodal">
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="node_id">Node ID</Label>
                  <Input
                    id="node_id"
                    type="number"
                    {...register('node_id', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label>Load Case</Label>
                  <Select defaultValue="dead" onValueChange={(v) => setValue('load_case', v)}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="dead">Dead Load</SelectItem>
                      <SelectItem value="live">Live Load</SelectItem>
                      <SelectItem value="wind">Wind Load</SelectItem>
                      <SelectItem value="seismic">Seismic Load</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="fx">Fx (kN)</Label>
                  <Input
                    id="fx"
                    type="number"
                    step="0.01"
                    {...register('fx', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="fy">Fy (kN)</Label>
                  <Input
                    id="fy"
                    type="number"
                    step="0.01"
                    {...register('fy', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="fz">Fz (kN)</Label>
                  <Input
                    id="fz"
                    type="number"
                    step="0.01"
                    {...register('fz', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="mx">Mx (kNm)</Label>
                  <Input
                    id="mx"
                    type="number"
                    step="0.01"
                    {...register('mx', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="my">My (kNm)</Label>
                  <Input
                    id="my"
                    type="number"
                    step="0.01"
                    {...register('my', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="mz">Mz (kNm)</Label>
                  <Input
                    id="mz"
                    type="number"
                    step="0.01"
                    {...register('mz', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <DialogFooter>
                <Button type="button" variant="outline" onClick={onClose}>
                  Cancel
                </Button>
                <Button type="submit" disabled={loading}>
                  {loading ? 'Applying...' : 'Apply Load'}
                </Button>
              </DialogFooter>
            </form>
          </TabsContent>

          <TabsContent value="element">
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="element_id">Element ID</Label>
                  <Input
                    id="element_id"
                    type="number"
                    {...register('element_id', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label>Load Case</Label>
                  <Select defaultValue="dead" onValueChange={(v) => setValue('load_case', v)}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="dead">Dead Load</SelectItem>
                      <SelectItem value="live">Live Load</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="w1">W1 (kN/m)</Label>
                  <Input
                    id="w1"
                    type="number"
                    step="0.01"
                    {...register('w1', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="w2">W2 (kN/m)</Label>
                  <Input
                    id="w2"
                    type="number"
                    step="0.01"
                    {...register('w2', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label>Direction</Label>
                  <Select defaultValue="y" onValueChange={(v) => setValue('direction', v)}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="x">X</SelectItem>
                      <SelectItem value="y">Y</SelectItem>
                      <SelectItem value="z">Z</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <DialogFooter>
                <Button type="button" variant="outline" onClick={onClose}>
                  Cancel
                </Button>
                <Button type="submit" disabled={loading}>
                  {loading ? 'Applying...' : 'Apply Load'}
                </Button>
              </DialogFooter>
            </form>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
