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
import { advancedAnalysisApi } from '@/lib/api';
import { useModelStore } from '@/stores/modelStore';
import { Zap, Activity, TrendingUp } from 'lucide-react';

interface AdvancedAnalysisDialogProps {
  open: boolean;
  onClose: () => void;
}

export function AdvancedAnalysisDialog({ open, onClose }: AdvancedAnalysisDialogProps) {
  const { currentProject } = useModelStore();
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const bucklingForm = useForm({
    defaultValues: { num_modes: 5, include_geometric_stiffness: true, solver: 'lanczos' },
  });

  const geometricForm = useForm({
    defaultValues: { max_iterations: 50, tolerance: 0.001, load_factor: 1.0, update_method: 'full' },
  });

  const materialForm = useForm({
    defaultValues: { plasticity_model: 'von_mises', hardening: 'isotropic', max_iterations: 100 },
  });

  const handleBuckling = async (data: any) => {
    if (!currentProject) return;
    setLoading(true);
    setResult(null);
    try {
      const res = await advancedAnalysisApi.buckling({ model_id: currentProject.id, ...data });
      setResult(res);
    } catch (error: any) {
      setResult({ error: error.message || 'Buckling analysis failed' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[800px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Advanced Analysis Options</DialogTitle>
        </DialogHeader>

        <Tabs defaultValue="buckling">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="buckling">Buckling</TabsTrigger>
            <TabsTrigger value="geometric">Geometric NL</TabsTrigger>
            <TabsTrigger value="material">Material NL</TabsTrigger>
          </TabsList>

          {/* BUCKLING TAB */}
          <TabsContent value="buckling">
            <form onSubmit={bucklingForm.handleSubmit(handleBuckling)} className="space-y-4">
              <div className="p-4 bg-orange-50 rounded-lg">
                <div className="flex items-center gap-2 mb-2">
                  <Zap className="h-5 w-5 text-orange-600" />
                  <h3 className="font-semibold">Linear Buckling Analysis</h3>
                </div>
                <p className="text-sm text-gray-700">
                  Eigenvalue analysis to determine critical buckling loads and mode shapes
                </p>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="num_modes">Number of Modes</Label>
                  <Input id="num_modes" type="number" {...bucklingForm.register('num_modes', { valueAsNumber: true })} />
                </div>
                <div>
                  <Label>Solver Method</Label>
                  <Select defaultValue="lanczos" onValueChange={(v) => bucklingForm.setValue('solver', v)}>
                    <SelectTrigger><SelectValue /></SelectTrigger>
                    <SelectContent>
                      <SelectItem value="lanczos">Lanczos</SelectItem>
                      <SelectItem value="subspace">Subspace Iteration</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
              {result && !result.error && result.buckling_modes && (
                <div className="bg-white border rounded-lg p-4">
                  <h4 className="font-semibold mb-3">Buckling Modes</h4>
                  <div className="space-y-2">
                    {result.buckling_modes.slice(0, 5).map((mode: any, idx: number) => (
                      <div key={idx} className="grid grid-cols-3 gap-2 text-sm p-2 bg-gray-50 rounded">
                        <div>Mode {idx + 1}</div>
                        <div>Load Factor: {mode.load_factor?.toFixed(3)}</div>
                        <div>Critical Load: {mode.critical_load?.toFixed(0)} kN</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              {result?.error && <Alert variant="destructive"><AlertDescription>{result.error}</AlertDescription></Alert>}
              <DialogFooter>
                <Button type="button" variant="outline" onClick={onClose}>Cancel</Button>
                <Button type="submit" disabled={loading}>{loading ? 'Running...' : 'Run Buckling Analysis'}</Button>
              </DialogFooter>
            </form>
          </TabsContent>

          {/* GEOMETRIC NONLINEAR TAB */}
          <TabsContent value="geometric">
            <form onSubmit={geometricForm.handleSubmit(async (data) => {
              if (!currentProject) return;
              setLoading(true);
              try {
                await advancedAnalysisApi.geometricNonlinear({ model_id: currentProject.id, ...data });
                onClose();
              } catch (error) {
                console.error('Geometric nonlinear analysis failed:', error);
              } finally {
                setLoading(false);
              }
            })} className="space-y-4">
              <div className="p-4 bg-blue-50 rounded-lg">
                <div className="flex items-center gap-2 mb-2">
                  <Activity className="h-5 w-5 text-blue-600" />
                  <h3 className="font-semibold">Geometric Nonlinearity</h3>
                </div>
                <p className="text-sm text-gray-700">
                  Large displacement analysis with updated geometry at each iteration
                </p>
              </div>
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="max_iterations_geom">Max Iterations</Label>
                  <Input id="max_iterations_geom" type="number" {...geometricForm.register('max_iterations', { valueAsNumber: true })} />
                </div>
                <div>
                  <Label htmlFor="tolerance_geom">Tolerance</Label>
                  <Input id="tolerance_geom" type="number" step="0.0001" {...geometricForm.register('tolerance', { valueAsNumber: true })} />
                </div>
                <div>
                  <Label htmlFor="load_factor">Load Factor</Label>
                  <Input id="load_factor" type="number" step="0.1" {...geometricForm.register('load_factor', { valueAsNumber: true })} />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>Update Method</Label>
                  <Select defaultValue="full" onValueChange={(v) => geometricForm.setValue('update_method', v)}>
                    <SelectTrigger><SelectValue /></SelectTrigger>
                    <SelectContent>
                      <SelectItem value="full">Full Newton-Raphson</SelectItem>
                      <SelectItem value="modified">Modified Newton</SelectItem>
                      <SelectItem value="quasi">Quasi-Newton</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="load_steps_geom">Load Steps</Label>
                  <Input id="load_steps_geom" type="number" defaultValue="10" />
                </div>
              </div>
              <DialogFooter>
                <Button type="button" variant="outline" onClick={onClose}>Cancel</Button>
                <Button type="submit" disabled={loading}>{loading ? 'Running...' : 'Run Geometric NL'}</Button>
              </DialogFooter>
            </form>
          </TabsContent>

          {/* MATERIAL NONLINEAR TAB */}
          <TabsContent value="material">
            <form onSubmit={materialForm.handleSubmit(async (data) => {
              if (!currentProject) return;
              setLoading(true);
              try {
                await advancedAnalysisApi.materialNonlinear({ model_id: currentProject.id, ...data });
                onClose();
              } catch (error) {
                console.error('Material nonlinear analysis failed:', error);
              } finally {
                setLoading(false);
              }
            })} className="space-y-4">
              <div className="p-4 bg-purple-50 rounded-lg">
                <div className="flex items-center gap-2 mb-2">
                  <TrendingUp className="h-5 w-5 text-purple-600" />
                  <h3 className="font-semibold">Material Nonlinearity</h3>
                </div>
                <p className="text-sm text-gray-700">
                  Inelastic material behavior including plasticity and strain hardening
                </p>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>Plasticity Model</Label>
                  <Select defaultValue="von_mises" onValueChange={(v) => materialForm.setValue('plasticity_model', v)}>
                    <SelectTrigger><SelectValue /></SelectTrigger>
                    <SelectContent>
                      <SelectItem value="von_mises">Von Mises</SelectItem>
                      <SelectItem value="tresca">Tresca</SelectItem>
                      <SelectItem value="drucker_prager">Drucker-Prager</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label>Hardening Rule</Label>
                  <Select defaultValue="isotropic" onValueChange={(v) => materialForm.setValue('hardening', v)}>
                    <SelectTrigger><SelectValue /></SelectTrigger>
                    <SelectContent>
                      <SelectItem value="isotropic">Isotropic</SelectItem>
                      <SelectItem value="kinematic">Kinematic</SelectItem>
                      <SelectItem value="mixed">Mixed</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="max_iterations_mat">Max Iterations</Label>
                  <Input id="max_iterations_mat" type="number" {...materialForm.register('max_iterations', { valueAsNumber: true })} />
                </div>
                <div>
                  <Label htmlFor="tolerance_mat">Tolerance</Label>
                  <Input id="tolerance_mat" type="number" step="0.0001" defaultValue="0.001" />
                </div>
                <div>
                  <Label htmlFor="load_steps_mat">Load Steps</Label>
                  <Input id="load_steps_mat" type="number" defaultValue="20" />
                </div>
              </div>
              <DialogFooter>
                <Button type="button" variant="outline" onClick={onClose}>Cancel</Button>
                <Button type="submit" disabled={loading}>{loading ? 'Running...' : 'Run Material NL'}</Button>
              </DialogFooter>
            </form>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
