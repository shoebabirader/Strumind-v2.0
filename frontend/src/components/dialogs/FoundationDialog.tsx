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
      mat_area: 100,
      mat_thickness: 0.5,
      soil_modulus: 50000,
      pile_capacity: 500,
      pile_diameter: 0.6,
      pile_length: 15,
      pile_spacing: 2.5,
      pile_type: 'bored',
      pile_cap_thickness: 1.0,
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
      // SECURITY FIX: Don't log potentially sensitive result data
      console.log('Foundation design completed successfully');
      onClose();
    } catch (error) {
      // SECURITY FIX: Sanitize error before logging
      const sanitizedError = error instanceof Error ? error.message.replace(/[\r\n]/g, ' ') : 'Unknown error';
      console.error('Foundation design failed:', sanitizedError);
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
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="total_load_mat">Total Load (kN)</Label>
                  <Input
                    id="total_load_mat"
                    type="number"
                    {...register('P', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="mat_area">Mat Area (m²)</Label>
                  <Input
                    id="mat_area"
                    type="number"
                    defaultValue="100"
                    {...register('mat_area', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="mat_thickness">Mat Thickness (m)</Label>
                  <Input
                    id="mat_thickness"
                    type="number"
                    step="0.1"
                    defaultValue="0.5"
                    {...register('mat_thickness', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="soil_modulus">Soil Modulus (kN/m³)</Label>
                  <Input
                    id="soil_modulus"
                    type="number"
                    defaultValue="20000"
                    {...register('soil_modulus', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="concrete_grade_mat">Concrete Grade (MPa)</Label>
                  <Input
                    id="concrete_grade_mat"
                    type="number"
                    {...register('concrete_grade', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="steel_grade_mat">Steel Grade (MPa)</Label>
                  <Input
                    id="steel_grade_mat"
                    type="number"
                    {...register('steel_grade', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <div>
                <Label htmlFor="soil_bearing_capacity_mat">SBC (kN/m²)</Label>
                <Input
                  id="soil_bearing_capacity_mat"
                  type="number"
                  {...register('soil_bearing_capacity', { valueAsNumber: true })}
                />
              </div>

              <DialogFooter>
                <Button type="button" variant="outline" onClick={onClose}>
                  Cancel
                </Button>
                <Button type="submit" disabled={loading}>
                  {loading ? 'Designing...' : 'Design Mat Foundation'}
                </Button>
              </DialogFooter>
            </form>
          </TabsContent>

          <TabsContent value="pile">
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="total_load_pile">Total Load (kN)</Label>
                  <Input
                    id="total_load_pile"
                    type="number"
                    {...register('P', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="pile_capacity">Pile Capacity (kN)</Label>
                  <Input
                    id="pile_capacity"
                    type="number"
                    defaultValue="500"
                    {...register('pile_capacity', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="pile_diameter">Pile Dia (m)</Label>
                  <Input
                    id="pile_diameter"
                    type="number"
                    step="0.05"
                    defaultValue="0.5"
                    {...register('pile_diameter', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="pile_length">Pile Length (m)</Label>
                  <Input
                    id="pile_length"
                    type="number"
                    defaultValue="15"
                    {...register('pile_length', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="pile_spacing">Pile Spacing (m)</Label>
                  <Input
                    id="pile_spacing"
                    type="number"
                    step="0.5"
                    defaultValue="2.5"
                    {...register('pile_spacing', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label>Pile Type</Label>
                  <Select
                    defaultValue="driven"
                    onValueChange={(v) => setValue('pile_type', v)}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="driven">Driven</SelectItem>
                      <SelectItem value="bored">Bored</SelectItem>
                      <SelectItem value="cast_in_situ">Cast-in-situ</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="pile_cap_thickness">Pile Cap Thickness (m)</Label>
                  <Input
                    id="pile_cap_thickness"
                    type="number"
                    step="0.1"
                    defaultValue="0.8"
                    {...register('pile_cap_thickness', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="concrete_grade_pile">Concrete Grade (MPa)</Label>
                  <Input
                    id="concrete_grade_pile"
                    type="number"
                    {...register('concrete_grade', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <DialogFooter>
                <Button type="button" variant="outline" onClick={onClose}>
                  Cancel
                </Button>
                <Button type="submit" disabled={loading}>
                  {loading ? 'Designing...' : 'Design Pile Foundation'}
                </Button>
              </DialogFooter>
            </form>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
