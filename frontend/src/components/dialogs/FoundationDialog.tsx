'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { foundationApi } from '@/lib/api';

interface FoundationDialogProps {
  open: boolean;
  onClose: () => void;
}

export function FoundationDialog({ open, onClose }: FoundationDialogProps) {
  const [loading, setLoading] = useState(false);
  const [foundationType, setFoundationType] = useState<'isolated' | 'mat' | 'pile'>('isolated');
  
  const { register, handleSubmit, setValue } = useForm({
    defaultValues: {
      P: 1000,
      Mx: 0,
      My: 0,
      soil_bearing_capacity: 200,
      concrete_grade: 25,
      steel_grade: 415,
    },
  });

  const onSubmit = async (data: any) => {
    setLoading(true);
    try {
      const result = await foundationApi.design({
        type: foundationType,
        loads: {
          P: data.P,
          Mx: data.Mx,
          My: data.My,
        },
        soil_bearing_capacity: data.soil_bearing_capacity,
        concrete_grade: data.concrete_grade,
        steel_grade: data.steel_grade,
      });
      console.log('Foundation design result:', result);
      onClose();
    } catch (error) {
      console.error('Foundation design failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>Foundation Design</DialogTitle>
        </DialogHeader>

        <Tabs value={foundationType} onValueChange={(v) => setFoundationType(v as any)}>
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="isolated">Isolated Footing</TabsTrigger>
            <TabsTrigger value="mat">Mat Foundation</TabsTrigger>
            <TabsTrigger value="pile">Pile Foundation</TabsTrigger>
          </TabsList>

          <TabsContent value="isolated">
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="P">Axial Load (kN)</Label>
                  <Input
                    id="P"
                    type="number"
                    {...register('P', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="Mx">Moment X (kNm)</Label>
                  <Input
                    id="Mx"
                    type="number"
                    {...register('Mx', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="My">Moment Y (kNm)</Label>
                  <Input
                    id="My"
                    type="number"
                    {...register('My', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="soil_bearing_capacity">SBC (kN/m²)</Label>
                  <Input
                    id="soil_bearing_capacity"
                    type="number"
                    {...register('soil_bearing_capacity', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="concrete_grade">Concrete Grade (MPa)</Label>
                  <Input
                    id="concrete_grade"
                    type="number"
                    {...register('concrete_grade', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <div>
                <Label htmlFor="steel_grade">Steel Grade (MPa)</Label>
                <Input
                  id="steel_grade"
                  type="number"
                  {...register('steel_grade', { valueAsNumber: true })}
                />
              </div>

              <DialogFooter>
                <Button type="button" variant="outline" onClick={onClose}>
                  Cancel
                </Button>
                <Button type="submit" disabled={loading}>
                  {loading ? 'Designing...' : 'Design Foundation'}
                </Button>
              </DialogFooter>
            </form>
          </TabsContent>

          <TabsContent value="mat">
            <div className="text-sm text-gray-500 p-4">
              Mat foundation design - Configure loads and soil properties
            </div>
          </TabsContent>

          <TabsContent value="pile">
            <div className="text-sm text-gray-500 p-4">
              Pile foundation design - Configure pile capacity and arrangement
            </div>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
