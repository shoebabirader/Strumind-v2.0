'use client';

import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { HelpCircle, Book, Video, MessageCircle } from 'lucide-react';

interface HelpDialogProps {
  open: boolean;
  onClose: () => void;
}

export function HelpDialog({ open, onClose }: HelpDialogProps) {
  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[700px]">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <HelpCircle className="w-5 h-5" />
            Help & Support
          </DialogTitle>
        </DialogHeader>
        <Tabs defaultValue="search">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="search">Search</TabsTrigger>
            <TabsTrigger value="docs">Docs</TabsTrigger>
            <TabsTrigger value="tutorials">Tutorials</TabsTrigger>
            <TabsTrigger value="support">Support</TabsTrigger>
          </TabsList>
          <TabsContent value="search" className="space-y-4">
            <Input placeholder="Search help articles..." />
            <div className="space-y-2">
              <Card>
                <CardHeader><CardTitle className="text-sm">Getting Started</CardTitle></CardHeader>
                <CardContent><p className="text-xs text-gray-500">Learn the basics of StruMind</p></CardContent>
              </Card>
              <Card>
                <CardHeader><CardTitle className="text-sm">Creating Your First Model</CardTitle></CardHeader>
                <CardContent><p className="text-xs text-gray-500">Step-by-step guide</p></CardContent>
              </Card>
            </div>
          </TabsContent>
          <TabsContent value="docs" className="space-y-4">
            <Card>
              <CardHeader><CardTitle className="text-sm flex items-center gap-2"><Book className="w-4 h-4" />Documentation</CardTitle></CardHeader>
              <CardContent><Button size="sm" variant="outline">Open Documentation</Button></CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="tutorials" className="space-y-4">
            <Card>
              <CardHeader><CardTitle className="text-sm flex items-center gap-2"><Video className="w-4 h-4" />Video Tutorials</CardTitle></CardHeader>
              <CardContent><Button size="sm" variant="outline">Watch Tutorials</Button></CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="support" className="space-y-4">
            <Card>
              <CardHeader><CardTitle className="text-sm flex items-center gap-2"><MessageCircle className="w-4 h-4" />Contact Support</CardTitle></CardHeader>
              <CardContent><Button size="sm">Send Message</Button></CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
