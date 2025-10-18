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
import { serviceabilityApi } from '@/lib/api';
import { CheckCircle2, XCircle, AlertTriangle } from 'lucide-react';

interface ServiceabilityDialogProps {
  open: boolean;
  onClose: () => void;
}

export function ServiceabilityDialog({ open, onClose }: ServiceabilityDialogProps) {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [activeTab, setActiveTab] = useState('deflection');

  // Deflection form
  const deflectionForm = useForm({
    defaultValues: {
      span: 6,
      deflection: 0.025,
      load_type: 'total',
      member_type: 'beam',
      support_condition: 'simply_supported',
    },
  });

  // Crack width form
  const crackForm = useForm({
    defaultValues: {
      stress: 200,
      cover: 40,
      bar_diameter: 16,
      bar_spacing: 150,
      concrete_grade: 25,
      exposure_class: 'moderate',
    },
  });

  // Vibration form
  const vibrationForm = useForm({
    defaultValues: {
      natural_frequency: 5.0,
      damping_ratio: 0.02,
      floor_type: 'office',
      span: 8,
      mass_per_area: 500,
    },
  });

  // Punching shear form
  const punchingForm = useForm({
    defaultValues: {
      column_size_x: 0.4,
      column_size_y: 0.4,
      slab_thickness: 0.2,
      effective_depth: 0.17,
      punching_load: 1000,
      concrete_grade: 25,
    },
  });

  const handleDeflectionCheck = async (data: any) => {
    setLoading(true);
    setResult(null);
    try {
      const res = await serviceabilityApi.checkDeflection(data);
      setResult({
        status: res.status || 'pass',
        actual: data.deflection,
        allowable: res.allowable_deflection || data.span / 250,
        ratio: res.deflection_ratio || (data.deflection / (data.span / 250)),
        message: res.message || `Deflection check ${res.status === 'pass' ? 'passed' : 'failed'}`,
      });
    } catch (error: any) {
      setResult({
        status: 'error',
        message: error.message || 'Deflection check failed',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleCrackCheck = async (data: any) => {
    setLoading(true);
    setResult(null);
    try {
      const res = await serviceabilityApi.checkCrackWidth(data);
      setResult({
        status: res.status || 'pass',
        actual: res.crack_width || 0.2,
        allowable: res.allowable_crack_width || 0.3,
        message: res.message || `Crack width check ${res.status === 'pass' ? 'passed' : 'failed'}`,
      });
    } catch (error: any) {
      setResult({
        status: 'error',
        message: error.message || 'Crack width check failed',
      });
    } finally {
      setLoading(false);
    }
  };

  const handleVibrationCheck = async (data: any) => {
    setLoading(true);
    setResult(null);
    try {
      const res = await serviceabilityApi.checkVibration(data);
      setResult({
        status: res.status || 'pass',
        frequency: data.natural_frequency,
        min_frequency: res.minimum_frequency || 4.0,
        message: res.message || `Vibration check ${res.status === 'pass' ? 'passed' : 'failed'}`,
      });
    } catch (error: any) {
      setResult({
        status: 'error',
        message: error.message || 'Vibration check failed',
      });
    } finally {
      setLoading(false);
    }
  };

  const handlePunchingCheck = async (data: any) => {
    setLoading(true);
    setResult(null);
    try {
      const res = await serviceabilityApi.checkPunchingShear(data);
      setResult({
        status: res.status || 'pass',
        actual_stress: res.punching_stress || 0.5,
        allowable_stress: res.allowable_stress || 1.5,
        utilization: res.utilization_ratio || 0.33,
        message: res.message || `Punching shear check ${res.status === 'pass' ? 'passed' : 'failed'}`,
      });
    } catch (error: any) {
      setResult({
        status: 'error',
        message: error.message || 'Punching shear check failed',
      });
    } finally {
      setLoading(false);
    }
  };

  const renderResult = () => {
    if (!result) return null;

    const getIcon = () => {
      if (result.status === 'pass') return <CheckCircle2 className="h-5 w-5 text-green-500" />;
      if (result.status === 'fail') return <XCircle className="h-5 w-5 text-red-500" />;
      return <AlertTriangle className="h-5 w-5 text-yellow-500" />;
    };

    const getVariant = () => {
      if (result.status === 'pass') return 'default';
      if (result.status === 'fail') return 'destructive';
      return 'default';
    };

    return (
      <Alert variant={getVariant()} className="mt-4">
        <div className="flex items-start gap-3">
          {getIcon()}
          <div className="flex-1">
            <AlertDescription>
              <div className="font-semibold mb-2">{result.message}</div>
              {result.actual !== undefined && (
                <div className="text-sm space-y-1">
                  <div>Actual: {result.actual.toFixed(3)} {activeTab === 'deflection' ? 'm' : activeTab === 'crack' ? 'mm' : activeTab === 'vibration' ? 'Hz' : 'MPa'}</div>
                  <div>Allowable: {result.allowable?.toFixed(3)} {activeTab === 'deflection' ? 'm' : activeTab === 'crack' ? 'mm' : activeTab === 'vibration' ? 'Hz' : 'MPa'}</div>
                  {result.ratio && <div>Ratio: {result.ratio.toFixed(2)}</div>}
                  {result.utilization && <div>Utilization: {(result.utilization * 100).toFixed(1)}%</div>}
                </div>
              )}
            </AlertDescription>
          </div>
        </div>
      </Alert>
    );
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[700px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Serviceability Checks (IS 456 / ACI 318)</DialogTitle>
        </DialogHeader>

        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="deflection">Deflection</TabsTrigger>
            <TabsTrigger value="crack">Crack Width</TabsTrigger>
            <TabsTrigger value="vibration">Vibration</TabsTrigger>
            <TabsTrigger value="punching">Punching</TabsTrigger>
          </TabsList>

          {/* DEFLECTION TAB */}
          <TabsContent value="deflection" className="space-y-4">
            <form onSubmit={deflectionForm.handleSubmit(handleDeflectionCheck)} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="span">Span (m)</Label>
                  <Input
                    id="span"
                    type="number"
                    step="0.1"
                    {...deflectionForm.register('span', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="deflection">Measured Deflection (m)</Label>
                  <Input
                    id="deflection"
                    type="number"
                    step="0.001"
                    {...deflectionForm.register('deflection', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>Member Type</Label>
                  <Select
                    defaultValue="beam"
                    onValueChange={(v) => deflectionForm.setValue('member_type', v)}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="beam">Beam</SelectItem>
                      <SelectItem value="slab">Slab</SelectItem>
                      <SelectItem value="cantilever">Cantilever</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label>Load Type</Label>
                  <Select
                    defaultValue="total"
                    onValueChange={(v) => deflectionForm.setValue('load_type', v)}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="total">Total Load</SelectItem>
                      <SelectItem value="live">Live Load Only</SelectItem>
                      <SelectItem value="dead">Dead Load Only</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div>
                <Label>Support Condition</Label>
                <Select
                  defaultValue="simply_supported"
                  onValueChange={(v) => deflectionForm.setValue('support_condition', v)}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="simply_supported">Simply Supported</SelectItem>
                    <SelectItem value="fixed">Fixed</SelectItem>
                    <SelectItem value="continuous">Continuous</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {renderResult()}

              <DialogFooter>
                <Button type="button" variant="outline" onClick={onClose}>
                  Cancel
                </Button>
                <Button type="submit" disabled={loading}>
                  {loading ? 'Checking...' : 'Check Deflection'}
                </Button>
              </DialogFooter>
            </form>
          </TabsContent>

          {/* CRACK WIDTH TAB */}
          <TabsContent value="crack" className="space-y-4">
            <form onSubmit={crackForm.handleSubmit(handleCrackCheck)} className="space-y-4">
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="stress">Steel Stress (MPa)</Label>
                  <Input
                    id="stress"
                    type="number"
                    {...crackForm.register('stress', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="cover">Cover (mm)</Label>
                  <Input
                    id="cover"
                    type="number"
                    {...crackForm.register('cover', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="bar_diameter">Bar Dia (mm)</Label>
                  <Input
                    id="bar_diameter"
                    type="number"
                    {...crackForm.register('bar_diameter', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="bar_spacing">Bar Spacing (mm)</Label>
                  <Input
                    id="bar_spacing"
                    type="number"
                    {...crackForm.register('bar_spacing', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="concrete_grade">Concrete Grade (MPa)</Label>
                  <Input
                    id="concrete_grade"
                    type="number"
                    {...crackForm.register('concrete_grade', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label>Exposure Class</Label>
                  <Select
                    defaultValue="moderate"
                    onValueChange={(v) => crackForm.setValue('exposure_class', v)}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="mild">Mild</SelectItem>
                      <SelectItem value="moderate">Moderate</SelectItem>
                      <SelectItem value="severe">Severe</SelectItem>
                      <SelectItem value="very_severe">Very Severe</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              {renderResult()}

              <DialogFooter>
                <Button type="button" variant="outline" onClick={onClose}>
                  Cancel
                </Button>
                <Button type="submit" disabled={loading}>
                  {loading ? 'Checking...' : 'Check Crack Width'}
                </Button>
              </DialogFooter>
            </form>
          </TabsContent>

          {/* VIBRATION TAB */}
          <TabsContent value="vibration" className="space-y-4">
            <form onSubmit={vibrationForm.handleSubmit(handleVibrationCheck)} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="natural_frequency">Natural Frequency (Hz)</Label>
                  <Input
                    id="natural_frequency"
                    type="number"
                    step="0.1"
                    {...vibrationForm.register('natural_frequency', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="damping_ratio">Damping Ratio</Label>
                  <Input
                    id="damping_ratio"
                    type="number"
                    step="0.01"
                    {...vibrationForm.register('damping_ratio', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="span_vib">Span (m)</Label>
                  <Input
                    id="span_vib"
                    type="number"
                    step="0.1"
                    {...vibrationForm.register('span', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="mass_per_area">Mass per Area (kg/m²)</Label>
                  <Input
                    id="mass_per_area"
                    type="number"
                    {...vibrationForm.register('mass_per_area', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <div>
                <Label>Floor Type</Label>
                <Select
                  defaultValue="office"
                  onValueChange={(v) => vibrationForm.setValue('floor_type', v)}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="office">Office</SelectItem>
                    <SelectItem value="residential">Residential</SelectItem>
                    <SelectItem value="hospital">Hospital/Laboratory</SelectItem>
                    <SelectItem value="workshop">Workshop</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {renderResult()}

              <DialogFooter>
                <Button type="button" variant="outline" onClick={onClose}>
                  Cancel
                </Button>
                <Button type="submit" disabled={loading}>
                  {loading ? 'Checking...' : 'Check Vibration'}
                </Button>
              </DialogFooter>
            </form>
          </TabsContent>

          {/* PUNCHING SHEAR TAB */}
          <TabsContent value="punching" className="space-y-4">
            <form onSubmit={punchingForm.handleSubmit(handlePunchingCheck)} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="column_size_x">Column Size X (m)</Label>
                  <Input
                    id="column_size_x"
                    type="number"
                    step="0.05"
                    {...punchingForm.register('column_size_x', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="column_size_y">Column Size Y (m)</Label>
                  <Input
                    id="column_size_y"
                    type="number"
                    step="0.05"
                    {...punchingForm.register('column_size_y', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="slab_thickness">Slab Thickness (m)</Label>
                  <Input
                    id="slab_thickness"
                    type="number"
                    step="0.01"
                    {...punchingForm.register('slab_thickness', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="effective_depth">Effective Depth (m)</Label>
                  <Input
                    id="effective_depth"
                    type="number"
                    step="0.01"
                    {...punchingForm.register('effective_depth', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="punching_load">Punching Load (kN)</Label>
                  <Input
                    id="punching_load"
                    type="number"
                    {...punchingForm.register('punching_load', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="concrete_grade_punch">Concrete Grade (MPa)</Label>
                  <Input
                    id="concrete_grade_punch"
                    type="number"
                    {...punchingForm.register('concrete_grade', { valueAsNumber: true })}
                  />
                </div>
              </div>

              {renderResult()}

              <DialogFooter>
                <Button type="button" variant="outline" onClick={onClose}>
                  Cancel
                </Button>
                <Button type="submit" disabled={loading}>
                  {loading ? 'Checking...' : 'Check Punching Shear'}
                </Button>
              </DialogFooter>
            </form>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
