'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { connectionsApi } from '@/lib/api';

interface ConnectionDialogProps {
  open: boolean;
  onClose: () => void;
}

export function ConnectionDialog({ open, onClose }: ConnectionDialogProps) {
  const [loading, setLoading] = useState(false);
  const { register, handleSubmit, setValue } = useForm({
    defaultValues: {
      beam_section: 'ISMB300',
      column_section: 'ISHB300',
      moment: 100,
      shear: 50,
      steel_grade: 250,
      connection_type: 'bolted' as 'bolted' | 'welded',
      axial_load: 1000,
      concrete_grade: 25,
    },
  });

  const onSubmit = async (data: any) => {
    setLoading(true);
    try {
      await connectionsApi.momentConnection(data);
      onClose();
    } catch (error) {
      console.error('Connection design failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>Steel Connection Design</DialogTitle>
        </DialogHeader>

        <Tabs defaultValue="moment">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="moment">Moment</TabsTrigger>
            <TabsTrigger value="shear">Shear</TabsTrigger>
            <TabsTrigger value="baseplate">Base Plate</TabsTrigger>
          </TabsList>

          <TabsContent value="moment">
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="beam_section">Beam Section</Label>
                  <Input id="beam_section" {...register('beam_section')} />
                </div>
                <div>
                  <Label htmlFor="column_section">Column Section</Label>
                  <Input id="column_section" {...register('column_section')} />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="moment">Moment (kNm)</Label>
                  <Input
                    id="moment"
                    type="number"
                    {...register('moment', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="shear">Shear (kN)</Label>
                  <Input
                    id="shear"
                    type="number"
                    {...register('shear', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="steel_grade">Steel Grade (MPa)</Label>
                  <Input
                    id="steel_grade"
                    type="number"
                    {...register('steel_grade', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label>Connection Type</Label>
                  <Select defaultValue="bolted" onValueChange={(v) => setValue('connection_type', v as 'bolted' | 'welded')}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="bolted">Bolted</SelectItem>
                      <SelectItem value="welded">Welded</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <DialogFooter>
                <Button type="button" variant="outline" onClick={onClose}>
                  Cancel
                </Button>
                <Button type="submit" disabled={loading}>
                  {loading ? 'Designing...' : 'Design Connection'}
                </Button>
              </DialogFooter>
            </form>
          </TabsContent>

          <TabsContent value="shear">
            <form onSubmit={handleSubmit(async (data) => {
              setLoading(true);
              try {
                await connectionsApi.shearConnection({ 
                  beam_section: data.beam_section || 'ISMB300',
                  shear: data.shear || 150,
                  steel_grade: data.steel_grade || 250,
                  connection_type: data.connection_type || 'bolted'
                });
                onClose();
              } catch (error) {
                console.error('Shear connection design failed:', error);
              } finally {
                setLoading(false);
              }
            })} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="beam_section_shear">Beam Section</Label>
                  <Input id="beam_section_shear" defaultValue="ISMB300" />
                </div>
                <div>
                  <Label htmlFor="support_section">Support Section</Label>
                  <Input id="support_section" defaultValue="ISHB300" />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="shear_force">Shear Force (kN)</Label>
                  <Input id="shear_force" type="number" defaultValue="150" />
                </div>
                <div>
                  <Label>Connection Type</Label>
                  <Select defaultValue="double_angle">
                    <SelectTrigger><SelectValue /></SelectTrigger>
                    <SelectContent>
                      <SelectItem value="double_angle">Double Angle</SelectItem>
                      <SelectItem value="single_plate">Single Plate</SelectItem>
                      <SelectItem value="end_plate">End Plate</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="bolt_diameter">Bolt Diameter (mm)</Label>
                  <Input id="bolt_diameter" type="number" defaultValue="20" />
                </div>
                <div>
                  <Label htmlFor="bolt_grade">Bolt Grade</Label>
                  <Select defaultValue="4.6">
                    <SelectTrigger><SelectValue /></SelectTrigger>
                    <SelectContent>
                      <SelectItem value="4.6">4.6</SelectItem>
                      <SelectItem value="8.8">8.8</SelectItem>
                      <SelectItem value="10.9">10.9</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="num_bolts">Number of Bolts</Label>
                  <Input id="num_bolts" type="number" defaultValue="4" />
                </div>
              </div>
              <DialogFooter>
                <Button type="button" variant="outline" onClick={onClose}>Cancel</Button>
                <Button type="submit" disabled={loading}>{loading ? 'Designing...' : 'Design Shear Connection'}</Button>
              </DialogFooter>
            </form>
          </TabsContent>

          <TabsContent value="baseplate">
            <form onSubmit={handleSubmit(async (data) => {
              setLoading(true);
              try {
                await connectionsApi.basePlate({ 
                  column_section: data.column_section || 'ISHB300',
                  axial_load: data.axial_load || 1000,
                  moment: data.moment || 50,
                  concrete_grade: data.concrete_grade || 25
                });
                onClose();
              } catch (error) {
                console.error('Base plate design failed:', error);
              } finally {
                setLoading(false);
              }
            })} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="column_section_bp">Column Section</Label>
                  <Input id="column_section_bp" defaultValue="ISHB300" />
                </div>
                <div>
                  <Label htmlFor="steel_grade_bp">Steel Grade (MPa)</Label>
                  <Input id="steel_grade_bp" type="number" defaultValue="250" />
                </div>
              </div>
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="axial_load">Axial Load (kN)</Label>
                  <Input id="axial_load" type="number" defaultValue="1000" />
                </div>
                <div>
                  <Label htmlFor="moment_x_bp">Moment Mx (kNm)</Label>
                  <Input id="moment_x_bp" type="number" defaultValue="50" />
                </div>
                <div>
                  <Label htmlFor="moment_y_bp">Moment My (kNm)</Label>
                  <Input id="moment_y_bp" type="number" defaultValue="50" />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="plate_length">Plate Length (mm)</Label>
                  <Input id="plate_length" type="number" defaultValue="500" />
                </div>
                <div>
                  <Label htmlFor="plate_width">Plate Width (mm)</Label>
                  <Input id="plate_width" type="number" defaultValue="500" />
                </div>
              </div>
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="plate_thickness">Plate Thickness (mm)</Label>
                  <Input id="plate_thickness" type="number" defaultValue="25" />
                </div>
                <div>
                  <Label htmlFor="concrete_grade_bp">Concrete Grade (MPa)</Label>
                  <Input id="concrete_grade_bp" type="number" defaultValue="25" />
                </div>
                <div>
                  <Label htmlFor="anchor_bolts">Anchor Bolts</Label>
                  <Input id="anchor_bolts" type="number" defaultValue="4" />
                </div>
              </div>
              <DialogFooter>
                <Button type="button" variant="outline" onClick={onClose}>Cancel</Button>
                <Button type="submit" disabled={loading}>{loading ? 'Designing...' : 'Design Base Plate'}</Button>
              </DialogFooter>
            </form>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
