'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { designApi } from '@/lib/api';

interface ConcreteDesignDialogProps {
  open: boolean;
  onClose: () => void;
}

export function ConcreteDesignDialog({ open, onClose }: ConcreteDesignDialogProps) {
  const [loading, setLoading] = useState(false);
  const [memberType, setMemberType] = useState<'beam' | 'column' | 'slab'>('beam');

  const handleDesign = async () => {
    setLoading(true);
    try {
      await designApi.run({ model_id: 1, design_type: 'concrete', element_ids: [1], design_code: 'IS456' });
      onClose();
    } catch (error) {
      console.error('Concrete design failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[700px]">
        <DialogHeader>
          <DialogTitle>Concrete Design (IS 456:2000)</DialogTitle>
        </DialogHeader>
        <Tabs defaultValue="beam">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="beam">Beam</TabsTrigger>
            <TabsTrigger value="column">Column</TabsTrigger>
            <TabsTrigger value="slab">Slab</TabsTrigger>
          </TabsList>
          <TabsContent value="beam" className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div><Label>Width (mm)</Label><Input type="number" defaultValue="300" /></div>
              <div><Label>Depth (mm)</Label><Input type="number" defaultValue="500" /></div>
              <div><Label>Concrete Grade</Label><Select><SelectTrigger><SelectValue placeholder="M25" /></SelectTrigger><SelectContent><SelectItem value="M20">M20</SelectItem><SelectItem value="M25">M25</SelectItem><SelectItem value="M30">M30</SelectItem></SelectContent></Select></div>
              <div><Label>Steel Grade</Label><Select><SelectTrigger><SelectValue placeholder="Fe415" /></SelectTrigger><SelectContent><SelectItem value="Fe415">Fe415</SelectItem><SelectItem value="Fe500">Fe500</SelectItem></SelectContent></Select></div>
            </div>
          </TabsContent>
          <TabsContent value="column" className="space-y-4">
            <div className="grid grid-cols-3 gap-4">
              <div><Label>Width (mm)</Label><Input type="number" defaultValue="400" /></div>
              <div><Label>Depth (mm)</Label><Input type="number" defaultValue="400" /></div>
              <div><Label>Height (m)</Label><Input type="number" step="0.1" defaultValue="3.5" /></div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div><Label>Axial Load (kN)</Label><Input type="number" defaultValue="1000" /></div>
              <div><Label>Moment (kNm)</Label><Input type="number" defaultValue="150" /></div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div><Label>Concrete Grade</Label><Select><SelectTrigger><SelectValue placeholder="M25" /></SelectTrigger><SelectContent><SelectItem value="M20">M20</SelectItem><SelectItem value="M25">M25</SelectItem><SelectItem value="M30">M30</SelectItem><SelectItem value="M40">M40</SelectItem></SelectContent></Select></div>
              <div><Label>Steel Grade</Label><Select><SelectTrigger><SelectValue placeholder="Fe415" /></SelectTrigger><SelectContent><SelectItem value="Fe415">Fe415</SelectItem><SelectItem value="Fe500">Fe500</SelectItem></SelectContent></Select></div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div><Label>Cover (mm)</Label><Input type="number" defaultValue="40" /></div>
              <div><Label>Column Type</Label><Select><SelectTrigger><SelectValue placeholder="Tied" /></SelectTrigger><SelectContent><SelectItem value="tied">Tied</SelectItem><SelectItem value="spiral">Spiral</SelectItem></SelectContent></Select></div>
            </div>
          </TabsContent>
          <TabsContent value="slab" className="space-y-4">
            <div className="grid grid-cols-3 gap-4">
              <div><Label>Thickness (mm)</Label><Input type="number" defaultValue="150" /></div>
              <div><Label>Span Lx (m)</Label><Input type="number" step="0.1" defaultValue="4" /></div>
              <div><Label>Span Ly (m)</Label><Input type="number" step="0.1" defaultValue="5" /></div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div><Label>Dead Load (kN/m²)</Label><Input type="number" step="0.1" defaultValue="2" /></div>
              <div><Label>Live Load (kN/m²)</Label><Input type="number" step="0.1" defaultValue="3" /></div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div><Label>Concrete Grade</Label><Select><SelectTrigger><SelectValue placeholder="M25" /></SelectTrigger><SelectContent><SelectItem value="M20">M20</SelectItem><SelectItem value="M25">M25</SelectItem><SelectItem value="M30">M30</SelectItem></SelectContent></Select></div>
              <div><Label>Steel Grade</Label><Select><SelectTrigger><SelectValue placeholder="Fe415" /></SelectTrigger><SelectContent><SelectItem value="Fe415">Fe415</SelectItem><SelectItem value="Fe500">Fe500</SelectItem></SelectContent></Select></div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div><Label>Support Condition</Label><Select><SelectTrigger><SelectValue placeholder="Simply Supported" /></SelectTrigger><SelectContent><SelectItem value="simply">Simply Supported</SelectItem><SelectItem value="continuous">Continuous</SelectItem><SelectItem value="fixed">Fixed</SelectItem></SelectContent></Select></div>
              <div><Label>Slab Type</Label><Select><SelectTrigger><SelectValue placeholder="One-Way" /></SelectTrigger><SelectContent><SelectItem value="oneway">One-Way</SelectItem><SelectItem value="twoway">Two-Way</SelectItem></SelectContent></Select></div>
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
