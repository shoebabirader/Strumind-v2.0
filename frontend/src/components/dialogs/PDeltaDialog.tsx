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
import { pdeltaApi } from '@/lib/api';
import { useModelStore } from '@/stores/modelStore';
import { AlertTriangle, TrendingUp, CheckCircle2 } from 'lucide-react';

interface PDeltaDialogProps {
  open: boolean;
  onClose: () => void;
}

export function PDeltaDialog({ open, onClose }: PDeltaDialogProps) {
  const { currentProject } = useModelStore();
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  
  const form = useForm({
    defaultValues: {
      load_case: 'dead+live',
      max_iterations: 10,
      convergence_tolerance: 0.001,
      include_geometric_stiffness: true,
      method: 'iterative',
      load_factor: 1.0,
      displacement_factor: 1.0,
      story_shear: 1000,
      story_weight: 5000,
      story_drift: 0.01,
      story_height: 3.5,
    },
  });

  const { register, handleSubmit, setValue } = form;

  const onSubmit = async (data: any) => {
    if (!currentProject) return;
    setLoading(true);
    setResult(null);
    try {
      const res = await pdeltaApi.runAnalysis({
        model_id: currentProject.id,
        ...data,
      });
      setResult(res);
    } catch (error: any) {
      setResult({ error: error.message || 'P-Delta analysis failed' });
    } finally {
      setLoading(false);
    }
  };

  const handleStabilityIndex = async () => {
    if (!currentProject) return;
    setLoading(true);
    try {
      const formData = form.getValues();
      const res = await pdeltaApi.calculateStabilityIndex({
        story_shear: formData.story_shear,
        story_weight: formData.story_weight,
        story_drift: formData.story_drift,
        story_height: formData.story_height,
      });
      setResult({ ...result, stability: res });
    } catch (error) {
      console.error('Failed to calculate stability index:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleMomentAmplification = async () => {
    if (!currentProject) return;
    setLoading(true);
    try {
      const res = await pdeltaApi.momentAmplification(1000, 5000, 1.0);
      setResult({ ...result, amplification: res });
    } catch (error) {
      console.error('Failed to calculate moment amplification:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[700px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>P-Delta Analysis (Second-Order Effects)</DialogTitle>
        </DialogHeader>

        <Tabs defaultValue="setup">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="setup">Setup</TabsTrigger>
            <TabsTrigger value="stability">Stability Index</TabsTrigger>
            <TabsTrigger value="amplification">Moment Amplification</TabsTrigger>
          </TabsList>

          <TabsContent value="setup">
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div className="p-4 bg-yellow-50 rounded-lg text-sm">
                <div className="flex items-center gap-2 mb-2">
                  <AlertTriangle className="h-4 w-4 text-yellow-600" />
                  <p className="font-medium">P-Delta Effects Include:</p>
                </div>
                <ul className="space-y-1 text-gray-700 ml-6">
                  <li>• Geometric nonlinearity due to axial loads</li>
                  <li>• Second-order moments and deflections</li>
                  <li>• Stability and buckling considerations</li>
                  <li>• Amplification of lateral displacements</li>
                </ul>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="load_case">Load Combination</Label>
                  <Input id="load_case" {...register('load_case')} placeholder="e.g., 1.2D + 1.6L" />
                </div>
                <div>
                  <Label htmlFor="max_iterations">Max Iterations</Label>
                  <Input id="max_iterations" type="number" {...register('max_iterations', { valueAsNumber: true })} />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="convergence_tolerance">Convergence Tolerance</Label>
                  <Input id="convergence_tolerance" type="number" step="0.0001" {...register('convergence_tolerance', { valueAsNumber: true })} />
                </div>
                <div>
                  <Label>Analysis Method</Label>
                  <Select defaultValue="iterative" onValueChange={(v) => setValue('method', v)}>
                    <SelectTrigger><SelectValue /></SelectTrigger>
                    <SelectContent>
                      <SelectItem value="iterative">Iterative</SelectItem>
                      <SelectItem value="direct">Direct Stiffness</SelectItem>
                      <SelectItem value="geometric">Geometric Stiffness Matrix</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="load_factor">Load Factor</Label>
                  <Input id="load_factor" type="number" step="0.1" defaultValue="1.0" {...register('load_factor', { valueAsNumber: true })} />
                </div>
                <div>
                  <Label htmlFor="displacement_factor">Displacement Factor</Label>
                  <Input id="displacement_factor" type="number" step="0.1" defaultValue="1.0" {...register('displacement_factor', { valueAsNumber: true })} />
                </div>
              </div>

              {result && !result.error && (
                <Alert>
                  <CheckCircle2 className="h-4 w-4" />
                  <AlertDescription>
                    <div className="font-semibold mb-2">P-Delta Analysis Complete</div>
                    <div className="text-sm space-y-1">
                      <div>Iterations: {result.iterations || 'N/A'}</div>
                      <div>Max Displacement Increase: {result.max_displacement_increase?.toFixed(1) || 'N/A'}%</div>
                      <div>Max Moment Increase: {result.max_moment_increase?.toFixed(1) || 'N/A'}%</div>
                      <div>Converged: {result.converged ? 'Yes' : 'No'}</div>
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
                <Button type="submit" disabled={loading}>{loading ? 'Running...' : 'Run P-Delta Analysis'}</Button>
              </DialogFooter>
            </form>
          </TabsContent>

          <TabsContent value="stability" className="space-y-4">
            <div className="p-4 bg-blue-50 rounded-lg">
              <div className="flex items-center gap-2 mb-3">
                <TrendingUp className="h-5 w-5 text-blue-600" />
                <h3 className="font-semibold">Stability Index (θ)</h3>
              </div>
              <p className="text-sm text-gray-700 mb-4">
                The stability index θ = (P × Δ) / (V × h) indicates the significance of P-Delta effects. 
                Values greater than 0.10 require P-Delta analysis.
              </p>

              {result?.stability ? (
                <div className="bg-white p-4 rounded border space-y-3">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <div className="text-xs text-gray-500">Stability Index (θ)</div>
                      <div className="text-2xl font-bold">{result.stability.theta?.toFixed(3)}</div>
                    </div>
                    <div>
                      <div className="text-xs text-gray-500">Status</div>
                      <div className={`text-lg font-semibold ${result.stability.theta > 0.10 ? 'text-red-600' : 'text-green-600'}`}>
                        {result.stability.theta > 0.10 ? 'Significant' : 'Acceptable'}
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-3 gap-3 text-sm">
                    <div className="p-2 bg-gray-50 rounded">
                      <div className="text-xs text-gray-500">Axial Load (P)</div>
                      <div className="font-semibold">{result.stability.axial_load?.toFixed(0)} kN</div>
                    </div>
                    <div className="p-2 bg-gray-50 rounded">
                      <div className="text-xs text-gray-500">Drift (Δ)</div>
                      <div className="font-semibold">{result.stability.drift?.toFixed(3)} m</div>
                    </div>
                    <div className="p-2 bg-gray-50 rounded">
                      <div className="text-xs text-gray-500">Story Shear (V)</div>
                      <div className="font-semibold">{result.stability.shear?.toFixed(0)} kN</div>
                    </div>
                  </div>

                  <div className={`p-3 rounded ${result.stability.theta > 0.10 ? 'bg-red-50' : 'bg-green-50'}`}>
                    <div className="font-medium mb-1">
                      {result.stability.theta > 0.10 ? '⚠ P-Delta Analysis Required' : '✓ P-Delta Effects Negligible'}
                    </div>
                    <div className="text-xs text-gray-600">
                      {result.stability.theta > 0.10 
                        ? 'θ > 0.10: Second-order effects are significant'
                        : 'θ ≤ 0.10: Second-order effects can be neglected'}
                    </div>
                  </div>
                </div>
              ) : (
                <div className="text-sm text-gray-500 text-center py-8">
                  Run P-Delta analysis first to calculate stability index
                </div>
              )}
            </div>

            <DialogFooter>
              <Button type="button" variant="outline" onClick={onClose}>Close</Button>
              <Button onClick={handleStabilityIndex} disabled={loading || !result}>
                {loading ? 'Calculating...' : 'Calculate Stability Index'}
              </Button>
            </DialogFooter>
          </TabsContent>

          <TabsContent value="amplification" className="space-y-4">
            <div className="p-4 bg-purple-50 rounded-lg">
              <div className="flex items-center gap-2 mb-3">
                <TrendingUp className="h-5 w-5 text-purple-600" />
                <h3 className="font-semibold">Moment Amplification Factors</h3>
              </div>
              <p className="text-sm text-gray-700 mb-4">
                Moment amplification factors account for P-Delta effects on member forces. 
                δ = 1 / (1 - θ) for non-sway frames, δ = 1 / (1 - Q) for sway frames.
              </p>

              {result?.amplification ? (
                <div className="bg-white p-4 rounded border space-y-3">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <div className="text-xs text-gray-500">Non-Sway Factor (δns)</div>
                      <div className="text-2xl font-bold">{result.amplification.delta_ns?.toFixed(3)}</div>
                    </div>
                    <div>
                      <div className="text-xs text-gray-500">Sway Factor (δs)</div>
                      <div className="text-2xl font-bold">{result.amplification.delta_s?.toFixed(3)}</div>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <div className="p-3 bg-gray-50 rounded">
                      <div className="text-sm font-medium mb-2">Amplified Moments:</div>
                      <div className="grid grid-cols-2 gap-2 text-sm">
                        <div>First-Order: {result.amplification.moment_first_order?.toFixed(2)} kNm</div>
                        <div>Second-Order: {result.amplification.moment_second_order?.toFixed(2)} kNm</div>
                        <div>Increase: {result.amplification.moment_increase?.toFixed(1)}%</div>
                        <div>Total: {result.amplification.moment_total?.toFixed(2)} kNm</div>
                      </div>
                    </div>

                    <div className="p-3 bg-blue-50 rounded text-sm">
                      <div className="font-medium mb-1">Design Moment:</div>
                      <div className="text-lg font-bold text-blue-700">
                        M = δns × Mns + δs × Ms = {result.amplification.design_moment?.toFixed(2)} kNm
                      </div>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="text-sm text-gray-500 text-center py-8">
                  Run P-Delta analysis first to calculate amplification factors
                </div>
              )}
            </div>

            <DialogFooter>
              <Button type="button" variant="outline" onClick={onClose}>Close</Button>
              <Button onClick={handleMomentAmplification} disabled={loading || !result}>
                {loading ? 'Calculating...' : 'Calculate Amplification'}
              </Button>
            </DialogFooter>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
