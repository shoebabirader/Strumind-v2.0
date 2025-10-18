'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { optimizationApi } from '@/lib/api';

interface OptimizationDialogProps {
  open: boolean;
  onClose: () => void;
}

export function OptimizationDialog({ open, onClose }: OptimizationDialogProps) {
  const [loading, setLoading] = useState(false);
  const { register, handleSubmit, setValue } = useForm({
    defaultValues: {
      span: 6,
      dead_load: 10,
      live_load: 5,
      objective: 'cost',
      max_depth: 600,
      min_width: 200,
    },
  });

  const onSubmit = async (data: any) => {
    setLoading(true);
    try {
      const result = await optimizationApi.beamSection({
        span: data.span,
        loads: {
          dead: data.dead_load,
          live: data.live_load,
        },
        constraints: {
          max_depth: data.max_depth,
          min_width: data.min_width,
        },
        objective: data.objective,
      });
      // SECURITY FIX: Don't log potentially sensitive result data
      console.log('Optimization completed successfully');
      onClose();
    } catch (error) {
      // SECURITY FIX: Sanitize error before logging
      const sanitizedError = error instanceof Error ? error.message.replace(/[\r\n]/g, ' ') : 'Unknown error';
      console.error('Optimization failed:', sanitizedError);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>Structural Optimization</DialogTitle>
        </DialogHeader>

        <Tabs defaultValue="beam">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="beam">Beam</TabsTrigger>
            <TabsTrigger value="column">Column</TabsTrigger>
            <TabsTrigger value="multi">Multi-Objective</TabsTrigger>
          </TabsList>

          <TabsContent value="beam">
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="span">Span (m)</Label>
                  <Input
                    id="span"
                    type="number"
                    step="0.1"
                    {...register('span', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label>Optimization Objective</Label>
                  <Select defaultValue="cost" onValueChange={(v) => setValue('objective', v)}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="cost">Minimize Cost</SelectItem>
                      <SelectItem value="weight">Minimize Weight</SelectItem>
                      <SelectItem value="carbon">Minimize Carbon</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="dead_load">Dead Load (kN/m)</Label>
                  <Input
                    id="dead_load"
                    type="number"
                    step="0.1"
                    {...register('dead_load', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="live_load">Live Load (kN/m)</Label>
                  <Input
                    id="live_load"
                    type="number"
                    step="0.1"
                    {...register('live_load', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="max_depth">Max Depth (mm)</Label>
                  <Input
                    id="max_depth"
                    type="number"
                    {...register('max_depth', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="min_width">Min Width (mm)</Label>
                  <Input
                    id="min_width"
                    type="number"
                    {...register('min_width', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <div className="p-4 bg-green-50 rounded-lg text-sm">
                <p className="font-medium mb-2">Optimization Features:</p>
                <ul className="space-y-1 text-gray-700">
                  <li>• Genetic algorithm optimization</li>
                  <li>• Code compliance constraints</li>
                  <li>• Multiple objectives support</li>
                  <li>• Pareto optimal solutions</li>
                </ul>
              </div>

              <DialogFooter>
                <Button type="button" variant="outline" onClick={onClose}>
                  Cancel
                </Button>
                <Button type="submit" disabled={loading}>
                  {loading ? 'Optimizing...' : 'Run Optimization'}
                </Button>
              </DialogFooter>
            </form>
          </TabsContent>

          <TabsContent value="column">
            <div className="text-sm text-gray-500 p-4">
              Column optimization - Configure loads and constraints
            </div>
          </TabsContent>

          <TabsContent value="multi">
            <div className="text-sm text-gray-500 p-4">
              Multi-objective optimization - Balance multiple criteria
            </div>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
