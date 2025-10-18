'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { specializedDesignApi } from '@/lib/api';

interface MovingLoadDialogProps {
  open: boolean;
  onClose: () => void;
}

export function MovingLoadDialog({ open, onClose }: MovingLoadDialogProps) {
  const [loading, setLoading] = useState(false);
  const [span, setSpan] = useState('10');
  const [loadingStandard, setLoadingStandard] = useState('IRC_Class_A');

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      await specializedDesignApi.movingLoad({ span: parseFloat(span), response_type: 'moment', location: 0, loading_standard: loadingStandard });
      onClose();
    } catch (error) {
      console.error('Moving load analysis failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader><DialogTitle>Moving Load Analysis</DialogTitle></DialogHeader>
        <div className="space-y-4">
          <div><Label htmlFor="span">Span (m)</Label><Input id="span" type="number" value={span} onChange={(e) => setSpan(e.target.value)} /></div>
          <div>
            <Label>Loading Standard</Label>
            <Select value={loadingStandard} onValueChange={setLoadingStandard}>
              <SelectTrigger><SelectValue /></SelectTrigger>
              <SelectContent>
                <SelectItem value="IRC_Class_A">IRC Class A</SelectItem>
                <SelectItem value="AASHTO_HS20">AASHTO HS20</SelectItem>
              </SelectContent>
            </Select>
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
