'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { parallelApi } from '@/lib/api';

interface ParallelAnalysisDialogProps {
  open: boolean;
  onClose: () => void;
}

export function ParallelAnalysisDialog({ open, onClose }: ParallelAnalysisDialogProps) {
  const [numCores, setNumCores] = useState('4');
  const [loading, setLoading] = useState(false);

  const handleRun = async () => {
    setLoading(true);
    try {
      await parallelApi.runBatchAnalysis({ model_ids: [1], analysis_type: 'linear', parallel: true });
      onClose();
    } catch (error) {
      console.error('Parallel analysis failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Parallel Analysis</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div><Label>Number of Cores</Label><Input type="number" value={numCores} onChange={(e) => setNumCores(e.target.value)} min="1" max="16" /></div>
          <p className="text-sm text-gray-500">Use multiple CPU cores for faster analysis</p>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button onClick={handleRun} disabled={loading}>Run Parallel</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
