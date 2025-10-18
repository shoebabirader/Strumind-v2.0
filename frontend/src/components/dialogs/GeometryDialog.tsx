'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { geometryApi } from '@/lib/api';

interface GeometryDialogProps {
  open: boolean;
  onClose: () => void;
}

export function GeometryDialog({ open, onClose }: GeometryDialogProps) {
  const [loading, setLoading] = useState(false);

  const handleValidate = async () => {
    setLoading(true);
    try {
      await geometryApi.validate(1, 0.001);
      onClose();
    } catch (error) {
      console.error('Geometry validation failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>Geometry Tools</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div><Label>Tolerance (mm)</Label><Input type="number" step="0.001" defaultValue="0.001" /></div>
          <p className="text-sm text-gray-500">Validate and fix geometry issues</p>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button onClick={handleValidate} disabled={loading}>Validate</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
