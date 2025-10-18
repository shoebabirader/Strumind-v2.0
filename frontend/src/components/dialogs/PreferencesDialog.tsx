'use client';

import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Switch } from '@/components/ui/switch';

interface PreferencesDialogProps {
  open: boolean;
  onClose: () => void;
}

export function PreferencesDialog({ open, onClose }: PreferencesDialogProps) {
  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>User Preferences</DialogTitle>
        </DialogHeader>
        <Tabs defaultValue="editor">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="editor">Editor</TabsTrigger>
            <TabsTrigger value="shortcuts">Shortcuts</TabsTrigger>
            <TabsTrigger value="notifications">Notifications</TabsTrigger>
          </TabsList>
          <TabsContent value="editor" className="space-y-4">
            <div><Label>Default Precision</Label><Input type="number" defaultValue="3" min="0" max="10" /></div>
            <div className="flex items-center justify-between"><Label>Show Grid</Label><Switch defaultChecked /></div>
            <div className="flex items-center justify-between"><Label>Snap to Grid</Label><Switch defaultChecked /></div>
          </TabsContent>
          <TabsContent value="shortcuts" className="space-y-4">
            <p className="text-sm text-gray-500">Keyboard shortcuts configuration</p>
          </TabsContent>
          <TabsContent value="notifications" className="space-y-4">
            <div className="flex items-center justify-between"><Label>Email Notifications</Label><Switch /></div>
            <div className="flex items-center justify-between"><Label>Desktop Notifications</Label><Switch defaultChecked /></div>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
