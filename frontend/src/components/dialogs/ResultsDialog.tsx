'use client';

import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface ResultsDialogProps {
  open: boolean;
  onClose: () => void;
}

export function ResultsDialog({ open, onClose }: ResultsDialogProps) {
  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[900px] max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Analysis Results</DialogTitle>
        </DialogHeader>
        <Tabs defaultValue="displacements">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="displacements">Displacements</TabsTrigger>
            <TabsTrigger value="forces">Forces</TabsTrigger>
            <TabsTrigger value="stresses">Stresses</TabsTrigger>
            <TabsTrigger value="reactions">Reactions</TabsTrigger>
          </TabsList>
          <TabsContent value="displacements">
            <Card><CardHeader><CardTitle className="text-sm">Node Displacements</CardTitle></CardHeader><CardContent><p className="text-sm text-gray-500">Displacement results will appear here</p></CardContent></Card>
          </TabsContent>
          <TabsContent value="forces">
            <Card><CardHeader><CardTitle className="text-sm">Element Forces</CardTitle></CardHeader><CardContent><p className="text-sm text-gray-500">Force results will appear here</p></CardContent></Card>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
