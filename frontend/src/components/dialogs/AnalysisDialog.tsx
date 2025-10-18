'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useAnalysis } from '@/hooks/useAnalysis';
import { useModelStore } from '@/stores/modelStore';

interface AnalysisDialogProps {
  open: boolean;
  onClose: () => void;
}

export function AnalysisDialog({ open, onClose }: AnalysisDialogProps) {
  const { currentProject } = useModelStore();
  const { runAnalysis, isLoading } = useAnalysis();
  const [analysisType, setAnalysisType] = useState<'linear' | 'modal' | 'time_history' | 'pushover' | 'buckling' | 'pdelta'>('linear');

  const handleRunAnalysis = async () => {
    if (!currentProject) return;

    try {
      await runAnalysis({
        project_id: currentProject.id,
        analysis_type: analysisType,
      });
      onClose();
    } catch (error) {
      console.error('Analysis failed:', error);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>Run Analysis</DialogTitle>
        </DialogHeader>

        <Tabs defaultValue="basic" className="w-full">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="basic">Basic</TabsTrigger>
            <TabsTrigger value="dynamic">Dynamic</TabsTrigger>
            <TabsTrigger value="nonlinear">Nonlinear</TabsTrigger>
          </TabsList>

          <TabsContent value="basic" className="space-y-4">
            <div>
              <Label>Analysis Type</Label>
              <Select value={analysisType} onValueChange={(v) => setAnalysisType(v as typeof analysisType)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="linear">Linear Static</SelectItem>
                  <SelectItem value="modal">Modal Analysis</SelectItem>
                  <SelectItem value="buckling">Buckling Analysis</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </TabsContent>

          <TabsContent value="dynamic" className="space-y-4">
            <div>
              <Label>Dynamic Analysis Type</Label>
              <Select value={analysisType} onValueChange={(v) => setAnalysisType(v as typeof analysisType)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="time_history">Time History</SelectItem>
                  <SelectItem value="response_spectrum">Response Spectrum</SelectItem>
                  <SelectItem value="frequency_response">Frequency Response</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </TabsContent>

          <TabsContent value="nonlinear" className="space-y-4">
            <div>
              <Label>Nonlinear Analysis Type</Label>
              <Select value={analysisType} onValueChange={(v) => setAnalysisType(v as typeof analysisType)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="pushover">Pushover Analysis</SelectItem>
                  <SelectItem value="pdelta">P-Delta Analysis</SelectItem>
                  <SelectItem value="geometric_nonlinear">Geometric Nonlinear</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </TabsContent>
        </Tabs>

        <DialogFooter>
          <Button type="button" variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <Button onClick={handleRunAnalysis} disabled={isLoading}>
            {isLoading ? 'Running...' : 'Run Analysis'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
