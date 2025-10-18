'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { seismicApi } from '@/lib/api';

interface SeismicDialogProps {
  open: boolean;
  onClose: () => void;
}

export function SeismicDialog({ open, onClose }: SeismicDialogProps) {
  const [loading, setLoading] = useState(false);
  const { register, handleSubmit, setValue, watch } = useForm({
    defaultValues: {
      code: 'IS1893',
      zone: 'III',
      importance_factor: 1.0,
      response_reduction_factor: 5.0,
      soil_type: 'II',
      time_period: 1.0,
      seismic_weight: 1000,
    },
  });

  const onSubmit = async (data: any) => {
    setLoading(true);
    try {
      const result = await seismicApi.calculateBaseShear(data);
      // SECURITY FIX: Don't log potentially sensitive result data
      console.log('Seismic analysis completed successfully');
      onClose();
    } catch (error) {
      // SECURITY FIX: Sanitize error before logging
      const sanitizedError = error instanceof Error ? error.message.replace(/[\r\n]/g, ' ') : 'Unknown error';
      console.error('Seismic analysis failed:', sanitizedError);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Seismic Analysis (IS 1893)</DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>Design Code</Label>
              <Select defaultValue="IS1893" onValueChange={(v) => setValue('code', v)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="IS1893">IS 1893:2016</SelectItem>
                  <SelectItem value="ASCE7">ASCE 7-16</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label>Seismic Zone</Label>
              <Select defaultValue="III" onValueChange={(v) => setValue('zone', v)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="II">Zone II</SelectItem>
                  <SelectItem value="III">Zone III</SelectItem>
                  <SelectItem value="IV">Zone IV</SelectItem>
                  <SelectItem value="V">Zone V</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="importance_factor">Importance Factor (I)</Label>
              <Input
                id="importance_factor"
                type="number"
                step="0.1"
                {...register('importance_factor', { valueAsNumber: true })}
              />
            </div>

            <div>
              <Label htmlFor="response_reduction_factor">Response Reduction (R)</Label>
              <Input
                id="response_reduction_factor"
                type="number"
                step="0.1"
                {...register('response_reduction_factor', { valueAsNumber: true })}
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label>Soil Type</Label>
              <Select defaultValue="II" onValueChange={(v) => setValue('soil_type', v)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="I">Type I (Rock)</SelectItem>
                  <SelectItem value="II">Type II (Medium)</SelectItem>
                  <SelectItem value="III">Type III (Soft)</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label htmlFor="time_period">Time Period (s)</Label>
              <Input
                id="time_period"
                type="number"
                step="0.01"
                {...register('time_period', { valueAsNumber: true })}
              />
            </div>
          </div>

          <div>
            <Label htmlFor="seismic_weight">Seismic Weight (kN)</Label>
            <Input
              id="seismic_weight"
              type="number"
              {...register('seismic_weight', { valueAsNumber: true })}
            />
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={onClose}>
              Cancel
            </Button>
            <Button type="submit" disabled={loading}>
              {loading ? 'Calculating...' : 'Calculate Base Shear'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
