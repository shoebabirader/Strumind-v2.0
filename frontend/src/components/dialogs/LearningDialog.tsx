'use client';

import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

interface LearningDialogProps {
  open: boolean;
  onClose: () => void;
}

export function LearningDialog({ open, onClose }: LearningDialogProps) {
  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[700px]">
        <DialogHeader>
          <DialogTitle>Learning Resources</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <Card><CardHeader><CardTitle className="text-sm">Tutorials</CardTitle></CardHeader><CardContent className="space-y-2"><Button variant="outline" size="sm" className="w-full justify-start">Getting Started Guide</Button><Button variant="outline" size="sm" className="w-full justify-start">Modeling Basics</Button><Button variant="outline" size="sm" className="w-full justify-start">Analysis Setup</Button></CardContent></Card>
          <Card><CardHeader><CardTitle className="text-sm">Documentation</CardTitle></CardHeader><CardContent className="space-y-2"><Button variant="outline" size="sm" className="w-full justify-start">API Reference</Button><Button variant="outline" size="sm" className="w-full justify-start">Design Codes</Button><Button variant="outline" size="sm" className="w-full justify-start">Examples</Button></CardContent></Card>
          <Card><CardHeader><CardTitle className="text-sm">Video Guides</CardTitle></CardHeader><CardContent className="space-y-2"><Button variant="outline" size="sm" className="w-full justify-start">Quick Start (5 min)</Button><Button variant="outline" size="sm" className="w-full justify-start">Advanced Features (15 min)</Button><Button variant="outline" size="sm" className="w-full justify-start">Design Workflow (20 min)</Button></CardContent></Card>
        </div>
      </DialogContent>
    </Dialog>
  );
}
