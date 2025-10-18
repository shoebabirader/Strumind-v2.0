'use client';

import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';

interface AboutDialogProps {
  open: boolean;
  onClose: () => void;
}

export function AboutDialog({ open, onClose }: AboutDialogProps) {
  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>About StrucMind</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div className="text-center py-4">
            <div className="text-4xl mb-2">🏗️</div>
            <h2 className="text-2xl font-bold">StrucMind</h2>
            <p className="text-sm text-gray-500">Professional Structural Analysis Software</p>
          </div>
          <Card>
            <CardContent className="pt-4 space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">Version:</span>
                <span className="font-semibold">1.0.0</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Build:</span>
                <span className="font-semibold">2025.10.17</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">License:</span>
                <span className="font-semibold">Professional</span>
              </div>
            </CardContent>
          </Card>
          <div className="flex gap-2">
            <Button size="sm" variant="outline" className="flex-1">Release Notes</Button>
            <Button size="sm" variant="outline" className="flex-1">Check for Updates</Button>
          </div>
          <p className="text-xs text-center text-gray-500">
            © 2025 StrucMind. All rights reserved.
          </p>
        </div>
      </DialogContent>
    </Dialog>
  );
}
