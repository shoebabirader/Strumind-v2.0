'use client';

import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Bell, CheckCircle, AlertCircle, Info } from 'lucide-react';

interface NotificationsDialogProps {
  open: boolean;
  onClose: () => void;
}

export function NotificationsDialog({ open, onClose }: NotificationsDialogProps) {
  const notifications = [
    { id: 1, type: 'success', message: 'Analysis completed successfully', time: '2 min ago' },
    { id: 2, type: 'warning', message: 'High stress detected in Element 45', time: '10 min ago' },
    { id: 3, type: 'info', message: 'New version available', time: '1 hour ago' },
  ];

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2"><Bell className="w-5 h-5" />Notifications</DialogTitle>
        </DialogHeader>
        <div className="space-y-2 max-h-[400px] overflow-y-auto">
          {notifications.map((notif) => (
            <Card key={notif.id}>
              <CardContent className="p-3 flex items-start gap-3">
                {notif.type === 'success' && <CheckCircle className="w-5 h-5 text-green-500 mt-0.5" />}
                {notif.type === 'warning' && <AlertCircle className="w-5 h-5 text-yellow-500 mt-0.5" />}
                {notif.type === 'info' && <Info className="w-5 h-5 text-blue-500 mt-0.5" />}
                <div className="flex-1">
                  <p className="text-sm">{notif.message}</p>
                  <p className="text-xs text-gray-500 mt-1">{notif.time}</p>
                </div>
                <Button size="sm" variant="ghost">×</Button>
              </CardContent>
            </Card>
          ))}
        </div>
      </DialogContent>
    </Dialog>
  );
}
