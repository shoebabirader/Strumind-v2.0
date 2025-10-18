'use client';

import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { modelsApi } from '@/lib/api';

interface ModelManagementDialogProps {
  open: boolean;
  onClose: () => void;
}

export function ModelManagementDialog({ open, onClose }: ModelManagementDialogProps) {
  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[700px]">
        <DialogHeader>
          <DialogTitle>Model Management</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">Model Validation</CardTitle>
            </CardHeader>
            <CardContent>
              <Button size="sm">Validate Model</Button>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">Model Cleanup</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <Button size="sm" variant="outline">Remove Duplicate Nodes</Button>
                <Button size="sm" variant="outline">Remove Unused Elements</Button>
                <Button size="sm" variant="outline">Merge Coincident Nodes</Button>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">Model Statistics</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-500">View model statistics and health</p>
            </CardContent>
          </Card>
        </div>
      </DialogContent>
    </Dialog>
  );
}
