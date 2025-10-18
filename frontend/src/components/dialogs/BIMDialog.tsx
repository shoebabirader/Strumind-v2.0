'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import { bimApi } from '@/lib/api';
import { useModelStore } from '@/stores/modelStore';
import { Upload, Download } from 'lucide-react';

interface BIMDialogProps {
  open: boolean;
  onClose: () => void;
}

export function BIMDialog({ open, onClose }: BIMDialogProps) {
  const { currentProject } = useModelStore();
  const [loading, setLoading] = useState(false);
  const [includeAnalysis, setIncludeAnalysis] = useState(false);

  const handleExportIFC = async () => {
    if (!currentProject) return;

    setLoading(true);
    try {
      await bimApi.exportIFC({
        project_id: currentProject.id,
        include_analysis_results: includeAnalysis,
        ifc_version: '4',
      });
      onClose();
    } catch (error) {
      console.error('IFC export failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleImportIFC = async (file: File) => {
    setLoading(true);
    try {
      await bimApi.importIFC(file);
      onClose();
    } catch (error) {
      console.error('IFC import failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>BIM Integration</DialogTitle>
        </DialogHeader>

        <Tabs defaultValue="export">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="export">Export IFC</TabsTrigger>
            <TabsTrigger value="import">Import IFC</TabsTrigger>
          </TabsList>

          <TabsContent value="export" className="space-y-4">
            <div className="flex items-center space-x-2">
              <Checkbox
                id="include_analysis"
                checked={includeAnalysis}
                onCheckedChange={(checked) => setIncludeAnalysis(checked as boolean)}
              />
              <Label htmlFor="include_analysis" className="font-normal">
                Include analysis results
              </Label>
            </div>

            <div className="p-4 bg-blue-50 rounded-lg text-sm">
              <p className="font-medium mb-2">Export will include:</p>
              <ul className="space-y-1 text-gray-700">
                <li>• Structural geometry</li>
                <li>• Material properties</li>
                <li>• Section properties</li>
                <li>• Load information</li>
                {includeAnalysis && <li>• Analysis results</li>}
              </ul>
            </div>

            <DialogFooter>
              <Button type="button" variant="outline" onClick={onClose}>
                Cancel
              </Button>
              <Button onClick={handleExportIFC} disabled={loading}>
                <Download className="h-4 w-4 mr-2" />
                {loading ? 'Exporting...' : 'Export IFC'}
              </Button>
            </DialogFooter>
          </TabsContent>

          <TabsContent value="import" className="space-y-4">
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
              <Upload className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p className="text-sm text-gray-600 mb-4">
                Drag and drop IFC file here, or click to browse
              </p>
              <input
                type="file"
                accept=".ifc"
                onChange={(e) => {
                  const file = e.target.files?.[0];
                  if (file) handleImportIFC(file);
                }}
                className="hidden"
                id="ifc-upload"
              />
              <label htmlFor="ifc-upload">
                <Button type="button" variant="outline" asChild>
                  <span>Select IFC File</span>
                </Button>
              </label>
            </div>

            <div className="p-4 bg-yellow-50 rounded-lg text-sm text-gray-700">
              <p className="font-medium mb-1">⚠️ Import Notes:</p>
              <p>IFC import will create nodes, elements, and materials from the file.</p>
            </div>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
