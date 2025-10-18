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
import { dynamicAnalysisApi } from '@/lib/api';
import { useModelStore } from '@/stores/modelStore';
import { Activity, Waves, BarChart3 } from 'lucide-react';

interface DynamicAnalysisDialogProps {
  open: boolean;
  onClose: () => void;
}

export function DynamicAnalysisDialog({ open, onClose }: DynamicAnalysisDialogProps) {
  const { currentProject } = useModelStore();
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const timeHistoryForm = useForm({
    defaultValues: {
      time_step: 0.01,
      duration: 10,
      damping_ratio: 0.05,
      integration_method: 'newmark',
      ground_motion_file: '',
      newmark_beta: 0.25,
      newmark_gamma: 0.5,
    },
  });

  const responseSpectrumForm = useForm({
    defaultValues: {
      spectrum_type: 'design',
      damping_ratio: 0.05,
      scale_factor: 1.0,
      direction: 'x',
      combination_method: 'cqc',
      zone_factor: 0.16,
      importance_factor: 1.0,
    },
  });

  const modalForm = useForm({
    defaultValues: {
      num_modes: 10,
      frequency_range_min: 0,
      frequency_range_max: 100,
      convergence_tolerance: 0.0001,
      solver: 'lanczos',
    },
  });

  const handleTimeHistory = async (data: any) => {
    if (!currentProject) return;
    setLoading(true);
    setResult(null);
    try {
      const res = await dynamicAnalysisApi.runTimeHistory({
        model_id: currentProject.id,
        ...data,
      });
      setResult(res);
    } catch (error: any) {
      setResult({ error: error.message || 'Time history analysis failed' });
    } finally {
      setLoading(false);
    }
  };

  const handleResponseSpectrum = async (data: any) => {
    if (!currentProject) return;
    setLoading(true);
    setResult(null);
    try {
      const res = await dynamicAnalysisApi.runResponseSpectrum({
        model_id: currentProject.id,
        ...data,
      });
      setResult(res);
    } catch (error: any) {
      setResult({ error: error.message || 'Response spectrum analysis failed' });
    } finally {
      setLoading(false);
    }
  };

  const handleModal = async (data: any) => {
    if (!currentProject) return;
    setLoading(true);
    setResult(null);
    try {
      const res = await dynamicAnalysisApi.performModalAnalysis({
        model_id: currentProject.id,
        ...data,
      });
      setResult(res);
    } catch (error: any) {
      setResult({ error: error.message || 'Modal analysis failed' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[800px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Dynamic Analysis</DialogTitle>
        </DialogHeader>

        <Tabs defaultValue="timehistory">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="timehistory">Time History</TabsTrigger>
            <TabsTrigger value="response">Response Spectrum</TabsTrigger>
            <TabsTrigger value="modal">Modal Analysis</TabsTrigger>
          </TabsList>

          {/* TIME HISTORY TAB */}
          <TabsContent value="timehistory">
            <form onSubmit={timeHistoryForm.handleSubmit(handleTimeHistory)} className="space-y-4">
              <div className="p-4 bg-blue-50 rounded-lg">
                <div className="flex items-center gap-2 mb-2">
                  <Activity className="h-5 w-5 text-blue-600" />
                  <h3 className="font-semibold">Time History Analysis</h3>
                </div>
                <p className="text-sm text-gray-700">
                  Direct integration of equations of motion with time-varying loads (earthquakes, wind, etc.)
                </p>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="time_step">Time Step (s)</Label>
                  <Input
                    id="time_step"
                    type="number"
                    step="0.001"
                    {...timeHistoryForm.register('time_step', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="duration">Duration (s)</Label>
                  <Input
                    id="duration"
                    type="number"
                    {...timeHistoryForm.register('duration', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="damping_ratio_th">Damping Ratio</Label>
                  <Input
                    id="damping_ratio_th"
                    type="number"
                    step="0.01"
                    {...timeHistoryForm.register('damping_ratio', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>Integration Method</Label>
                  <Select
                    defaultValue="newmark"
                    onValueChange={(v) => timeHistoryForm.setValue('integration_method', v)}
                  >
                    <SelectTrigger><SelectValue /></SelectTrigger>
                    <SelectContent>
                      <SelectItem value="newmark">Newmark-β</SelectItem>
                      <SelectItem value="wilson">Wilson-θ</SelectItem>
                      <SelectItem value="central">Central Difference</SelectItem>
                      <SelectItem value="runge_kutta">Runge-Kutta</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="ground_motion_file">Ground Motion File</Label>
                  <Input
                    id="ground_motion_file"
                    {...timeHistoryForm.register('ground_motion_file')}
                    placeholder="earthquake.txt"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="newmark_beta">Newmark β</Label>
                  <Input
                    id="newmark_beta"
                    type="number"
                    step="0.01"
                    defaultValue="0.25"
                    {...timeHistoryForm.register('newmark_beta', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="newmark_gamma">Newmark γ</Label>
                  <Input
                    id="newmark_gamma"
                    type="number"
                    step="0.01"
                    defaultValue="0.5"
                    {...timeHistoryForm.register('newmark_gamma', { valueAsNumber: true })}
                  />
                </div>
              </div>

              {result && !result.error && (
                <Alert>
                  <Activity className="h-4 w-4" />
                  <AlertDescription>
                    <div className="font-semibold mb-2">Time History Complete</div>
                    <div className="text-sm space-y-1">
                      <div>Max Displacement: {result.max_displacement?.toFixed(3)} m</div>
                      <div>Max Velocity: {result.max_velocity?.toFixed(3)} m/s</div>
                      <div>Max Acceleration: {result.max_acceleration?.toFixed(2)} m/s²</div>
                      <div>Time Steps: {result.time_steps}</div>
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
                  {loading ? 'Running...' : 'Run Time History'}
                </Button>
              </DialogFooter>
            </form>
          </TabsContent>

          {/* RESPONSE SPECTRUM TAB */}
          <TabsContent value="response">
            <form onSubmit={responseSpectrumForm.handleSubmit(handleResponseSpectrum)} className="space-y-4">
              <div className="p-4 bg-purple-50 rounded-lg">
                <div className="flex items-center gap-2 mb-2">
                  <Waves className="h-5 w-5 text-purple-600" />
                  <h3 className="font-semibold">Response Spectrum Analysis</h3>
                </div>
                <p className="text-sm text-gray-700">
                  Modal superposition method using design or site-specific response spectra
                </p>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>Spectrum Type</Label>
                  <Select
                    defaultValue="design"
                    onValueChange={(v) => responseSpectrumForm.setValue('spectrum_type', v)}
                  >
                    <SelectTrigger><SelectValue /></SelectTrigger>
                    <SelectContent>
                      <SelectItem value="design">Design Spectrum (IS 1893)</SelectItem>
                      <SelectItem value="site_specific">Site-Specific</SelectItem>
                      <SelectItem value="user_defined">User-Defined</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="damping_ratio_rs">Damping Ratio</Label>
                  <Input
                    id="damping_ratio_rs"
                    type="number"
                    step="0.01"
                    {...responseSpectrumForm.register('damping_ratio', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="scale_factor">Scale Factor</Label>
                  <Input
                    id="scale_factor"
                    type="number"
                    step="0.1"
                    {...responseSpectrumForm.register('scale_factor', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label>Direction</Label>
                  <Select
                    defaultValue="x"
                    onValueChange={(v) => responseSpectrumForm.setValue('direction', v)}
                  >
                    <SelectTrigger><SelectValue /></SelectTrigger>
                    <SelectContent>
                      <SelectItem value="x">X Direction</SelectItem>
                      <SelectItem value="y">Y Direction</SelectItem>
                      <SelectItem value="z">Z Direction</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label>Combination Method</Label>
                  <Select
                    defaultValue="cqc"
                    onValueChange={(v) => responseSpectrumForm.setValue('combination_method', v)}
                  >
                    <SelectTrigger><SelectValue /></SelectTrigger>
                    <SelectContent>
                      <SelectItem value="cqc">CQC</SelectItem>
                      <SelectItem value="srss">SRSS</SelectItem>
                      <SelectItem value="abs">Absolute Sum</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="zone_factor">Zone Factor (Z)</Label>
                  <Input
                    id="zone_factor"
                    type="number"
                    step="0.01"
                    defaultValue="0.24"
                    {...responseSpectrumForm.register('zone_factor', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="importance_factor">Importance Factor (I)</Label>
                  <Input
                    id="importance_factor"
                    type="number"
                    step="0.1"
                    defaultValue="1.0"
                    {...responseSpectrumForm.register('importance_factor', { valueAsNumber: true })}
                  />
                </div>
              </div>

              {result && !result.error && (
                <Alert>
                  <Waves className="h-4 w-4" />
                  <AlertDescription>
                    <div className="font-semibold mb-2">Response Spectrum Complete</div>
                    <div className="text-sm space-y-1">
                      <div>Base Shear: {result.base_shear?.toFixed(2)} kN</div>
                      <div>Max Displacement: {result.max_displacement?.toFixed(3)} m</div>
                      <div>Modes Combined: {result.modes_combined}</div>
                      <div>Effective Mass Ratio: {result.effective_mass_ratio?.toFixed(1)}%</div>
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
                  {loading ? 'Running...' : 'Run Response Spectrum'}
                </Button>
              </DialogFooter>
            </form>
          </TabsContent>

          {/* MODAL ANALYSIS TAB */}
          <TabsContent value="modal">
            <form onSubmit={modalForm.handleSubmit(handleModal)} className="space-y-4">
              <div className="p-4 bg-green-50 rounded-lg">
                <div className="flex items-center gap-2 mb-2">
                  <BarChart3 className="h-5 w-5 text-green-600" />
                  <h3 className="font-semibold">Modal Analysis (Eigenvalue)</h3>
                </div>
                <p className="text-sm text-gray-700">
                  Extract natural frequencies, mode shapes, and participation factors
                </p>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="num_modes">Number of Modes</Label>
                  <Input
                    id="num_modes"
                    type="number"
                    {...modalForm.register('num_modes', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="convergence_tolerance">Convergence Tolerance</Label>
                  <Input
                    id="convergence_tolerance"
                    type="number"
                    step="0.0001"
                    {...modalForm.register('convergence_tolerance', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="frequency_range_min">Min Frequency (Hz)</Label>
                  <Input
                    id="frequency_range_min"
                    type="number"
                    step="0.1"
                    {...modalForm.register('frequency_range_min', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="frequency_range_max">Max Frequency (Hz)</Label>
                  <Input
                    id="frequency_range_max"
                    type="number"
                    {...modalForm.register('frequency_range_max', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <div>
                <Label>Eigenvalue Solver</Label>
                <Select
                  defaultValue="subspace"
                  onValueChange={(v) => modalForm.setValue('solver', v)}
                >
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="subspace">Subspace Iteration</SelectItem>
                    <SelectItem value="lanczos">Lanczos</SelectItem>
                    <SelectItem value="arnoldi">Arnoldi</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {result && !result.error && result.modes && (
                <div className="bg-white border rounded-lg p-4">
                  <h4 className="font-semibold mb-3">Modal Results</h4>
                  <div className="space-y-2 max-h-60 overflow-y-auto">
                    {result.modes.slice(0, 10).map((mode: any, idx: number) => (
                      <div key={idx} className="grid grid-cols-4 gap-2 text-sm p-2 bg-gray-50 rounded">
                        <div><span className="text-gray-500">Mode {idx + 1}:</span></div>
                        <div><span className="font-medium">{mode.frequency?.toFixed(3)} Hz</span></div>
                        <div><span className="text-gray-500">Period:</span> {mode.period?.toFixed(3)} s</div>
                        <div><span className="text-gray-500">Mass:</span> {mode.mass_participation?.toFixed(1)}%</div>
                      </div>
                    ))}
                  </div>
                  <div className="mt-3 p-3 bg-blue-50 rounded">
                    <div className="text-sm font-medium">
                      Total Mass Participation: {result.total_mass_participation?.toFixed(1)}%
                    </div>
                  </div>
                </div>
              )}

              {result?.error && (
                <Alert variant="destructive">
                  <AlertDescription>{result.error}</AlertDescription>
                </Alert>
              )}

              <DialogFooter>
                <Button type="button" variant="outline" onClick={onClose}>Cancel</Button>
                <Button type="submit" disabled={loading}>
                  {loading ? 'Running...' : 'Run Modal Analysis'}
                </Button>
              </DialogFooter>
            </form>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
