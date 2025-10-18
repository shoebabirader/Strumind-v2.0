'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { pushoverApi } from '@/lib/api';
import { useModelStore } from '@/stores/modelStore';

interface PushoverDialogProps {
  open: boolean;
  onClose: () => void;
}

export function PushoverDialog({ open, onClose }: PushoverDialogProps) {
  const { currentProject } = useModelStore();
  const [loading, setLoading] = useState(false);
  const { register, handleSubmit, setValue } = useForm({
    defaultValues: {
      load_pattern: 'uniform',
      target_displacement: 0.1,
      max_steps: 100,
    },
  });

  const onSubmit = async (data: any) => {
    if (!currentProject) return;
    setLoading(true);
    try {
      await pushoverApi.runPushover({
        model_id: currentProject.id,
        ...data,
      });
      onClose();
    } catch (error) {
      console.error('Pushover analysis failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Pushover Analysis</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <Label>Load Pattern</Label>
            <Select defaultValue="uniform" onValueChange={(v) => setValue('load_pattern', v)}>
              <SelectTrigger><SelectValue /></SelectTrigger>
              <SelectContent>
                <SelectItem value="uniform">Uniform</SelectItem>
                <SelectItem value="triangular">Triangular</SelectItem>
                <SelectItem value="modal">Modal</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="target_displacement">Target Displacement (m)</Label>
              <Input id="target_displacement" type="number" step="0.001" {...register('target_displacement', { valueAsNumber: true })} />
            </div>
            <div>
              <Label htmlFor="max_steps">Max Steps</Label>
              <Input id="max_steps" type="number" {...register('max_steps', { valueAsNumber: true })} />
            </div>
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={onClose}>Cancel</Button>
            <Button type="submit" disabled={loading}>{loading ? 'Running...' : 'Run Pushover'}</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
