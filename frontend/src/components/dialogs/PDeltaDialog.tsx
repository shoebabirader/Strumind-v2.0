'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { pdeltaApi } from '@/lib/api';
import { useModelStore } from '@/stores/modelStore';

interface PDeltaDialogProps {
  open: boolean;
  onClose: () => void;
}

export function PDeltaDialog({ open, onClose }: PDeltaDialogProps) {
  const { currentProject } = useModelStore();
  const [loading, setLoading] = useState(false);
  const [loadCase, setLoadCase] = useState('dead+live');

  const handleRun = async () => {
    if (!currentProject) return;
    setLoading(true);
    try {
      await pdeltaApi.runAnalysis({
        model_id: currentProject.id,
        load_case: loadCase,
      });
      onClose();
    } catch (error) {
      console.error('P-Delta analysis failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>P-Delta Analysis</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div>
            <Label htmlFor="load_case">Load Case</Label>
            <Input id="load_case" value={loadCase} onChange={(e) => setLoadCase(e.target.value)} />
          </div>
          <div className="p-4 bg-yellow-50 rounded-lg text-sm">
            <p className="font-medium mb-2">P-Delta Effects:</p>
            <ul className="space-y-1 text-gray-700">
              <li>• Geometric nonlinearity</li>
              <li>• Second-order effects</li>
              <li>• Stability analysis</li>
            </ul>
          </div>
        </div>
        <DialogFooter>
          <Button type="button" variant="outline" onClick={onClose}>Cancel</Button>
          <Button onClick={handleRun} disabled={loading}>{loading ? 'Running...' : 'Run P-Delta'}</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
