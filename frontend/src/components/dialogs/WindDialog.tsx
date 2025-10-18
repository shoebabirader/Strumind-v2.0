'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { windApi } from '@/lib/api';

interface WindDialogProps {
  open: boolean;
  onClose: () => void;
}

export function WindDialog({ open, onClose }: WindDialogProps) {
  const [loading, setLoading] = useState(false);
  const { register, handleSubmit, setValue } = useForm({
    defaultValues: {
      code: 'IS875',
      basic_wind_speed: 44,
      terrain_category: 2,
      structure_class: 'B',
      height: 10,
      zone: 'interior',
      building_width: 20,
      building_depth: 15,
      wind_direction: 0,
      method: 'static',
      drag_coefficient: 1.2,
      exposure_factor: 1.0,
      natural_frequency: 0.5,
      damping_ratio: 0.01,
      mode_shape: 'first',
      mass_per_height: 1000,
      response_type: 'along',
      gust_factor: 2.0,
      turbulence_intensity: 0.15,
    },
  });

  const onSubmit = async (data: any) => {
    setLoading(true);
    try {
      const result = await windApi.calculateDesignPressure(data);
      // SECURITY FIX: Don't log potentially sensitive result data
      console.log('Wind analysis completed successfully');
      onClose();
    } catch (error) {
      // SECURITY FIX: Sanitize error before logging
      const sanitizedError = error instanceof Error ? error.message.replace(/[\r\n]/g, ' ') : 'Unknown error';
      console.error('Wind analysis failed:', sanitizedError);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>Wind Analysis (IS 875)</DialogTitle>
        </DialogHeader>

        <Tabs defaultValue="pressure" className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="pressure">Design Pressure</TabsTrigger>
            <TabsTrigger value="forces">Wind Forces</TabsTrigger>
            <TabsTrigger value="dynamic">Dynamic Response</TabsTrigger>
          </TabsList>

          <TabsContent value="pressure">
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>Design Code</Label>
                  <Select defaultValue="IS875" onValueChange={(v) => setValue('code', v)}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="IS875">IS 875:2015</SelectItem>
                      <SelectItem value="ASCE7">ASCE 7-16</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label htmlFor="basic_wind_speed">Basic Wind Speed (m/s)</Label>
                  <Input
                    id="basic_wind_speed"
                    type="number"
                    {...register('basic_wind_speed', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>Terrain Category</Label>
                  <Select defaultValue="2" onValueChange={(v) => setValue('terrain_category', parseInt(v))}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="1">Category 1 (Exposed)</SelectItem>
                      <SelectItem value="2">Category 2 (Open)</SelectItem>
                      <SelectItem value="3">Category 3 (Urban)</SelectItem>
                      <SelectItem value="4">Category 4 (Dense)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label>Structure Class</Label>
                  <Select defaultValue="B" onValueChange={(v) => setValue('structure_class', v)}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="A">Class A (Low Risk)</SelectItem>
                      <SelectItem value="B">Class B (Normal)</SelectItem>
                      <SelectItem value="C">Class C (High Risk)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="height">Height (m)</Label>
                  <Input
                    id="height"
                    type="number"
                    step="0.1"
                    {...register('height', { valueAsNumber: true })}
                  />
                </div>

                <div>
                  <Label>Pressure Zone</Label>
                  <Select defaultValue="interior" onValueChange={(v) => setValue('zone', v)}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="corner">Corner</SelectItem>
                      <SelectItem value="edge">Edge</SelectItem>
                      <SelectItem value="interior">Interior</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <DialogFooter>
                <Button type="button" variant="outline" onClick={onClose}>
                  Cancel
                </Button>
                <Button type="submit" disabled={loading}>
                  {loading ? 'Calculating...' : 'Calculate Pressure'}
                </Button>
              </DialogFooter>
            </form>
          </TabsContent>

          <TabsContent value="forces">
            <form onSubmit={handleSubmit(async (data) => {
              setLoading(true);
              try {
                await windApi.calculateWindForces({
                  ...data,
                  building_width: data.building_width || 20,
                  building_depth: data.building_depth || 15,
                  building_height: data.height,
                });
                onClose();
              } catch (error) {
                console.error('Wind forces calculation failed:', error);
              } finally {
                setLoading(false);
              }
            })} className="space-y-4">
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="building_width">Building Width (m)</Label>
                  <Input
                    id="building_width"
                    type="number"
                    step="0.1"
                    defaultValue="20"
                    {...register('building_width', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="building_depth">Building Depth (m)</Label>
                  <Input
                    id="building_depth"
                    type="number"
                    step="0.1"
                    defaultValue="15"
                    {...register('building_depth', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="building_height_forces">Building Height (m)</Label>
                  <Input
                    id="building_height_forces"
                    type="number"
                    step="0.1"
                    {...register('height', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>Wind Direction</Label>
                  <Select defaultValue="0" onValueChange={(v) => setValue('wind_direction', parseInt(v))}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="0">0° (Along X)</SelectItem>
                      <SelectItem value="90">90° (Along Y)</SelectItem>
                      <SelectItem value="45">45° (Diagonal)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label>Force Coefficient Method</Label>
                  <Select defaultValue="static" onValueChange={(v) => setValue('method', v)}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="static">Static Method</SelectItem>
                      <SelectItem value="dynamic">Dynamic Method</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="drag_coefficient">Drag Coefficient (Cd)</Label>
                  <Input
                    id="drag_coefficient"
                    type="number"
                    step="0.1"
                    defaultValue="1.2"
                    {...register('drag_coefficient', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="exposure_factor">Exposure Factor (k2)</Label>
                  <Input
                    id="exposure_factor"
                    type="number"
                    step="0.01"
                    defaultValue="1.0"
                    {...register('exposure_factor', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <DialogFooter>
                <Button type="button" variant="outline" onClick={onClose}>
                  Cancel
                </Button>
                <Button type="submit" disabled={loading}>
                  {loading ? 'Calculating...' : 'Calculate Wind Forces'}
                </Button>
              </DialogFooter>
            </form>
          </TabsContent>

          <TabsContent value="dynamic">
            <form onSubmit={handleSubmit(async (data) => {
              setLoading(true);
              try {
                await windApi.calculateDynamicResponse({
                  ...data,
                  natural_frequency: data.natural_frequency || 0.5,
                  damping_ratio: data.damping_ratio || 0.01,
                  mode_shape: data.mode_shape || 'first',
                });
                onClose();
              } catch (error) {
                console.error('Dynamic response calculation failed:', error);
              } finally {
                setLoading(false);
              }
            })} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="natural_frequency">Natural Frequency (Hz)</Label>
                  <Input
                    id="natural_frequency"
                    type="number"
                    step="0.01"
                    defaultValue="0.5"
                    {...register('natural_frequency', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="damping_ratio_wind">Damping Ratio</Label>
                  <Input
                    id="damping_ratio_wind"
                    type="number"
                    step="0.001"
                    defaultValue="0.01"
                    {...register('damping_ratio', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="mass_per_height">Mass per Height (kg/m)</Label>
                  <Input
                    id="mass_per_height"
                    type="number"
                    defaultValue="10000"
                    {...register('mass_per_height', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label>Response Type</Label>
                  <Select defaultValue="along" onValueChange={(v) => setValue('response_type', v)}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="along">Along-Wind</SelectItem>
                      <SelectItem value="across">Across-Wind</SelectItem>
                      <SelectItem value="torsional">Torsional</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label>Mode Shape</Label>
                  <Select defaultValue="first" onValueChange={(v) => setValue('mode_shape', v)}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="first">First Mode</SelectItem>
                      <SelectItem value="second">Second Mode</SelectItem>
                      <SelectItem value="third">Third Mode</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="gust_factor">Gust Factor</Label>
                  <Input
                    id="gust_factor"
                    type="number"
                    step="0.1"
                    defaultValue="2.0"
                    {...register('gust_factor', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <div>
                <Label htmlFor="turbulence_intensity">Turbulence Intensity (%)</Label>
                <Input
                  id="turbulence_intensity"
                  type="number"
                  step="1"
                  defaultValue="15"
                  {...register('turbulence_intensity', { valueAsNumber: true })}
                />
              </div>

              <DialogFooter>
                <Button type="button" variant="outline" onClick={onClose}>
                  Cancel
                </Button>
                <Button type="submit" disabled={loading}>
                  {loading ? 'Calculating...' : 'Calculate Dynamic Response'}
                </Button>
              </DialogFooter>
            </form>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
