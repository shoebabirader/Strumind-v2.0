'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { nonlinearApi } from '@/lib/api';

interface NonlinearDialogProps {
  open: boolean;
  onClose: () => void;
}

export function NonlinearDialog({ open, onClose }: NonlinearDialogProps) {
  const [loading, setLoading] = useState(false);

  const handleRun = async () => {
    setLoading(true);
    try {
      await nonlinearApi.runNewtonRaphson({ model_id: 1, max_iterations: 100, tolerance: 0.001, load_steps: 10 });
      onClose();
    } catch (error) {
      console.error('Nonlinear analysis failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>Nonlinear Analysis</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div><Label>Max Iterations</Label><Input type="number" defaultValue="100" /></div>
          <div><Label>Convergence Tolerance</Label><Input type="number" step="0.0001" defaultValue="0.001" /></div>
          <p className="text-sm text-gray-500">Material and geometric nonlinearity</p>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button onClick={handleRun} disabled={loading}>Run Analysis</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
