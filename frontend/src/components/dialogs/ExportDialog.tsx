'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';

interface ExportDialogProps {
  open: boolean;
  onClose: () => void;
}

export function ExportDialog({ open, onClose }: ExportDialogProps) {
  const [format, setFormat] = useState('json');
  const [includeResults, setIncludeResults] = useState(true);

  const handleExport = () => {
    console.log('Exporting as:', format);
    onClose();
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Export Model</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div><Label>Export Format</Label><Select value={format} onValueChange={setFormat}><SelectTrigger><SelectValue /></SelectTrigger><SelectContent><SelectItem value="json">JSON</SelectItem><SelectItem value="csv">CSV</SelectItem><SelectItem value="excel">Excel</SelectItem><SelectItem value="dxf">DXF (CAD)</SelectItem><SelectItem value="ifc">IFC (BIM)</SelectItem><SelectItem value="pdf">PDF Report</SelectItem></SelectContent></Select></div>
          <div className="flex items-center space-x-2">
            <Checkbox id="results" checked={includeResults} onCheckedChange={(checked) => setIncludeResults(checked as boolean)} />
            <label htmlFor="results" className="text-sm">Include analysis results</label>
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button onClick={handleExport}>Export</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
