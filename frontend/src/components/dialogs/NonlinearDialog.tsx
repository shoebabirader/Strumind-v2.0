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
import { Checkbox } from '@/components/ui/checkbox';
import { nonlinearApi } from '@/lib/api';
import { useModelStore } from '@/stores/modelStore';
import { TrendingUp, Settings, CheckCircle2 } from 'lucide-react';

interface NonlinearDialogProps {
  open: boolean;
  onClose: () => void;
}

export function NonlinearDialog({ open, onClose }: NonlinearDialogProps) {
  const { currentProject } = useModelStore();
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const { register, handleSubmit, setValue } = useForm({
    defaultValues: {
      method: 'newton_raphson',
      max_iterations: 100,
      tolerance: 0.001,
      load_steps: 10,
      include_geometric: true,
      include_material: true,
      line_search: true,
      min_load_step: 0.01,
      max_load_step: 0.1,
    },
  });

  const onSubmit = async (data: any) => {
    if (!currentProject) return;
    setLoading(true);
    setResult(null);
    try {
      const res = await nonlinearApi.runNewtonRaphson({
        model_id: currentProject.id,
        ...data,
      });
      setResult(res);
    } catch (error: any) {
      setResult({ error: error.message || 'Nonlinear analysis failed' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[800px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Nonlinear Analysis</DialogTitle>
        </DialogHeader>

        <Tabs defaultValue="setup">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="setup">Setup</TabsTrigger>
            <TabsTrigger value="material">Material Models</TabsTrigger>
            <TabsTrigger value="convergence">Convergence</TabsTrigger>
          </TabsList>

          {/* SETUP TAB */}
          <TabsContent value="setup">
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div className="p-4 bg-orange-50 rounded-lg">
                <div className="flex items-center gap-2 mb-2">
                  <TrendingUp className="h-5 w-5 text-orange-600" />
                  <h3 className="font-semibold">Nonlinear Analysis</h3>
                </div>
                <p className="text-sm text-gray-700 mb-2">
                  Accounts for material and/or geometric nonlinearity using iterative solution methods
                </p>
                <div className="flex gap-4 mt-3">
                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="include_geometric"
                      defaultChecked
                      onCheckedChange={(checked) => setValue('include_geometric', checked as boolean)}
                    />
                    <Label htmlFor="include_geometric" className="text-sm font-normal">
                      Geometric Nonlinearity (Large Displacements)
                    </Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="include_material"
                      defaultChecked
                      onCheckedChange={(checked) => setValue('include_material', checked as boolean)}
                    />
                    <Label htmlFor="include_material" className="text-sm font-normal">
                      Material Nonlinearity (Plasticity)
                    </Label>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>Solution Method</Label>
                  <Select
                    defaultValue="newton_raphson"
                    onValueChange={(v) => setValue('method', v)}
                  >
                    <SelectTrigger><SelectValue /></SelectTrigger>
                    <SelectContent>
                      <SelectItem value="newton_raphson">Newton-Raphson</SelectItem>
                      <SelectItem value="modified_newton">Modified Newton</SelectItem>
                      <SelectItem value="arc_length">Arc-Length</SelectItem>
                      <SelectItem value="displacement_control">Displacement Control</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="load_steps">Load Steps</Label>
                  <Input
                    id="load_steps"
                    type="number"
                    {...register('load_steps', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="max_iterations">Max Iterations</Label>
                  <Input
                    id="max_iterations"
                    type="number"
                    {...register('max_iterations', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="tolerance">Tolerance</Label>
                  <Input
                    id="tolerance"
                    type="number"
                    step="0.0001"
                    {...register('tolerance', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="line_search">Line Search Factor</Label>
                  <Input
                    id="line_search"
                    type="number"
                    step="0.1"
                    defaultValue="1.0"
                    {...register('line_search', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="min_load_step">Min Load Step</Label>
                  <Input
                    id="min_load_step"
                    type="number"
                    step="0.01"
                    defaultValue="0.01"
                    {...register('min_load_step', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="max_load_step">Max Load Step</Label>
                  <Input
                    id="max_load_step"
                    type="number"
                    step="0.1"
                    defaultValue="1.0"
                    {...register('max_load_step', { valueAsNumber: true })}
                  />
                </div>
              </div>

              {result && !result.error && (
                <Alert>
                  <CheckCircle2 className="h-4 w-4" />
                  <AlertDescription>
                    <div className="font-semibold mb-2">Nonlinear Analysis Complete</div>
                    <div className="text-sm space-y-1">
                      <div>Load Steps Completed: {result.steps_completed}/{result.total_steps}</div>
                      <div>Total Iterations: {result.total_iterations}</div>
                      <div>Avg Iterations/Step: {result.avg_iterations?.toFixed(1)}</div>
                      <div>Converged: {result.converged ? 'Yes ✓' : 'No ✗'}</div>
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
                <Button type="submit" disabled={loading}>
                  {loading ? 'Running...' : 'Run Nonlinear Analysis'}
                </Button>
              </DialogFooter>
            </form>
          </TabsContent>

          {/* MATERIAL MODELS TAB */}
          <TabsContent value="material" className="space-y-4">
            <div className="p-4 bg-purple-50 rounded-lg">
              <div className="flex items-center gap-2 mb-3">
                <Settings className="h-5 w-5 text-purple-600" />
                <h3 className="font-semibold">Material Constitutive Models</h3>
              </div>
              <p className="text-sm text-gray-700">
                Define nonlinear material behavior for concrete, steel, and other materials
              </p>
            </div>

            <div className="space-y-3">
              {/* Concrete Model */}
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold mb-3">Concrete Model</h4>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label>Concrete Model</Label>
                    <Select defaultValue="kent_park">
                      <SelectTrigger><SelectValue /></SelectTrigger>
                      <SelectContent>
                        <SelectItem value="kent_park">Kent-Park (Confined)</SelectItem>
                        <SelectItem value="mander">Mander Model</SelectItem>
                        <SelectItem value="hognestad">Hognestad Parabola</SelectItem>
                        <SelectItem value="popovics">Popovics Model</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label htmlFor="fc">Compressive Strength (MPa)</Label>
                    <Input id="fc" type="number" defaultValue="25" />
                  </div>
                  <div>
                    <Label htmlFor="ec">Elastic Modulus (GPa)</Label>
                    <Input id="ec" type="number" defaultValue="25" />
                  </div>
                  <div>
                    <Label htmlFor="strain_peak">Peak Strain</Label>
                    <Input id="strain_peak" type="number" step="0.0001" defaultValue="0.002" />
                  </div>
                </div>
              </div>

              {/* Steel Model */}
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold mb-3">Steel Model</h4>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label>Steel Model</Label>
                    <Select defaultValue="bilinear">
                      <SelectTrigger><SelectValue /></SelectTrigger>
                      <SelectContent>
                        <SelectItem value="bilinear">Bilinear (Elastic-Plastic)</SelectItem>
                        <SelectItem value="menegotto_pinto">Menegotto-Pinto</SelectItem>
                        <SelectItem value="ramberg_osgood">Ramberg-Osgood</SelectItem>
                        <SelectItem value="giuffre_menegotto">Giuffré-Menegotto-Pinto</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label htmlFor="fy">Yield Strength (MPa)</Label>
                    <Input id="fy" type="number" defaultValue="415" />
                  </div>
                  <div>
                    <Label htmlFor="es">Elastic Modulus (GPa)</Label>
                    <Input id="es" type="number" defaultValue="200" />
                  </div>
                  <div>
                    <Label htmlFor="hardening">Strain Hardening Ratio</Label>
                    <Input id="hardening" type="number" step="0.01" defaultValue="0.01" />
                  </div>
                </div>
              </div>

              {/* Plasticity Options */}
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold mb-3">Plasticity Options</h4>
                <div className="space-y-3">
                  <div className="flex items-center space-x-2">
                    <Checkbox id="kinematic_hardening" defaultChecked />
                    <Label htmlFor="kinematic_hardening" className="font-normal">
                      Kinematic Hardening (Bauschinger Effect)
                    </Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Checkbox id="isotropic_hardening" />
                    <Label htmlFor="isotropic_hardening" className="font-normal">
                      Isotropic Hardening
                    </Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Checkbox id="cyclic_degradation" />
                    <Label htmlFor="cyclic_degradation" className="font-normal">
                      Cyclic Strength Degradation
                    </Label>
                  </div>
                </div>
              </div>
            </div>

            <DialogFooter>
              <Button type="button" variant="outline" onClick={onClose}>Close</Button>
              <Button type="button">Apply Material Models</Button>
            </DialogFooter>
          </TabsContent>

          {/* CONVERGENCE TAB */}
          <TabsContent value="convergence" className="space-y-4">
            <div className="p-4 bg-green-50 rounded-lg">
              <div className="flex items-center gap-2 mb-3">
                <CheckCircle2 className="h-5 w-5 text-green-600" />
                <h3 className="font-semibold">Convergence Criteria & Settings</h3>
              </div>
              <p className="text-sm text-gray-700">
                Configure convergence checks and solution control parameters
              </p>
            </div>

            <div className="space-y-4">
              <div className="border rounded-lg p-4">
                <h4 className="font-semibold mb-3">Convergence Criteria</h4>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <Checkbox id="force_convergence" defaultChecked />
                      <Label htmlFor="force_convergence" className="font-normal">
                        Force Convergence
                      </Label>
                    </div>
                    <Input className="w-32" type="number" step="0.001" defaultValue="0.001" placeholder="Tolerance" />
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <Checkbox id="displacement_convergence" defaultChecked />
                      <Label htmlFor="displacement_convergence" className="font-normal">
                        Displacement Convergence
                      </Label>
                    </div>
                    <Input className="w-32" type="number" step="0.001" defaultValue="0.001" placeholder="Tolerance" />
                  </div>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <Checkbox id="energy_convergence" />
                      <Label htmlFor="energy_convergence" className="font-normal">
                        Energy Convergence
                      </Label>
                    </div>
                    <Input className="w-32" type="number" step="0.001" defaultValue="0.001" placeholder="Tolerance" />
                  </div>
                </div>
              </div>

              <div className="border rounded-lg p-4">
                <h4 className="font-semibold mb-3">Solution Control</h4>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="stiffness_update">Stiffness Update</Label>
                    <Select defaultValue="every_iteration">
                      <SelectTrigger><SelectValue /></SelectTrigger>
                      <SelectContent>
                        <SelectItem value="every_iteration">Every Iteration</SelectItem>
                        <SelectItem value="first_iteration">First Iteration Only</SelectItem>
                        <SelectItem value="every_n">Every N Iterations</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label htmlFor="bisection_tolerance">Bisection Tolerance</Label>
                    <Input id="bisection_tolerance" type="number" step="0.01" defaultValue="0.5" />
                  </div>
                  <div>
                    <Label htmlFor="max_bisections">Max Bisections</Label>
                    <Input id="max_bisections" type="number" defaultValue="5" />
                  </div>
                  <div>
                    <Label htmlFor="divergence_limit">Divergence Limit</Label>
                    <Input id="divergence_limit" type="number" defaultValue="1000" />
                  </div>
                </div>
              </div>

              <div className="border rounded-lg p-4">
                <h4 className="font-semibold mb-3">Advanced Options</h4>
                <div className="space-y-3">
                  <div className="flex items-center space-x-2">
                    <Checkbox id="auto_time_stepping" defaultChecked />
                    <Label htmlFor="auto_time_stepping" className="font-normal">
                      Automatic Time Stepping
                    </Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Checkbox id="line_search_enable" defaultChecked />
                    <Label htmlFor="line_search_enable" className="font-normal">
                      Enable Line Search
                    </Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Checkbox id="save_intermediate" />
                    <Label htmlFor="save_intermediate" className="font-normal">
                      Save Intermediate Results
                    </Label>
                  </div>
                </div>
              </div>
            </div>

            <DialogFooter>
              <Button type="button" variant="outline" onClick={onClose}>Close</Button>
              <Button type="button">Apply Settings</Button>
            </DialogFooter>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
