'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { ProjectDialog } from '@/components/dialogs/ProjectDialog';
import { NodeDialog } from '@/components/dialogs/NodeDialog';
import { ElementDialog } from '@/components/dialogs/ElementDialog';
import { AnalysisDialog } from '@/components/dialogs/AnalysisDialog';
import { SeismicDialog } from '@/components/dialogs/SeismicDialog';
import { WindDialog } from '@/components/dialogs/WindDialog';
import { DesignDialog } from '@/components/dialogs/DesignDialog';
import { FoundationDialog } from '@/components/dialogs/FoundationDialog';
import { ReportDialog } from '@/components/dialogs/ReportDialog';
import { AIAssistantDialog } from '@/components/dialogs/AIAssistantDialog';
import { 
  FileText, 
  Plus, 
  Play, 
  Wind as WindIcon, 
  Activity,
  Hammer,
  FileBarChart,
  Bot
} from 'lucide-react';

export function MainToolbar() {
  const [projectDialogOpen, setProjectDialogOpen] = useState(false);
  const [nodeDialogOpen, setNodeDialogOpen] = useState(false);
  const [elementDialogOpen, setElementDialogOpen] = useState(false);
  const [analysisDialogOpen, setAnalysisDialogOpen] = useState(false);
  const [seismicDialogOpen, setSeismicDialogOpen] = useState(false);
  const [windDialogOpen, setWindDialogOpen] = useState(false);
  const [designDialogOpen, setDesignDialogOpen] = useState(false);
  const [foundationDialogOpen, setFoundationDialogOpen] = useState(false);
  const [reportDialogOpen, setReportDialogOpen] = useState(false);
  const [aiDialogOpen, setAiDialogOpen] = useState(false);

  return (
    <>
      <div className="h-12 bg-white border-b border-gray-200 flex items-center px-4 space-x-2">
        <Button size="sm" variant="ghost" onClick={() => setProjectDialogOpen(true)}>
          <FileText className="h-4 w-4 mr-2" />
          New Project
        </Button>
        
        <div className="h-6 w-px bg-gray-300" />
        
        <Button size="sm" variant="ghost" onClick={() => setNodeDialogOpen(true)}>
          <Plus className="h-4 w-4 mr-2" />
          Node
        </Button>
        
        <Button size="sm" variant="ghost" onClick={() => setElementDialogOpen(true)}>
          <Plus className="h-4 w-4 mr-2" />
          Element
        </Button>
        
        <div className="h-6 w-px bg-gray-300" />
        
        <Button size="sm" variant="ghost" onClick={() => setAnalysisDialogOpen(true)}>
          <Play className="h-4 w-4 mr-2" />
          Analysis
        </Button>
        
        <Button size="sm" variant="ghost" onClick={() => setSeismicDialogOpen(true)}>
          <Activity className="h-4 w-4 mr-2" />
          Seismic
        </Button>
        
        <Button size="sm" variant="ghost" onClick={() => setWindDialogOpen(true)}>
          <WindIcon className="h-4 w-4 mr-2" />
          Wind
        </Button>
        
        <div className="h-6 w-px bg-gray-300" />
        
        <Button size="sm" variant="ghost" onClick={() => setDesignDialogOpen(true)}>
          <Hammer className="h-4 w-4 mr-2" />
          Design
        </Button>
        
        <Button size="sm" variant="ghost" onClick={() => setFoundationDialogOpen(true)}>
          Foundation
        </Button>
        
        <div className="h-6 w-px bg-gray-300" />
        
        <Button size="sm" variant="ghost" onClick={() => setReportDialogOpen(true)}>
          <FileBarChart className="h-4 w-4 mr-2" />
          Report
        </Button>
        
        <Button size="sm" variant="ghost" onClick={() => setAiDialogOpen(true)}>
          <Bot className="h-4 w-4 mr-2" />
          AI Assistant
        </Button>
      </div>

      <ProjectDialog open={projectDialogOpen} onClose={() => setProjectDialogOpen(false)} />
      <NodeDialog open={nodeDialogOpen} onClose={() => setNodeDialogOpen(false)} />
      <ElementDialog open={elementDialogOpen} onClose={() => setElementDialogOpen(false)} />
      <AnalysisDialog open={analysisDialogOpen} onClose={() => setAnalysisDialogOpen(false)} />
      <SeismicDialog open={seismicDialogOpen} onClose={() => setSeismicDialogOpen(false)} />
      <WindDialog open={windDialogOpen} onClose={() => setWindDialogOpen(false)} />
      <DesignDialog open={designDialogOpen} onClose={() => setDesignDialogOpen(false)} />
      <FoundationDialog open={foundationDialogOpen} onClose={() => setFoundationDialogOpen(false)} />
      <ReportDialog open={reportDialogOpen} onClose={() => setReportDialogOpen(false)} />
      <AIAssistantDialog open={aiDialogOpen} onClose={() => setAiDialogOpen(false)} />
    </>
  );
}
