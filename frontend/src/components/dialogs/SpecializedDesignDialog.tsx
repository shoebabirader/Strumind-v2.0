'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { specializedDesignApi } from '@/lib/api';

interface SpecializedDesignDialogProps {
  open: boolean;
  onClose: () => void;
}

export function SpecializedDesignDialog({ open, onClose }: SpecializedDesignDialogProps) {
  const [loading, setLoading] = useState(false);

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[700px]">
        <DialogHeader>
          <DialogTitle>Specialized Design</DialogTitle>
        </DialogHeader>
        <Tabs defaultValue="shearwall">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="shearwall">Shear Wall</TabsTrigger>
            <TabsTrigger value="retaining">Retaining Wall</TabsTrigger>
            <TabsTrigger value="staircase">Staircase</TabsTrigger>
            <TabsTrigger value="watertank">Water Tank</TabsTrigger>
          </TabsList>
          <TabsContent value="shearwall" className="space-y-4">
            <p className="text-sm">Design shear walls per IS 13920</p>
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
