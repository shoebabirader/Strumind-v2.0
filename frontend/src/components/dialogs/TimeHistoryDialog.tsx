'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { advancedAnalysisApi } from '@/lib/api';
import { useModelStore } from '@/stores/modelStore';

interface TimeHistoryDialogProps {
  open: boolean;
  onClose: () => void;
}

export function TimeHistoryDialog({ open, onClose }: TimeHistoryDialogProps) {
  const { currentProject } = useModelStore();
  const [loading, setLoading] = useState(false);
  const [timeStep, setTimeStep] = useState('0.01');
  const [dampingRatio, setDampingRatio] = useState('0.05');

  const handleRun = async () => {
    if (!currentProject) return;
    setLoading(true);
    try {
      await advancedAnalysisApi.timeHistory({
        model_id: currentProject.id,
        ground_motion: [],
        time_step: parseFloat(timeStep),
        damping_ratio: parseFloat(dampingRatio),
      });
      onClose();
    } catch (error) {
      console.error('Time history analysis failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Time History Analysis</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <Label htmlFor="time_step">Time Step (s)</Label>
              <Input id="time_step" type="number" step="0.001" value={timeStep} onChange={(e) => setTimeStep(e.target.value)} />
            </div>
            <div>
              <Label htmlFor="damping_ratio">Damping Ratio</Label>
              <Input id="damping_ratio" type="number" step="0.01" value={dampingRatio} onChange={(e) => setDampingRatio(e.target.value)} />
            </div>
          </div>
        </div>
        <DialogFooter>
          <Button type="button" variant="outline" onClick={onClose}>Cancel</Button>
          <Button onClick={handleRun} disabled={loading}>{loading ? 'Running...' : 'Run Analysis'}</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
