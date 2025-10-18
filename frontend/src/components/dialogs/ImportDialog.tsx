'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

interface ImportDialogProps {
  open: boolean;
  onClose: () => void;
}

export function ImportDialog({ open, onClose }: ImportDialogProps) {
  const [file, setFile] = useState<File | null>(null);

  const handleImport = () => {
    if (file) {
      console.log('Importing file:', file.name);
      onClose();
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Import Model</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div><Label>Select File</Label><Input type="file" accept=".json,.csv,.dxf,.ifc" onChange={(e) => setFile(e.target.files?.[0] || null)} /></div>
          <p className="text-sm text-gray-500">Supported formats: JSON, CSV, DXF, IFC</p>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button onClick={handleImport} disabled={!file}>Import</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
