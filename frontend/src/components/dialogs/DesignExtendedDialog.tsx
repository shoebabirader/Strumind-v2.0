'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { designExtendedApi } from '@/lib/api';

interface DesignExtendedDialogProps {
  open: boolean;
  onClose: () => void;
}

export function DesignExtendedDialog({ open, onClose }: DesignExtendedDialogProps) {
  const [loading, setLoading] = useState(false);

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[700px]">
        <DialogHeader>
          <DialogTitle>Extended Design Features</DialogTitle>
        </DialogHeader>
        <Tabs defaultValue="composite">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="composite">Composite</TabsTrigger>
            <TabsTrigger value="prestressed">Prestressed</TabsTrigger>
            <TabsTrigger value="timber">Timber</TabsTrigger>
          </TabsList>
          <TabsContent value="composite" className="space-y-4">
            <p className="text-sm">Composite beam and column design</p>
          </TabsContent>
        </Tabs>
        <DialogFooter>
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button disabled={loading}>Design</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
