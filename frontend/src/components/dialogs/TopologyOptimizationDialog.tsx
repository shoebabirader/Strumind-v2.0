'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Slider } from '@/components/ui/slider';
import { generativeApi } from '@/lib/api';

interface TopologyOptimizationDialogProps {
  open: boolean;
  onClose: () => void;
}

export function TopologyOptimizationDialog({ open, onClose }: TopologyOptimizationDialogProps) {
  const [loading, setLoading] = useState(false);
  const [volumeFraction, setVolumeFraction] = useState([50]);

  const handleOptimize = async () => {
    setLoading(true);
    try {
      await generativeApi.topologyOptimization({
        design_space: {},
        loads: {},
        constraints: {},
        volume_fraction: volumeFraction[0] / 100,
      });
      onClose();
    } catch (error) {
      console.error('Topology optimization failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Topology Optimization</DialogTitle>
        </DialogHeader>

        <div className="space-y-6">
          <div>
            <Label>Volume Fraction: {volumeFraction[0]}%</Label>
            <Slider
              value={volumeFraction}
              onValueChange={setVolumeFraction}
              min={10}
              max={90}
              step={5}
              className="mt-2"
            />
            <p className="text-xs text-gray-500 mt-1">
              Target material volume as percentage of design space
            </p>
          </div>

          <div className="p-4 bg-purple-50 rounded-lg text-sm">
            <p className="font-medium mb-2">Optimization Method:</p>
            <ul className="space-y-1 text-gray-700">
              <li>• SIMP (Solid Isotropic Material with Penalization)</li>
              <li>• Iterative material removal</li>
              <li>• Stress-based optimization</li>
              <li>• Manufacturing constraints</li>
            </ul>
          </div>

          <div className="p-4 bg-yellow-50 rounded-lg text-sm text-gray-700">
            <p className="font-medium mb-1">⚠️ Note:</p>
            <p>Topology optimization may take several minutes depending on model complexity.</p>
          </div>
        </div>

        <DialogFooter>
          <Button type="button" variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <Button onClick={handleOptimize} disabled={loading}>
            {loading ? 'Optimizing...' : 'Run Optimization'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
