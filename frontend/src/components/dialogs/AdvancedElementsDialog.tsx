'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Label } from '@/components/ui/label';
import { advancedElementsApi } from '@/lib/api';

interface AdvancedElementsDialogProps {
  open: boolean;
  onClose: () => void;
}

export function AdvancedElementsDialog({ open, onClose }: AdvancedElementsDialogProps) {
  const [elementType, setElementType] = useState('shell');

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>Advanced Elements</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div><Label>Element Type</Label><Select value={elementType} onValueChange={setElementType}><SelectTrigger><SelectValue /></SelectTrigger><SelectContent><SelectItem value="shell">Shell</SelectItem><SelectItem value="plate">Plate</SelectItem><SelectItem value="solid">Solid</SelectItem><SelectItem value="cable">Cable</SelectItem></SelectContent></Select></div>
          <p className="text-sm text-gray-500">Advanced finite elements for complex structures</p>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button>Create Element</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
