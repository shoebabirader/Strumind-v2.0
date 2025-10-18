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
    },
  });

  const onSubmit = async (data: any) => {
    setLoading(true);
    try {
      const result = await windApi.calculateDesignPressure(data);
      console.log('Wind analysis result:', result);
      onClose();
    } catch (error) {
      console.error('Wind analysis failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
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
            <div className="text-sm text-gray-500 p-4">
              Wind forces calculation - Configure design pressure first
            </div>
          </TabsContent>

          <TabsContent value="dynamic">
            <div className="text-sm text-gray-500 p-4">
              Dynamic wind response - Along-wind and across-wind analysis
            </div>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
