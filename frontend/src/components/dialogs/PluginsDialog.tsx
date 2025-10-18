'use client';

import { useState, useEffect } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { pluginsApi } from '@/lib/api';
import { Play, RefreshCw } from 'lucide-react';

interface PluginsDialogProps {
  open: boolean;
  onClose: () => void;
}

export function PluginsDialog({ open, onClose }: PluginsDialogProps) {
  const [plugins, setPlugins] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (open) loadPlugins();
  }, [open]);

  const loadPlugins = async () => {
    try {
      const data = await pluginsApi.list();
      setPlugins(data);
    } catch (error) {
      console.error('Failed to load plugins:', error);
    }
  };

  const handleReload = async () => {
    setLoading(true);
    try {
      await pluginsApi.reload();
      await loadPlugins();
    } catch (error) {
      console.error('Failed to reload plugins:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[700px] h-[600px] flex flex-col">
        <DialogHeader>
          <div className="flex items-center justify-between">
            <DialogTitle>Plugin Manager</DialogTitle>
            <Button size="sm" variant="outline" onClick={handleReload} disabled={loading}>
              <RefreshCw className="h-4 w-4 mr-2" />
              Reload
            </Button>
          </div>
        </DialogHeader>
        <div className="flex-1 overflow-y-auto space-y-3">
          {plugins.length === 0 ? (
            <p className="text-sm text-gray-500 text-center py-8">No plugins installed</p>
          ) : (
            plugins.map((plugin, index) => (
              <Card key={index}>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div>
                      <CardTitle className="text-base">{plugin.name}</CardTitle>
                      <CardDescription>{plugin.description}</CardDescription>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Badge variant={plugin.enabled ? 'default' : 'secondary'}>{plugin.enabled ? 'Enabled' : 'Disabled'}</Badge>
                      <Button size="sm" variant="outline"><Play className="h-4 w-4" /></Button>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="text-xs text-gray-500">
                    Type: {plugin.type} | Version: {plugin.version}
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}
