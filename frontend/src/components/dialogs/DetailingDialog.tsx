'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { detailingApi } from '@/lib/api';

interface DetailingDialogProps {
  open: boolean;
  onClose: () => void;
}

export function DetailingDialog({ open, onClose }: DetailingDialogProps) {
  const [loading, setLoading] = useState(false);
  const [elementId, setElementId] = useState('');
  const [drawingStandard, setDrawingStandard] = useState('IS');

  const handleGenerate = async () => {
    if (!elementId) return;

    setLoading(true);
    try {
      await detailingApi.generate({
        element_id: parseInt(elementId),
        design_results: {},
        drawing_standard: drawingStandard as any,
      });
      onClose();
    } catch (error) {
      console.error('Detailing generation failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Generate Detailing</DialogTitle>
        </DialogHeader>

        <div className="space-y-4">
          <div>
            <Label htmlFor="element_id">Element ID</Label>
            <Input
              id="element_id"
              type="number"
              value={elementId}
              onChange={(e) => setElementId(e.target.value)}
              placeholder="Enter element ID"
            />
          </div>

          <div>
            <Label>Drawing Standard</Label>
            <Select value={drawingStandard} onValueChange={setDrawingStandard}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="IS">IS Code</SelectItem>
                <SelectItem value="BS">BS Code</SelectItem>
                <SelectItem value="ACI">ACI Code</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="p-4 bg-blue-50 rounded-lg text-sm">
            <p className="font-medium mb-2">Detailing will include:</p>
            <ul className="space-y-1 text-gray-700">
              <li>• Reinforcement layout</li>
              <li>• Bar bending schedule (BBS)</li>
              <li>• Section details</li>
              <li>• Stirrup spacing</li>
              <li>• Development lengths</li>
            </ul>
          </div>
        </div>

        <DialogFooter>
          <Button type="button" variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <Button onClick={handleGenerate} disabled={loading || !elementId}>
            {loading ? 'Generating...' : 'Generate Detailing'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
