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
      connection_type: 'bolted',
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
    <Dialog open={open} onOpenChange={onClose}>
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
                  <Select defaultValue="bolted" onValueChange={(v) => setValue('connection_type', v)}>
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
            <div className="text-sm text-gray-500 p-4">
              Simple shear connection design
            </div>
          </TabsContent>

          <TabsContent value="baseplate">
            <div className="text-sm text-gray-500 p-4">
              Column base plate design
            </div>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
