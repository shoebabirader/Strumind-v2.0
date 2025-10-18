'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Label } from '@/components/ui/label';

interface LoadCombinationsDialogProps {
  open: boolean;
  onClose: () => void;
}

export function LoadCombinationsDialog({ open, onClose }: LoadCombinationsDialogProps) {
  const [code, setCode] = useState('IS456');

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>Load Combinations</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div><Label>Design Code</Label><Select value={code} onValueChange={setCode}><SelectTrigger><SelectValue /></SelectTrigger><SelectContent><SelectItem value="IS456">IS 456:2000</SelectItem><SelectItem value="ACI318">ACI 318</SelectItem><SelectItem value="EC2">Eurocode 2</SelectItem></SelectContent></Select></div>
          <div className="border rounded p-4 space-y-2">
            <div className="flex justify-between"><span className="text-sm">1.5 DL + 1.5 LL</span><Button size="sm" variant="outline">Edit</Button></div>
            <div className="flex justify-between"><span className="text-sm">1.2 DL + 1.2 LL + 1.2 WL</span><Button size="sm" variant="outline">Edit</Button></div>
            <div className="flex justify-between"><span className="text-sm">1.2 DL + 1.2 LL + 1.2 EL</span><Button size="sm" variant="outline">Edit</Button></div>
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={onClose}>Close</Button>
          <Button>Apply Combinations</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
