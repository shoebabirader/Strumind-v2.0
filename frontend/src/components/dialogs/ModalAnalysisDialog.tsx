'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { dynamicAnalysisApi } from '@/lib/api';
import { useModelStore } from '@/stores/modelStore';

interface ModalAnalysisDialogProps {
  open: boolean;
  onClose: () => void;
}

export function ModalAnalysisDialog({ open, onClose }: ModalAnalysisDialogProps) {
  const { currentProject } = useModelStore();
  const [loading, setLoading] = useState(false);
  const [numModes, setNumModes] = useState('10');

  const handleRun = async () => {
    if (!currentProject) return;
    setLoading(true);
    try {
      await dynamicAnalysisApi.performModalAnalysis({ model_id: currentProject.id, num_modes: parseInt(numModes) });
      onClose();
    } catch (error) {
      console.error('Modal analysis failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader><DialogTitle>Modal Analysis</DialogTitle></DialogHeader>
        <div className="space-y-4">
          <div><Label htmlFor="num_modes">Number of Modes</Label><Input id="num_modes" type="number" value={numModes} onChange={(e) => setNumModes(e.target.value)} /></div>
          <div className="p-4 bg-blue-50 rounded-lg text-sm">
            <p className="font-medium mb-2">Modal Analysis will compute:</p>
            <ul className="space-y-1 text-gray-700">
              <li>• Natural frequencies</li>
              <li>• Mode shapes</li>
              <li>• Modal participation factors</li>
              <li>• Effective modal mass</li>
            </ul>
          </div>
        </div>
        <DialogFooter>
          <Button type="button" variant="outline" onClick={onClose}>Cancel</Button>
          <Button onClick={handleRun} disabled={loading}>{loading ? 'Running...' : 'Run Modal Analysis'}</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
