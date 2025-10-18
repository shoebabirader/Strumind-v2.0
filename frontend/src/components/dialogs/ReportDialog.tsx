'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { reportingApi } from '@/lib/api';
import { useModelStore } from '@/stores/modelStore';

interface ReportDialogProps {
  open: boolean;
  onClose: () => void;
}

export function ReportDialog({ open, onClose }: ReportDialogProps) {
  const { currentProject } = useModelStore();
  const [loading, setLoading] = useState(false);
  const [format, setFormat] = useState<'pdf' | 'docx' | 'html'>('pdf');
  const [includeAnalysis, setIncludeAnalysis] = useState(true);
  const [includeDesign, setIncludeDesign] = useState(true);
  const [includeDrawings, setIncludeDrawings] = useState(false);

  const handleGenerate = async () => {
    if (!currentProject) return;

    setLoading(true);
    try {
      await reportingApi.generateAnalysisReport({
        project_id: currentProject.id,
        analysis_data: {},
        design_data: {},
        format,
      });
      onClose();
    } catch (error) {
      console.error('Report generation failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Generate Report</DialogTitle>
        </DialogHeader>

        <div className="space-y-4">
          <div>
            <Label>Report Format</Label>
            <Select value={format} onValueChange={(v: any) => setFormat(v)}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="pdf">PDF Document</SelectItem>
                <SelectItem value="docx">Word Document</SelectItem>
                <SelectItem value="html">HTML Report</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-3">
            <Label>Include Sections</Label>
            
            <div className="flex items-center space-x-2">
              <Checkbox
                id="analysis"
                checked={includeAnalysis}
                onCheckedChange={(checked) => setIncludeAnalysis(checked as boolean)}
              />
              <Label htmlFor="analysis" className="font-normal">
                Analysis Results
              </Label>
            </div>

            <div className="flex items-center space-x-2">
              <Checkbox
                id="design"
                checked={includeDesign}
                onCheckedChange={(checked) => setIncludeDesign(checked as boolean)}
              />
              <Label htmlFor="design" className="font-normal">
                Design Calculations
              </Label>
            </div>

            <div className="flex items-center space-x-2">
              <Checkbox
                id="drawings"
                checked={includeDrawings}
                onCheckedChange={(checked) => setIncludeDrawings(checked as boolean)}
              />
              <Label htmlFor="drawings" className="font-normal">
                Drawings & Detailing
              </Label>
            </div>
          </div>

          <div className="p-4 bg-gray-50 rounded-lg text-sm text-gray-600">
            <p className="font-medium mb-2">Report will include:</p>
            <ul className="space-y-1">
              <li>• Project information</li>
              <li>• Model geometry</li>
              {includeAnalysis && <li>• Analysis results & diagrams</li>}
              {includeDesign && <li>• Design calculations & checks</li>}
              {includeDrawings && <li>• Reinforcement detailing</li>}
            </ul>
          </div>
        </div>

        <DialogFooter>
          <Button type="button" variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <Button onClick={handleGenerate} disabled={loading}>
            {loading ? 'Generating...' : 'Generate Report'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
