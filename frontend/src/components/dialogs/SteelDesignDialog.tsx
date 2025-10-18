'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { designApi } from '@/lib/api';

interface SteelDesignDialogProps {
  open: boolean;
  onClose: () => void;
}

export function SteelDesignDialog({ open, onClose }: SteelDesignDialogProps) {
  const [loading, setLoading] = useState(false);
  const [memberType, setMemberType] = useState<'beam' | 'column' | 'truss'>('beam');

  const handleDesign = async () => {
    setLoading(true);
    try {
      await designApi.run({ model_id: 1, design_type: 'steel', element_ids: [1], design_code: 'IS800' });
      onClose();
    } catch (error) {
      console.error('Steel design failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[700px]">
        <DialogHeader>
          <DialogTitle>Steel Design (IS 800:2007)</DialogTitle>
        </DialogHeader>
        <Tabs defaultValue="beam">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="beam">Beam</TabsTrigger>
            <TabsTrigger value="column">Column</TabsTrigger>
            <TabsTrigger value="truss">Truss</TabsTrigger>
          </TabsList>
          <TabsContent value="beam" className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div><Label>Section</Label><Select><SelectTrigger><SelectValue placeholder="ISMB 300" /></SelectTrigger><SelectContent><SelectItem value="ISMB200">ISMB 200</SelectItem><SelectItem value="ISMB300">ISMB 300</SelectItem><SelectItem value="ISMB400">ISMB 400</SelectItem></SelectContent></Select></div>
              <div><Label>Steel Grade</Label><Select><SelectTrigger><SelectValue placeholder="Fe410" /></SelectTrigger><SelectContent><SelectItem value="Fe410">Fe410</SelectItem><SelectItem value="Fe500">Fe500</SelectItem></SelectContent></Select></div>
            </div>
          </TabsContent>
          <TabsContent value="column" className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div><Label>Section</Label><Select><SelectTrigger><SelectValue placeholder="ISHB 300" /></SelectTrigger><SelectContent><SelectItem value="ISHB200">ISHB 200</SelectItem><SelectItem value="ISHB300">ISHB 300</SelectItem><SelectItem value="ISHB400">ISHB 400</SelectItem><SelectItem value="ISHB450">ISHB 450</SelectItem></SelectContent></Select></div>
              <div><Label>Effective Length (m)</Label><Input type="number" step="0.1" defaultValue="3.5" /></div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div><Label>Axial Load (kN)</Label><Input type="number" defaultValue="500" /></div>
              <div><Label>Moment (kNm)</Label><Input type="number" defaultValue="100" /></div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div><Label>Steel Grade</Label><Select><SelectTrigger><SelectValue placeholder="Fe410" /></SelectTrigger><SelectContent><SelectItem value="Fe250">Fe250</SelectItem><SelectItem value="Fe410">Fe410</SelectItem><SelectItem value="Fe500">Fe500</SelectItem></SelectContent></Select></div>
              <div><Label>End Condition</Label><Select><SelectTrigger><SelectValue placeholder="Pinned-Pinned" /></SelectTrigger><SelectContent><SelectItem value="pinned">Pinned-Pinned</SelectItem><SelectItem value="fixed">Fixed-Fixed</SelectItem><SelectItem value="fixed_pinned">Fixed-Pinned</SelectItem></SelectContent></Select></div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div><Label>Slenderness Ratio</Label><Input type="number" defaultValue="120" disabled /></div>
              <div><Label>Classification</Label><Input defaultValue="Compact" disabled /></div>
            </div>
          </TabsContent>
          <TabsContent value="truss" className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div><Label>Section</Label><Select><SelectTrigger><SelectValue placeholder="ISA 75x75x6" /></SelectTrigger><SelectContent><SelectItem value="ISA65">ISA 65x65x6</SelectItem><SelectItem value="ISA75">ISA 75x75x6</SelectItem><SelectItem value="ISA90">ISA 90x90x8</SelectItem><SelectItem value="ISA100">ISA 100x100x8</SelectItem></SelectContent></Select></div>
              <div><Label>Member Length (m)</Label><Input type="number" step="0.1" defaultValue="2.5" /></div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div><Label>Axial Force (kN)</Label><Input type="number" defaultValue="150" /></div>
              <div><Label>Force Type</Label><Select><SelectTrigger><SelectValue placeholder="Tension" /></SelectTrigger><SelectContent><SelectItem value="tension">Tension</SelectItem><SelectItem value="compression">Compression</SelectItem></SelectContent></Select></div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div><Label>Steel Grade</Label><Select><SelectTrigger><SelectValue placeholder="Fe410" /></SelectTrigger><SelectContent><SelectItem value="Fe410">Fe410</SelectItem><SelectItem value="Fe500">Fe500</SelectItem></SelectContent></Select></div>
              <div><Label>Connection Type</Label><Select><SelectTrigger><SelectValue placeholder="Welded" /></SelectTrigger><SelectContent><SelectItem value="welded">Welded</SelectItem><SelectItem value="bolted">Bolted</SelectItem></SelectContent></Select></div>
            </div>
          </TabsContent>
        </Tabs>
        <DialogFooter>
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button onClick={handleDesign} disabled={loading}>Design</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
