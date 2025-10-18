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
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Import Model</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div><Label>Select File</Label><Input type="file" accept=".json,.csv,.dxf,.ifc" onChange={(e) => setFile(e.target.files?.[0] || null)} /></div>
          {file && <div className="p-3 bg-blue-50 rounded"><p className="text-sm font-medium">Selected: {file.name}</p><p className="text-xs text-gray-600">Size: {(file.size/1024).toFixed(1)} KB</p></div>}
          <div className="p-4 bg-gray-50 rounded"><p className="text-sm font-medium mb-2">Supported Formats:</p><ul className="text-xs space-y-1 text-gray-700"><li>• JSON - StruMind native format</li><li>• CSV - Tabular data</li><li>• DXF - AutoCAD geometry</li><li>• IFC - BIM models</li></ul></div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button onClick={handleImport} disabled={!file}>Import</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
