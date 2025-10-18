'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useDesign } from '@/hooks/useDesign';
import { useModelStore } from '@/stores/modelStore';

interface DesignDialogProps {
  open: boolean;
  onClose: () => void;
}

export function DesignDialog({ open, onClose }: DesignDialogProps) {
  const { currentProject } = useModelStore();
  const { runDesign, isLoading } = useDesign();
  const [designCode, setDesignCode] = useState('IS456');
  const [designType, setDesignType] = useState<'concrete' | 'steel'>('concrete');

  const handleRunDesign = async () => {
    if (!currentProject) return;

    try {
      await runDesign({
        model_id: currentProject.id,
        design_code: designCode,
        design_type: designType,
      });
      onClose();
    } catch (error) {
      console.error('Design failed:', error);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>Member Design</DialogTitle>
        </DialogHeader>

        <Tabs defaultValue="concrete" onValueChange={(v) => setDesignType(v as any)}>
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="concrete">Concrete Design</TabsTrigger>
            <TabsTrigger value="steel">Steel Design</TabsTrigger>
          </TabsList>

          <TabsContent value="concrete" className="space-y-4">
            <div>
              <Label>Design Code</Label>
              <Select value={designCode} onValueChange={setDesignCode}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="IS456">IS 456:2000</SelectItem>
                  <SelectItem value="ACI318">ACI 318-19</SelectItem>
                  <SelectItem value="BS8110">BS 8110</SelectItem>
                  <SelectItem value="EC2">Eurocode 2</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="p-4 bg-blue-50 rounded-lg">
              <h4 className="font-medium text-sm mb-2">Concrete Design Features:</h4>
              <ul className="text-sm space-y-1 text-gray-700">
                <li>• Flexural design (beams & slabs)</li>
                <li>• Shear design with stirrups</li>
                <li>• Column design (axial + bending)</li>
                <li>• Torsion design</li>
                <li>• Detailing as per code</li>
              </ul>
            </div>
          </TabsContent>

          <TabsContent value="steel" className="space-y-4">
            <div>
              <Label>Design Code</Label>
              <Select value={designCode} onValueChange={setDesignCode}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="IS800">IS 800:2007</SelectItem>
                  <SelectItem value="AISC360">AISC 360-16</SelectItem>
                  <SelectItem value="BS5950">BS 5950</SelectItem>
                  <SelectItem value="EC3">Eurocode 3</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="p-4 bg-green-50 rounded-lg">
              <h4 className="font-medium text-sm mb-2">Steel Design Features:</h4>
              <ul className="text-sm space-y-1 text-gray-700">
                <li>• Tension member design</li>
                <li>• Compression member design</li>
                <li>• Beam design (flexure & shear)</li>
                <li>• Connection design</li>
                <li>• Buckling checks</li>
              </ul>
            </div>
          </TabsContent>
        </Tabs>

        <DialogFooter>
          <Button type="button" variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <Button onClick={handleRunDesign} disabled={isLoading}>
            {isLoading ? 'Designing...' : 'Run Design'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
