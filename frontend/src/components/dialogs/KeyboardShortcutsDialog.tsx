'use client';

import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface KeyboardShortcutsDialogProps {
  open: boolean;
  onClose: () => void;
}

export function KeyboardShortcutsDialog({ open, onClose }: KeyboardShortcutsDialogProps) {
  const shortcuts = [
    { category: 'General', items: [
      { keys: 'Ctrl + S', action: 'Save Project' },
      { keys: 'Ctrl + Z', action: 'Undo' },
      { keys: 'Ctrl + Y', action: 'Redo' },
      { keys: 'Ctrl + K', action: 'Command Palette' },
    ]},
    { category: 'View', items: [
      { keys: 'I', action: 'Isometric View' },
      { keys: 'T', action: 'Top View' },
      { keys: 'F', action: 'Front View' },
      { keys: 'S', action: 'Side View' },
      { keys: 'E', action: 'Zoom Extents' },
    ]},
    { category: 'Modeling', items: [
      { keys: 'N', action: 'Create Node' },
      { keys: 'E', action: 'Create Element' },
      { keys: 'M', action: 'Create Material' },
      { keys: 'L', action: 'Create Load' },
    ]},
  ];

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[600px] max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Keyboard Shortcuts</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          {shortcuts.map((section) => (
            <Card key={section.category}>
              <CardHeader>
                <CardTitle className="text-sm">{section.category}</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {section.items.map((item, idx) => (
                    <div key={idx} className="flex justify-between items-center">
                      <span className="text-sm">{item.action}</span>
                      <kbd className="px-2 py-1 text-xs bg-gray-100 rounded border">{item.keys}</kbd>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </DialogContent>
    </Dialog>
  );
}
