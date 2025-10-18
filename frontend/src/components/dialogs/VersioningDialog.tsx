'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { useVersioning } from '@/hooks/useVersioning';
import { useModelStore } from '@/stores/modelStore';
import { Clock, GitBranch } from 'lucide-react';

interface VersioningDialogProps {
  open: boolean;
  onClose: () => void;
}

export function VersioningDialog({ open, onClose }: VersioningDialogProps) {
  const { currentProject } = useModelStore();
  const { versions, createVersion, restoreVersion } = useVersioning(currentProject?.id);
  const [versionName, setVersionName] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);

  const handleCreateVersion = async () => {
    if (!currentProject || !versionName) return;
    setLoading(true);
    try {
      await createVersion({
        project_id: currentProject.id,
        version_name: versionName,
        description,
      });
      setVersionName('');
      setDescription('');
    } catch (error) {
      console.error('Version creation failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRestore = async (versionNumber: number) => {
    if (!currentProject) return;
    if (confirm('Restore this version? Current changes will be saved as a new version.')) {
      await restoreVersion({ projectId: currentProject.id, versionNumber });
    }
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[600px] h-[600px] flex flex-col">
        <DialogHeader>
          <DialogTitle>Version Control</DialogTitle>
        </DialogHeader>
        <div className="flex-1 overflow-y-auto space-y-4">
          <div className="p-4 bg-gray-50 rounded-lg space-y-3">
            <div>
              <Label htmlFor="version_name">Version Name</Label>
              <Input id="version_name" value={versionName} onChange={(e) => setVersionName(e.target.value)} placeholder="v1.0" />
            </div>
            <div>
              <Label htmlFor="description">Description</Label>
              <Textarea id="description" value={description} onChange={(e) => setDescription(e.target.value)} placeholder="What changed..." rows={2} />
            </div>
            <Button onClick={handleCreateVersion} disabled={loading || !versionName} size="sm">
              <GitBranch className="h-4 w-4 mr-2" />
              Create Version
            </Button>
          </div>
          <div>
            <h3 className="text-sm font-semibold mb-3">Version History</h3>
            <div className="space-y-2">
              {versions.length === 0 ? (
                <p className="text-sm text-gray-500">No versions yet</p>
              ) : (
                versions.map((version) => (
                  <div key={version.id} className="p-3 border rounded-lg hover:bg-gray-50">
                    <div className="flex items-center justify-between mb-1">
                      <div className="flex items-center space-x-2">
                        <Badge>v{version.version_number}</Badge>
                        <span className="font-medium text-sm">{version.version_name}</span>
                      </div>
                      <Button size="sm" variant="outline" onClick={() => handleRestore(version.version_number)}>
                        Restore
                      </Button>
                    </div>
                    {version.description && <p className="text-xs text-gray-600 mb-1">{version.description}</p>}
                    <div className="flex items-center text-xs text-gray-500">
                      <Clock className="h-3 w-3 mr-1" />
                      {new Date(version.created_at).toLocaleString()}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
