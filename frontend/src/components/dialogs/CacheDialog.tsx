'use client';

import { useState, useEffect } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { cacheApi } from '@/lib/api';
import { Trash2, Activity } from 'lucide-react';

interface CacheDialogProps {
  open: boolean;
  onClose: () => void;
}

export function CacheDialog({ open, onClose }: CacheDialogProps) {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (open) loadStats();
  }, [open]);

  const loadStats = async () => {
    try {
      const data = await cacheApi.getStats();
      setStats(data);
    } catch (error) {
      console.error('Failed to load cache stats:', error);
    }
  };

  const handleClear = async () => {
    if (confirm('Clear all cache? This cannot be undone.')) {
      setLoading(true);
      try {
        await cacheApi.clear();
        await loadStats();
      } catch (error) {
        console.error('Failed to clear cache:', error);
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader><DialogTitle>Cache Management</DialogTitle></DialogHeader>
        <div className="space-y-4">
          <Card>
            <CardHeader><CardTitle className="text-sm">Cache Statistics</CardTitle></CardHeader>
            <CardContent className="space-y-2 text-sm">
              <div className="flex justify-between"><span>Total Entries:</span><span className="font-medium">{stats?.total_entries || 0}</span></div>
              <div className="flex justify-between"><span>Cache Size:</span><span className="font-medium">{stats?.size || '0 MB'}</span></div>
              <div className="flex justify-between"><span>Hit Rate:</span><span className="font-medium">{stats?.hit_rate || '0%'}</span></div>
            </CardContent>
          </Card>
          <div className="flex items-center space-x-2">
            <Activity className="h-4 w-4 text-green-500" />
            <span className="text-sm text-gray-600">Cache is healthy</span>
          </div>
        </div>
        <DialogFooter>
          <Button type="button" variant="outline" onClick={onClose}>Close</Button>
          <Button variant="destructive" onClick={handleClear} disabled={loading}>
            <Trash2 className="h-4 w-4 mr-2" />
            Clear Cache
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
