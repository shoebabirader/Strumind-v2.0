'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useMaterials } from '@/hooks/useMaterials';
import { useModelStore } from '@/stores/modelStore';

interface MaterialDialogProps {
    open: boolean;
    onClose: () => void;
}

export function MaterialDialog({ open, onClose }: MaterialDialogProps) {
    const { currentProject } = useModelStore();
    const { createMaterial, library } = useMaterials(currentProject?.id);
    const [loading, setLoading] = useState(false);
    const { register, handleSubmit, setValue, watch } = useForm({
        defaultValues: {
            name: '',
            material_type: 'concrete',
            elastic_modulus: 0,
            poissons_ratio: 0.2,
            density: 0,
            yield_strength: 0,
            ultimate_strength: 0,
        },
    });

    const onSubmit = async (data: any) => {
        if (!currentProject) return;

        setLoading(true);
        try {
            await createMaterial({ ...data, project_id: currentProject.id });
            onClose();
        } catch (error) {
            console.error('Failed to create material:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
            <DialogContent className="sm:max-w-[600px]">
                <DialogHeader>
                    <DialogTitle>Material Properties</DialogTitle>
                </DialogHeader>

                <Tabs defaultValue="custom">
                    <TabsList className="grid w-full grid-cols-2">
                        <TabsTrigger value="library">Library</TabsTrigger>
                        <TabsTrigger value="custom">Custom</TabsTrigger>
                    </TabsList>

                    <TabsContent value="library" className="space-y-4">
                        <div>
                            <Label>Select from Library</Label>
                            <Select>
                                <SelectTrigger>
                                    <SelectValue placeholder="Choose material" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="m25">M25 Concrete</SelectItem>
                                    <SelectItem value="m30">M30 Concrete</SelectItem>
                                    <SelectItem value="fe415">Fe 415 Steel</SelectItem>
                                    <SelectItem value="fe500">Fe 500 Steel</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                    </TabsContent>

                    <TabsContent value="custom">
                        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <Label htmlFor="name">Material Name</Label>
                                    <Input id="name" {...register('name')} placeholder="Custom Material" />
                                </div>
                                <div>
                                    <Label>Material Type</Label>
                                    <Select defaultValue="concrete" onValueChange={(v) => setValue('material_type', v)}>
                                        <SelectTrigger>
                                            <SelectValue />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="concrete">Concrete</SelectItem>
                                            <SelectItem value="steel">Steel</SelectItem>
                                            <SelectItem value="timber">Timber</SelectItem>
                                            <SelectItem value="masonry">Masonry</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <Label htmlFor="elastic_modulus">Elastic Modulus (MPa)</Label>
                                    <Input
                                        id="elastic_modulus"
                                        type="number"
                                        {...register('elastic_modulus', { valueAsNumber: true })}
                                    />
                                </div>
                                <div>
                                    <Label htmlFor="poissons_ratio">Poisson's Ratio</Label>
                                    <Input
                                        id="poissons_ratio"
                                        type="number"
                                        step="0.01"
                                        {...register('poissons_ratio', { valueAsNumber: true })}
                                    />
                                </div>
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <Label htmlFor="density">Density (kg/m³)</Label>
                                    <Input
                                        id="density"
                                        type="number"
                                        {...register('density', { valueAsNumber: true })}
                                    />
                                </div>
                                <div>
                                    <Label htmlFor="yield_strength">Yield Strength (MPa)</Label>
                                    <Input
                                        id="yield_strength"
                                        type="number"
                                        {...register('yield_strength', { valueAsNumber: true })}
                                    />
                                </div>
                            </div>

                            <DialogFooter>
                                <Button type="button" variant="outline" onClick={onClose}>
                                    Cancel
                                </Button>
                                <Button type="submit" disabled={loading}>
                                    {loading ? 'Creating...' : 'Create Material'}
                                </Button>
                            </DialogFooter>
                        </form>
                    </TabsContent>
                </Tabs>
            </DialogContent>
        </Dialog>
    );
}
