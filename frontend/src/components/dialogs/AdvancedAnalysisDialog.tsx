'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { advancedAnalysisApi } from '@/lib/api';

interface AdvancedAnalysisDialogProps {
  open: boolean;
  onClose: () => void;
}

export function AdvancedAnalysisDialog({ open, onClose }: AdvancedAnalysisDialogProps) {
  const [loading, setLoading] = useState(false);

  const handleRun = async () => {
    setLoading(true);
    try {
      await advancedAnalysisApi.buckling({ model_id: 1, num_modes: 5 });
      onClose();
    } catch (error) {
      console.error('Advanced analysis failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[700px]">
        <DialogHeader>
          <DialogTitle>Advanced Analysis</DialogTitle>
        </DialogHeader>
        <Tabs defaultValue="pdelta">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="pdelta">P-Delta</TabsTrigger>
            <TabsTrigger value="buckling">Buckling</TabsTrigger>
            <TabsTrigger value="nonlinear">Nonlinear</TabsTrigger>
            <TabsTrigger value="pushover">Pushover</TabsTrigger>
          </TabsList>
          <TabsContent value="pdelta" className="space-y-4">
            <p className="text-sm">P-Delta analysis considers geometric nonlinearity</p>
          </TabsContent>
        </Tabs>
        <DialogFooter>
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button onClick={handleRun} disabled={loading}>Run Analysis</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
