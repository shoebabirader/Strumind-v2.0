'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { workflowApi } from '@/lib/api';

interface WorkflowDialogProps {
  open: boolean;
  onClose: () => void;
}

export function WorkflowDialog({ open, onClose }: WorkflowDialogProps) {
  const [loading, setLoading] = useState(false);
  const [workflowName, setWorkflowName] = useState('');

  const handleCreate = async () => {
    setLoading(true);
    try {
      await workflowApi.create();
      onClose();
    } catch (error) {
      console.error('Workflow creation failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>Workflow Automation</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div><Label>Workflow Name</Label><Input value={workflowName} onChange={(e) => setWorkflowName(e.target.value)} placeholder="My Workflow" /></div>
          <div className="border rounded p-4"><p className="text-sm text-gray-500">Configure workflow steps here</p></div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={onClose}>Cancel</Button>
          <Button onClick={handleCreate} disabled={loading}>Create Workflow</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
