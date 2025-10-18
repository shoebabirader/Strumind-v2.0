'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { serviceabilityApi } from '@/lib/api';

interface ServiceabilityDialogProps {
  open: boolean;
  onClose: () => void;
}

export function ServiceabilityDialog({ open, onClose }: ServiceabilityDialogProps) {
  const [loading, setLoading] = useState(false);
  const [span, setSpan] = useState('6');
  const [deflection, setDeflection] = useState('0.025');

  const handleCheck = async () => {
    setLoading(true);
    try {
      await serviceabilityApi.checkDeflection({ span: parseFloat(span), deflection: parseFloat(deflection), load_type: 'total', member_type: 'beam' });
      onClose();
    } catch (error) {
      console.error('Serviceability check failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader><DialogTitle>Serviceability Checks</DialogTitle></DialogHeader>
        <Tabs defaultValue="deflection">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="deflection">Deflection</TabsTrigger>
            <TabsTrigger value="crack">Crack Width</TabsTrigger>
            <TabsTrigger value="vibration">Vibration</TabsTrigger>
            <TabsTrigger value="punching">Punching</TabsTrigger>
          </TabsList>
          <TabsContent value="deflection" className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div><Label htmlFor="span">Span (m)</Label><Input id="span" type="number" value={span} onChange={(e) => setSpan(e.target.value)} /></div>
              <div><Label htmlFor="deflection">Deflection (m)</Label><Input id="deflection" type="number" step="0.001" value={deflection} onChange={(e) => setDeflection(e.target.value)} /></div>
            </div>
            <DialogFooter>
              <Button type="button" variant="outline" onClick={onClose}>Cancel</Button>
              <Button onClick={handleCheck} disabled={loading}>{loading ? 'Checking...' : 'Check Deflection'}</Button>
            </DialogFooter>
          </TabsContent>
          <TabsContent value="crack"><div className="text-sm text-gray-500 p-4">Crack width check</div></TabsContent>
          <TabsContent value="vibration"><div className="text-sm text-gray-500 p-4">Vibration check</div></TabsContent>
          <TabsContent value="punching"><div className="text-sm text-gray-500 p-4">Punching shear check</div></TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
