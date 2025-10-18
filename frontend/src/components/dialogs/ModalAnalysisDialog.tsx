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
import { Waves, BarChart3, PieChart } from 'lucide-react';

interface ModalAnalysisDialogProps {
  open: boolean;
  onClose: () => void;
}

export function ModalAnalysisDialog({ open, onClose }: ModalAnalysisDialogProps) {
  const { currentProject } = useModelStore();
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const { register, handleSubmit, setValue } = useForm({
    defaultValues: {
      num_modes: 10,
      solver: 'subspace',
      convergence_tolerance: 0.0001,
      max_iterations: 100,
      frequency_shift: 0,
      mass_matrix_type: 'consistent',
    },
  });

  const onSubmit = async (data: any) => {
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
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[900px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Modal Analysis (Eigenvalue Problem)</DialogTitle>
        </DialogHeader>

        <Tabs defaultValue="setup">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="setup">Setup</TabsTrigger>
            <TabsTrigger value="modes">Mode Shapes</TabsTrigger>
            <TabsTrigger value="participation">Participation Factors</TabsTrigger>
          </TabsList>

          {/* SETUP TAB */}
          <TabsContent value="setup">
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div className="p-4 bg-blue-50 rounded-lg">
                <div className="flex items-center gap-2 mb-2">
                  <Waves className="h-5 w-5 text-blue-600" />
                  <h3 className="font-semibold">Modal Analysis</h3>
                </div>
                <p className="text-sm text-gray-700 mb-2">
                  Solves the eigenvalue problem: [K - ω²M]φ = 0
                </p>
                <ul className="text-sm text-gray-700 space-y-1 ml-4">
                  <li>• Natural frequencies (ω) and periods (T)</li>
                  <li>• Mode shapes (φ)</li>
                  <li>• Modal participation factors</li>
                  <li>• Effective modal mass</li>
                </ul>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="num_modes">Number of Modes</Label>
                  <Input
                    id="num_modes"
                    type="number"
                    {...register('num_modes', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label>Eigenvalue Solver</Label>
                  <Select
                    defaultValue="subspace"
                    onValueChange={(v) => setValue('solver', v)}
                  >
                    <SelectTrigger><SelectValue /></SelectTrigger>
                    <SelectContent>
                      <SelectItem value="subspace">Subspace Iteration</SelectItem>
                      <SelectItem value="lanczos">Lanczos</SelectItem>
                      <SelectItem value="arnoldi">Arnoldi</SelectItem>
                      <SelectItem value="jacobi">Jacobi</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="convergence_tolerance">Convergence Tolerance</Label>
                  <Input
                    id="convergence_tolerance"
                    type="number"
                    step="0.00001"
                    {...register('convergence_tolerance', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="max_iterations">Max Iterations</Label>
                  <Input
                    id="max_iterations"
                    type="number"
                    {...register('max_iterations', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="frequency_shift">Frequency Shift (Hz)</Label>
                  <Input
                    id="frequency_shift"
                    type="number"
                    step="0.1"
                    defaultValue="0"
                    {...register('frequency_shift', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label>Mass Matrix Type</Label>
                  <Select
                    defaultValue="consistent"
                    onValueChange={(v) => setValue('mass_matrix_type', v)}
                  >
                    <SelectTrigger><SelectValue /></SelectTrigger>
                    <SelectContent>
                      <SelectItem value="consistent">Consistent</SelectItem>
                      <SelectItem value="lumped">Lumped</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              {result && !result.error && (
                <Alert>
                  <Waves className="h-4 w-4" />
                  <AlertDescription>
                    <div className="font-semibold mb-2">Modal Analysis Complete</div>
                    <div className="text-sm space-y-1">
                      <div>Modes Extracted: {result.modes_extracted || result.num_modes}</div>
                      <div>First Mode Frequency: {result.first_frequency?.toFixed(3)} Hz</div>
                      <div>First Mode Period: {result.first_period?.toFixed(3)} s</div>
                      <div>Total Mass Participation: {result.total_mass_participation?.toFixed(1)}%</div>
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
                  {loading ? 'Running...' : 'Run Modal Analysis'}
                </Button>
              </DialogFooter>
            </form>
          </TabsContent>

          {/* MODE SHAPES TAB */}
          <TabsContent value="modes" className="space-y-4">
            <div className="p-4 bg-purple-50 rounded-lg">
              <div className="flex items-center gap-2 mb-3">
                <BarChart3 className="h-5 w-5 text-purple-600" />
                <h3 className="font-semibold">Mode Shapes & Frequencies</h3>
              </div>
              <p className="text-sm text-gray-700">
                Natural vibration modes showing deformed shapes at resonant frequencies
              </p>
            </div>

            {result?.modes ? (
              <div className="space-y-3">
                <div className="bg-white border rounded-lg overflow-hidden">
                  <div className="grid grid-cols-6 gap-2 p-3 bg-gray-50 font-semibold text-sm border-b">
                    <div>Mode</div>
                    <div>Frequency (Hz)</div>
                    <div>Period (s)</div>
                    <div>Type</div>
                    <div>Direction</div>
                    <div>Mass (%)</div>
                  </div>
                  <div className="max-h-96 overflow-y-auto">
                    {result.modes.map((mode: any, idx: number) => (
                      <div key={idx} className="grid grid-cols-6 gap-2 p-3 text-sm border-b hover:bg-gray-50">
                        <div className="font-medium">{idx + 1}</div>
                        <div>{mode.frequency?.toFixed(3)}</div>
                        <div>{mode.period?.toFixed(3)}</div>
                        <div className="text-xs">
                          {mode.type === 'translation' ? '→ Trans' : '↻ Rot'}
                        </div>
                        <div className="text-xs">{mode.direction || 'Mixed'}</div>
                        <div>{mode.mass_participation?.toFixed(1)}</div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-3">
                  <div className="p-3 bg-blue-50 rounded">
                    <div className="text-xs text-gray-600">Fundamental Period</div>
                    <div className="text-lg font-bold">{result.modes[0]?.period?.toFixed(3)} s</div>
                  </div>
                  <div className="p-3 bg-green-50 rounded">
                    <div className="text-xs text-gray-600">Fundamental Frequency</div>
                    <div className="text-lg font-bold">{result.modes[0]?.frequency?.toFixed(3)} Hz</div>
                  </div>
                  <div className="p-3 bg-purple-50 rounded">
                    <div className="text-xs text-gray-600">Modes Extracted</div>
                    <div className="text-lg font-bold">{result.modes.length}</div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-sm text-gray-500 text-center py-12">
                Run modal analysis first to view mode shapes
              </div>
            )}

            <DialogFooter>
              <Button type="button" variant="outline" onClick={onClose}>Close</Button>
            </DialogFooter>
          </TabsContent>

          {/* PARTICIPATION FACTORS TAB */}
          <TabsContent value="participation" className="space-y-4">
            <div className="p-4 bg-green-50 rounded-lg">
              <div className="flex items-center gap-2 mb-3">
                <PieChart className="h-5 w-5 text-green-600" />
                <h3 className="font-semibold">Modal Participation Factors</h3>
              </div>
              <p className="text-sm text-gray-700">
                Indicates how much each mode contributes to the total response in each direction
              </p>
            </div>

            {result?.participation ? (
              <div className="space-y-4">
                <div className="grid grid-cols-3 gap-4">
                  <div className="p-4 bg-white border rounded-lg">
                    <div className="text-sm text-gray-600 mb-2">X-Direction</div>
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Mass Participation:</span>
                        <span className="font-semibold">{result.participation.x_mass?.toFixed(1)}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-blue-600 h-2 rounded-full"
                          style={{ width: `${result.participation.x_mass}%` }}
                        />
                      </div>
                    </div>
                  </div>

                  <div className="p-4 bg-white border rounded-lg">
                    <div className="text-sm text-gray-600 mb-2">Y-Direction</div>
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Mass Participation:</span>
                        <span className="font-semibold">{result.participation.y_mass?.toFixed(1)}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-green-600 h-2 rounded-full"
                          style={{ width: `${result.participation.y_mass}%` }}
                        />
                      </div>
                    </div>
                  </div>

                  <div className="p-4 bg-white border rounded-lg">
                    <div className="text-sm text-gray-600 mb-2">Z-Direction</div>
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Mass Participation:</span>
                        <span className="font-semibold">{result.participation.z_mass?.toFixed(1)}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-purple-600 h-2 rounded-full"
                          style={{ width: `${result.participation.z_mass}%` }}
                        />
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-white border rounded-lg p-4">
                  <h4 className="font-semibold mb-3">Cumulative Mass Participation</h4>
                  <div className="space-y-2">
                    {result.modes?.slice(0, 10).map((mode: any, idx: number) => (
                      <div key={idx} className="flex items-center gap-3 text-sm">
                        <div className="w-16">Mode {idx + 1}</div>
                        <div className="flex-1 flex gap-2">
                          <div className="flex-1">
                            <div className="w-full bg-gray-200 rounded-full h-4">
                              <div
                                className="bg-gradient-to-r from-blue-500 to-purple-500 h-4 rounded-full flex items-center justify-end pr-2 text-xs text-white"
                                style={{ width: `${mode.cumulative_mass || (idx + 1) * 10}%` }}
                              >
                                {(mode.cumulative_mass || (idx + 1) * 10).toFixed(0)}%
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <Alert>
                  <AlertDescription>
                    <div className="font-medium mb-1">Code Requirements:</div>
                    <div className="text-sm">
                      • IS 1893: Minimum 90% mass participation required<br />
                      • ASCE 7: Minimum 90% mass participation in each direction<br />
                      • Current: {result.total_mass_participation?.toFixed(1)}% {result.total_mass_participation >= 90 ? '✓' : '✗'}
                    </div>
                  </AlertDescription>
                </Alert>
              </div>
            ) : (
              <div className="text-sm text-gray-500 text-center py-12">
                Run modal analysis first to view participation factors
              </div>
            )}

            <DialogFooter>
              <Button type="button" variant="outline" onClick={onClose}>Close</Button>
            </DialogFooter>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
