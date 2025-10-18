'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { specializedDesignApi } from '@/lib/api';

interface TemperatureDialogProps {
  open: boolean;
  onClose: () => void;
}

export function TemperatureDialog({ open, onClose }: TemperatureDialogProps) {
  const [loading, setLoading] = useState(false);
  const [analysisType, setAnalysisType] = useState('uniform');
  const [deltaT, setDeltaT] = useState('30');
  const [length, setLength] = useState('50');

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      await specializedDesignApi.temperatureAnalysis({ analysis_type: analysisType as any, delta_T: parseFloat(deltaT), length: parseFloat(length) });
      onClose();
    } catch (error) {
      console.error('Temperature analysis failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader><DialogTitle>Temperature Analysis</DialogTitle></DialogHeader>
        <div className="space-y-4">
          <div>
            <Label>Analysis Type</Label>
            <Select value={analysisType} onValueChange={setAnalysisType}>
              <SelectTrigger><SelectValue /></SelectTrigger>
              <SelectContent>
                <SelectItem value="uniform">Uniform</SelectItem>
                <SelectItem value="gradient">Gradient</SelectItem>
                <SelectItem value="fire">Fire</SelectItem>
                <SelectItem value="seasonal">Seasonal</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div><Label htmlFor="deltaT">ΔT (°C)</Label><Input id="deltaT" type="number" value={deltaT} onChange={(e) => setDeltaT(e.target.value)} /></div>
            <div><Label htmlFor="length">Length (m)</Label><Input id="length" type="number" value={length} onChange={(e) => setLength(e.target.value)} /></div>
          </div>
        </div>
        <DialogFooter>
          <Button type="button" variant="outline" onClick={onClose}>Cancel</Button>
          <Button onClick={handleAnalyze} disabled={loading}>{loading ? 'Analyzing...' : 'Analyze'}</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
