'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { pushoverApi } from '@/lib/api';
import { useModelStore } from '@/stores/modelStore';
import { LineChart, TrendingUp } from 'lucide-react';

interface PushoverDialogProps {
  open: boolean;
  onClose: () => void;
}

export function PushoverDialog({ open, onClose }: PushoverDialogProps) {
  const { currentProject } = useModelStore();
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  
  const form = useForm({
    defaultValues: {
      load_pattern: 'uniform' as 'uniform' | 'triangular' | 'modal',
      target_displacement: 0.1,
      max_steps: 100,
      control_node: 1,
      convergence_tolerance: 0.001,
      load_increment: 0.01,
      min_increment: 0.001,
    },
  });

  const { register, handleSubmit, setValue } = form;

  const onSubmit = async (data: any) => {
    if (!currentProject) return;
    setLoading(true);
    setResult(null);
    try {
      const res = await pushoverApi.runPushover({
        model_id: currentProject.id,
        ...data,
      });
      setResult(res);
    } catch (error: any) {
      setResult({ error: error.message || 'Pushover analysis failed' });
    } finally {
      setLoading(false);
    }
  };

  const handleCapacityCurve = async () => {
    if (!currentProject) return;
    setLoading(true);
    try {
      const formData = form.getValues();
      const res = await pushoverApi.getCapacityCurve({
        model_id: currentProject.id,
        load_pattern: formData.load_pattern,
        target_displacement: formData.target_displacement,
        max_steps: formData.max_steps,
      });
      setResult({ ...result, capacity_curve: res });
    } catch (error) {
      console.error('Failed to get capacity curve:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePerformancePoint = async () => {
    if (!currentProject) return;
    setLoading(true);
    try {
      const formData = form.getValues();
      const res = await pushoverApi.getPerformancePoint({
        model_id: currentProject.id,
        load_pattern: formData.load_pattern,
        target_displacement: formData.target_displacement,
        max_steps: formData.max_steps,
      });
      setResult({ ...result, performance_point: res });
    } catch (error) {
      console.error('Failed to get performance point:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[700px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Pushover Analysis (Nonlinear Static)</DialogTitle>
        </DialogHeader>

        <Tabs defaultValue="setup">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="setup">Setup</TabsTrigger>
            <TabsTrigger value="capacity">Capacity Curve</TabsTrigger>
            <TabsTrigger value="performance">Performance Point</TabsTrigger>
          </TabsList>

          <TabsContent value="setup">
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>Load Pattern</Label>
                  <Select defaultValue="uniform" onValueChange={(v) => setValue('load_pattern', v as 'uniform' | 'triangular' | 'modal')}>
                    <SelectTrigger><SelectValue /></SelectTrigger>
                    <SelectContent>
                      <SelectItem value="uniform">Uniform</SelectItem>
                      <SelectItem value="triangular">Triangular</SelectItem>
                      <SelectItem value="modal">Modal (First Mode)</SelectItem>
                      <SelectItem value="code">Code-Based (IS 1893)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="control_node">Control Node ID</Label>
                  <Input id="control_node" type="number" {...register('control_node', { valueAsNumber: true })} />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="target_displacement">Target Disp (m)</Label>
                  <Input id="target_displacement" type="number" step="0.001" {...register('target_displacement', { valueAsNumber: true })} />
                </div>
                <div>
                  <Label htmlFor="max_steps">Max Steps</Label>
                  <Input id="max_steps" type="number" {...register('max_steps', { valueAsNumber: true })} />
                </div>
                <div>
                  <Label htmlFor="convergence_tolerance">Tolerance</Label>
                  <Input id="convergence_tolerance" type="number" step="0.0001" {...register('convergence_tolerance', { valueAsNumber: true })} />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="load_increment">Initial Load Increment</Label>
                  <Input id="load_increment" type="number" step="0.01" defaultValue="0.1" {...register('load_increment', { valueAsNumber: true })} />
                </div>
                <div>
                  <Label htmlFor="min_increment">Min Increment</Label>
                  <Input id="min_increment" type="number" step="0.001" defaultValue="0.01" {...register('min_increment', { valueAsNumber: true })} />
                </div>
              </div>

              {result && !result.error && (
                <Alert>
                  <TrendingUp className="h-4 w-4" />
                  <AlertDescription>
                    <div className="font-semibold mb-2">Analysis Complete</div>
                    <div className="text-sm space-y-1">
                      <div>Steps Completed: {result.steps_completed || 'N/A'}</div>
                      <div>Max Base Shear: {result.max_base_shear?.toFixed(2) || 'N/A'} kN</div>
                      <div>Ultimate Displacement: {result.ultimate_displacement?.toFixed(3) || 'N/A'} m</div>
                    </div>
                  </AlertDescription>
                </Alert>
              )}

              {result?.error && (
                <Alert variant="destructive">
                  <AlertDescription>{result.error}</AlertDescription>
                </Alert>
              )}

              <DialogFooter>
                <Button type="button" variant="outline" onClick={onClose}>Cancel</Button>
                <Button type="submit" disabled={loading}>{loading ? 'Running...' : 'Run Pushover'}</Button>
              </DialogFooter>
            </form>
          </TabsContent>

          <TabsContent value="capacity" className="space-y-4">
            <div className="p-4 bg-blue-50 rounded-lg">
              <div className="flex items-center gap-2 mb-3">
                <LineChart className="h-5 w-5 text-blue-600" />
                <h3 className="font-semibold">Capacity Curve (Base Shear vs Displacement)</h3>
              </div>
              <p className="text-sm text-gray-700 mb-4">
                The capacity curve shows the relationship between base shear and roof displacement, representing the structure's lateral load-resisting capacity.
              </p>
              
              {result?.capacity_curve ? (
                <div className="bg-white p-4 rounded border">
                  <div className="text-sm space-y-2">
                    <div className="grid grid-cols-2 gap-2">
                      <div>Yield Point: {result.capacity_curve.yield_displacement?.toFixed(3)} m</div>
                      <div>Yield Force: {result.capacity_curve.yield_force?.toFixed(2)} kN</div>
                      <div>Ultimate Point: {result.capacity_curve.ultimate_displacement?.toFixed(3)} m</div>
                      <div>Ultimate Force: {result.capacity_curve.ultimate_force?.toFixed(2)} kN</div>
                    </div>
                    <div className="mt-3 p-3 bg-gray-50 rounded">
                      <div className="font-medium mb-1">Ductility Ratio: {result.capacity_curve.ductility?.toFixed(2)}</div>
                      <div className="text-xs text-gray-600">μ = Δu / Δy</div>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="text-sm text-gray-500 text-center py-8">
                  Run pushover analysis first to generate capacity curve
                </div>
              )}
            </div>

            <DialogFooter>
              <Button type="button" variant="outline" onClick={onClose}>Close</Button>
              <Button onClick={handleCapacityCurve} disabled={loading || !result}>
                {loading ? 'Loading...' : 'Get Capacity Curve'}
              </Button>
            </DialogFooter>
          </TabsContent>

          <TabsContent value="performance" className="space-y-4">
            <div className="p-4 bg-green-50 rounded-lg">
              <div className="flex items-center gap-2 mb-3">
                <TrendingUp className="h-5 w-5 text-green-600" />
                <h3 className="font-semibold">Performance Point (Capacity-Demand)</h3>
              </div>
              <p className="text-sm text-gray-700 mb-4">
                The performance point is the intersection of the capacity curve and demand spectrum, representing the expected seismic performance.
              </p>

              {result?.performance_point ? (
                <div className="bg-white p-4 rounded border space-y-3">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <div className="text-xs text-gray-500">Displacement</div>
                      <div className="text-lg font-semibold">{result.performance_point.displacement?.toFixed(3)} m</div>
                    </div>
                    <div>
                      <div className="text-xs text-gray-500">Base Shear</div>
                      <div className="text-lg font-semibold">{result.performance_point.base_shear?.toFixed(2)} kN</div>
                    </div>
                    <div>
                      <div className="text-xs text-gray-500">Effective Period</div>
                      <div className="text-lg font-semibold">{result.performance_point.period?.toFixed(2)} s</div>
                    </div>
                    <div>
                      <div className="text-xs text-gray-500">Effective Damping</div>
                      <div className="text-lg font-semibold">{result.performance_point.damping?.toFixed(1)}%</div>
                    </div>
                  </div>

                  <div className="p-3 bg-blue-50 rounded">
                    <div className="font-medium mb-2">Performance Level</div>
                    <div className="text-sm">
                      {result.performance_point.level === 'IO' && '✓ Immediate Occupancy (IO)'}
                      {result.performance_point.level === 'LS' && '⚠ Life Safety (LS)'}
                      {result.performance_point.level === 'CP' && '⚠ Collapse Prevention (CP)'}
                    </div>
                  </div>
                </div>
              ) : (
                <div className="text-sm text-gray-500 text-center py-8">
                  Run pushover analysis and generate capacity curve first
                </div>
              )}
            </div>

            <DialogFooter>
              <Button type="button" variant="outline" onClick={onClose}>Close</Button>
              <Button onClick={handlePerformancePoint} disabled={loading || !result}>
                {loading ? 'Calculating...' : 'Calculate Performance Point'}
              </Button>
            </DialogFooter>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
