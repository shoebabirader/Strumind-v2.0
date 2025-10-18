'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Label } from '@/components/ui/label';
import { mlApi } from '@/lib/api';

interface MLDialogProps {
  open: boolean;
  onClose: () => void;
}

export function MLDialog({ open, onClose }: MLDialogProps) {
  const [model, setModel] = useState('section_prediction');
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    setLoading(true);
    try {
      await mlApi.predict({ model_type: model as 'beam_design' | 'column_design' | 'load_prediction', input_features: {} });
      onClose();
    } catch (error) {
      console.error('ML prediction failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>Machine Learning</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div><Label>ML Model</Label><Select value={model} onValueChange={setModel}><SelectTrigger><SelectValue /></SelectTrigger><SelectContent><SelectItem value="section_prediction">Section Prediction</SelectItem><SelectItem value="reinforcement">Reinforcement Prediction</SelectItem><SelectItem value="optimization">Design Optimization</SelectItem><SelectItem value="load_prediction">Load Prediction</SelectItem><SelectItem value="failure_prediction">Failure Prediction</SelectItem></SelectContent></Select></div>
          <div className="p-4 bg-purple-50 rounded-lg"><p className="text-sm font-medium mb-2">AI-Powered Features:</p><ul className="text-sm space-y-1 text-gray-700"><li>• Automatic section sizing</li><li>• Reinforcement optimization</li><li>• Load pattern recognition</li><li>• Failure mode prediction</li></ul></div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button onClick={handlePredict} disabled={loading}>Predict</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
