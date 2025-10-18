'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { resultsProcessingApi } from '@/lib/api';

interface ResultsProcessingDialogProps {
  open: boolean;
  onClose: () => void;
}

export function ResultsProcessingDialog({ open, onClose }: ResultsProcessingDialogProps) {
  const [loadCase, setLoadCase] = useState('DL');
  const [loading, setLoading] = useState(false);

  const handleProcess = async () => {
    setLoading(true);
    try {
      await resultsProcessingApi.momentDiagram({ element_id: 1, load_case: loadCase });
      onClose();
    } catch (error) {
      console.error('Results processing failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[700px]">
        <DialogHeader>
          <DialogTitle>Results Processing</DialogTitle>
        </DialogHeader>
        <Tabs defaultValue="stresses">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="stresses">Stresses</TabsTrigger>
            <TabsTrigger value="envelopes">Envelopes</TabsTrigger>
            <TabsTrigger value="diagrams">Diagrams</TabsTrigger>
            <TabsTrigger value="export">Export</TabsTrigger>
          </TabsList>
          <TabsContent value="stresses" className="space-y-4">
            <div>
              <Label>Load Case</Label>
              <Select value={loadCase} onValueChange={setLoadCase}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="DL">Dead Load</SelectItem>
                  <SelectItem value="LL">Live Load</SelectItem>
                  <SelectItem value="WL">Wind Load</SelectItem>
                  <SelectItem value="EL">Earthquake Load</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <p className="text-sm text-gray-500">Calculate element stresses and utilization ratios</p>
          </TabsContent>
          <TabsContent value="envelopes" className="space-y-4">
            <p className="text-sm text-gray-500">Generate load combination envelopes</p>
          </TabsContent>
          <TabsContent value="diagrams" className="space-y-4">
            <p className="text-sm text-gray-500">Generate moment, shear, and deflection diagrams</p>
          </TabsContent>
          <TabsContent value="export" className="space-y-4">
            <p className="text-sm text-gray-500">Export results to various formats</p>
          </TabsContent>
        </Tabs>
        <DialogFooter>
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button onClick={handleProcess} disabled={loading}>Process</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
