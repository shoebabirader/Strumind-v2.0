'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { dynamicAnalysisApi } from '@/lib/api';

interface DynamicAnalysisDialogProps {
  open: boolean;
  onClose: () => void;
}

export function DynamicAnalysisDialog({ open, onClose }: DynamicAnalysisDialogProps) {
  const [loading, setLoading] = useState(false);

  const handleRun = async () => {
    setLoading(true);
    try {
      await dynamicAnalysisApi.performModalAnalysis({ model_id: 1, num_modes: 10 });
      onClose();
    } catch (error) {
      console.error('Dynamic analysis failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[700px]">
        <DialogHeader>
          <DialogTitle>Dynamic Analysis</DialogTitle>
        </DialogHeader>
        <Tabs defaultValue="timehistory">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="timehistory">Time History</TabsTrigger>
            <TabsTrigger value="response">Response Spectrum</TabsTrigger>
            <TabsTrigger value="modal">Modal</TabsTrigger>
          </TabsList>
          <TabsContent value="timehistory" className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div><Label>Time Step (s)</Label><Input type="number" step="0.001" defaultValue="0.01" /></div>
              <div><Label>Duration (s)</Label><Input type="number" defaultValue="10" /></div>
              <div><Label>Damping Ratio</Label><Input type="number" step="0.01" defaultValue="0.05" /></div>
            </div>
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
