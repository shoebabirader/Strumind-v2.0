'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { advancedAnalysisApi } from '@/lib/api';
import { useModelStore } from '@/stores/modelStore';

interface BucklingDialogProps {
  open: boolean;
  onClose: () => void;
}

export function BucklingDialog({ open, onClose }: BucklingDialogProps) {
  const { currentProject } = useModelStore();
  const [loading, setLoading] = useState(false);
  const [numModes, setNumModes] = useState('5');

  const handleRun = async () => {
    if (!currentProject) return;
    setLoading(true);
    try {
      await advancedAnalysisApi.buckling({ model_id: currentProject.id, num_modes: parseInt(numModes) });
      onClose();
    } catch (error) {
      console.error('Buckling analysis failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader><DialogTitle>Buckling Analysis</DialogTitle></DialogHeader>
        <div className="space-y-4">
          <div><Label htmlFor="num_modes">Number of Buckling Modes</Label><Input id="num_modes" type="number" value={numModes} onChange={(e) => setNumModes(e.target.value)} /></div>
          <div className="p-4 bg-yellow-50 rounded-lg text-sm">
            <p className="font-medium mb-2">Buckling Analysis will compute:</p>
            <ul className="space-y-1 text-gray-700">
              <li>• Critical load factors</li>
              <li>• Buckling mode shapes</li>
              <li>• Stability assessment</li>
            </ul>
          </div>
        </div>
        <DialogFooter>
          <Button type="button" variant="outline" onClick={onClose}>Cancel</Button>
          <Button onClick={handleRun} disabled={loading}>{loading ? 'Running...' : 'Run Buckling Analysis'}</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
