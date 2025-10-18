'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Label } from '@/components/ui/label';

interface UnitsDialogProps {
  open: boolean;
  onClose: () => void;
}

export function UnitsDialog({ open, onClose }: UnitsDialogProps) {
  const [unitSystem, setUnitSystem] = useState('SI');

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Unit System</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div><Label>Unit System</Label><Select value={unitSystem} onValueChange={setUnitSystem}><SelectTrigger><SelectValue /></SelectTrigger><SelectContent><SelectItem value="SI">SI (m, kN, MPa)</SelectItem><SelectItem value="SI_mm">SI (mm, N, MPa)</SelectItem><SelectItem value="Imperial">Imperial (ft, kip, ksi)</SelectItem></SelectContent></Select></div>
          <p className="text-sm text-gray-500">Change units for the entire project</p>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button>Apply Units</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
