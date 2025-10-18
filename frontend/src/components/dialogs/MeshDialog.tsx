'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { specializedDesignApi } from '@/lib/api';

interface MeshDialogProps {
  open: boolean;
  onClose: () => void;
}

export function MeshDialog({ open, onClose }: MeshDialogProps) {
  const [loading, setLoading] = useState(false);
  const [width, setWidth] = useState('10');
  const [height, setHeight] = useState('10');
  const [nx, setNx] = useState('10');
  const [ny, setNy] = useState('10');

  const handleGenerate = async () => {
    setLoading(true);
    try {
      await specializedDesignApi.generateMesh({ mesh_type: 'rectangle', width: parseFloat(width), height: parseFloat(height), nx: parseInt(nx), ny: parseInt(ny) });
      onClose();
    } catch (error) {
      console.error('Mesh generation failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader><DialogTitle>Mesh Generation</DialogTitle></DialogHeader>
        <Tabs defaultValue="generate">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="generate">Generate</TabsTrigger>
            <TabsTrigger value="refine">Refine</TabsTrigger>
            <TabsTrigger value="quality">Quality</TabsTrigger>
          </TabsList>
          <TabsContent value="generate" className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div><Label htmlFor="width">Width (m)</Label><Input id="width" type="number" value={width} onChange={(e) => setWidth(e.target.value)} /></div>
              <div><Label htmlFor="height">Height (m)</Label><Input id="height" type="number" value={height} onChange={(e) => setHeight(e.target.value)} /></div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div><Label htmlFor="nx">Divisions X</Label><Input id="nx" type="number" value={nx} onChange={(e) => setNx(e.target.value)} /></div>
              <div><Label htmlFor="ny">Divisions Y</Label><Input id="ny" type="number" value={ny} onChange={(e) => setNy(e.target.value)} /></div>
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" onClick={onClose}>Cancel</Button>
              <Button onClick={handleGenerate} disabled={loading}>{loading ? 'Generating...' : 'Generate Mesh'}</Button>
            </DialogFooter>
          </TabsContent>
          <TabsContent value="refine"><div className="text-sm text-gray-500 p-4">Mesh refinement options</div></TabsContent>
          <TabsContent value="quality"><div className="text-sm text-gray-500 p-4">Mesh quality check</div></TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
