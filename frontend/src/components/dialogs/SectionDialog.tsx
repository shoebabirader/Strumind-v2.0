'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { sectionsApi } from '@/lib/api';
import { useModelStore } from '@/stores/modelStore';

interface SectionDialogProps {
  open: boolean;
  onClose: () => void;
}

export function SectionDialog({ open, onClose }: SectionDialogProps) {
  const { currentProject } = useModelStore();
  const [loading, setLoading] = useState(false);
  
  const { register, handleSubmit, setValue } = useForm({
    defaultValues: {
      name: '',
      section_type: 'rectangular',
      width: 0,
      depth: 0,
      area: 0,
      Ixx: 0,
      Iyy: 0,
      J: 0,
    },
  });

  const onSubmit = async (data: any) => {
    if (!currentProject) return;

    setLoading(true);
    try {
      await sectionsApi.create({ ...data, project_id: currentProject.id });
      onClose();
    } catch (error) {
      console.error('Failed to create section:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>Section Properties</DialogTitle>
        </DialogHeader>

        <Tabs defaultValue="custom">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="library">Library</TabsTrigger>
            <TabsTrigger value="custom">Custom</TabsTrigger>
          </TabsList>

          <TabsContent value="library">
            <div className="space-y-4">
              <div>
                <Label>Section Type</Label>
                <Select>
                  <SelectTrigger>
                    <SelectValue placeholder="Select section" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="ismb200">ISMB 200</SelectItem>
                    <SelectItem value="ismb250">ISMB 250</SelectItem>
                    <SelectItem value="ismb300">ISMB 300</SelectItem>
                    <SelectItem value="ismc100">ISMC 100</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </TabsContent>

          <TabsContent value="custom">
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="name">Section Name</Label>
                  <Input id="name" {...register('name')} placeholder="Custom Section" />
                </div>
                <div>
                  <Label>Section Type</Label>
                  <Select defaultValue="rectangular" onValueChange={(v) => setValue('section_type', v)}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="rectangular">Rectangular</SelectItem>
                      <SelectItem value="circular">Circular</SelectItem>
                      <SelectItem value="i_section">I-Section</SelectItem>
                      <SelectItem value="t_section">T-Section</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="width">Width (mm)</Label>
                  <Input
                    id="width"
                    type="number"
                    {...register('width', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="depth">Depth (mm)</Label>
                  <Input
                    id="depth"
                    type="number"
                    {...register('depth', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="area">Area (mm²)</Label>
                  <Input
                    id="area"
                    type="number"
                    {...register('area', { valueAsNumber: true })}
                  />
                </div>
                <div>
                  <Label htmlFor="Ixx">Ixx (mm⁴)</Label>
                  <Input
                    id="Ixx"
                    type="number"
                    {...register('Ixx', { valueAsNumber: true })}
                  />
                </div>
              </div>

              <DialogFooter>
                <Button type="button" variant="outline" onClick={onClose}>
                  Cancel
                </Button>
                <Button type="submit" disabled={loading}>
                  {loading ? 'Creating...' : 'Create Section'}
                </Button>
              </DialogFooter>
            </form>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
