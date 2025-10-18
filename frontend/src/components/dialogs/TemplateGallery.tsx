'use client';

import { useState, useEffect } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { templatesApi } from '@/lib/api';
import { FileText } from 'lucide-react';

interface TemplateGalleryProps {
  open: boolean;
  onClose: () => void;
}

export function TemplateGallery({ open, onClose }: TemplateGalleryProps) {
  const [templates, setTemplates] = useState<any[]>([]);

  useEffect(() => {
    if (open) loadTemplates();
  }, [open]);

  const loadTemplates = async () => {
    try {
      const data = await templatesApi.list();
      setTemplates(data);
    } catch (error) {
      console.error('Failed to load templates:', error);
    }
  };

  const handleUseTemplate = async (templateName: string) => {
    try {
      await templatesApi.get(templateName);
      onClose();
    } catch (error) {
      console.error('Failed to load template:', error);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[800px] h-[600px] flex flex-col">
        <DialogHeader><DialogTitle>Template Gallery</DialogTitle></DialogHeader>
        <div className="flex-1 overflow-y-auto">
          <div className="grid grid-cols-2 gap-4">
            {templates.length === 0 ? (
              <p className="col-span-2 text-sm text-gray-500 text-center py-8">No templates available</p>
            ) : (
              templates.map((template, index) => (
                <Card key={index} className="cursor-pointer hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <CardTitle className="text-base">{template.name}</CardTitle>
                        <CardDescription>{template.description}</CardDescription>
                      </div>
                      <FileText className="h-8 w-8 text-gray-400" />
                    </div>
                  </CardHeader>
                  <CardContent>
                    <Button size="sm" onClick={() => handleUseTemplate(template.name)}>Use Template</Button>
                  </CardContent>
                </Card>
              ))
            )}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
