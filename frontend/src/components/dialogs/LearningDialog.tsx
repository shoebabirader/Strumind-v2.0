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
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[700px]">
        <DialogHeader>
          <DialogTitle>Learning Resources</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <Card><CardHeader><CardTitle className="text-sm">Tutorials</CardTitle></CardHeader><CardContent><Button variant="outline" size="sm">Getting Started</Button></CardContent></Card>
          <Card><CardHeader><CardTitle className="text-sm">Documentation</CardTitle></CardHeader><CardContent><Button variant="outline" size="sm">View Docs</Button></CardContent></Card>
          <Card><CardHeader><CardTitle className="text-sm">Video Guides</CardTitle></CardHeader><CardContent><Button variant="outline" size="sm">Watch Videos</Button></CardContent></Card>
        </div>
      </DialogContent>
    </Dialog>
  );
}
