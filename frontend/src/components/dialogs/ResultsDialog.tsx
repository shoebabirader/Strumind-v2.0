'use client';

import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface ResultsDialogProps {
  open: boolean;
  onClose: () => void;
}

export function ResultsDialog({ open, onClose }: ResultsDialogProps) {
  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[900px] max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Analysis Results</DialogTitle>
        </DialogHeader>
        <Tabs defaultValue="displacements">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="displacements">Displacements</TabsTrigger>
            <TabsTrigger value="forces">Forces</TabsTrigger>
            <TabsTrigger value="stresses">Stresses</TabsTrigger>
            <TabsTrigger value="reactions">Reactions</TabsTrigger>
          </TabsList>
          <TabsContent value="displacements">
            <Card><CardHeader><CardTitle className="text-sm">Node Displacements</CardTitle></CardHeader><CardContent>
              <div className="space-y-2">
                <div className="grid grid-cols-7 gap-2 text-xs font-semibold p-2 bg-gray-50 rounded">
                  <div>Node</div><div>Ux (mm)</div><div>Uy (mm)</div><div>Uz (mm)</div><div>Rx (rad)</div><div>Ry (rad)</div><div>Rz (rad)</div>
                </div>
                {[1,2,3,4,5].map(i => (
                  <div key={i} className="grid grid-cols-7 gap-2 text-xs p-2 border-b">
                    <div>{i}</div><div>{(Math.random()*10).toFixed(2)}</div><div>{(Math.random()*10).toFixed(2)}</div><div>{(Math.random()*10).toFixed(2)}</div><div>{(Math.random()*0.01).toFixed(4)}</div><div>{(Math.random()*0.01).toFixed(4)}</div><div>{(Math.random()*0.01).toFixed(4)}</div>
                  </div>
                ))}
              </div>
            </CardContent></Card>
          </TabsContent>
          <TabsContent value="forces">
            <Card><CardHeader><CardTitle className="text-sm">Element Forces</CardTitle></CardHeader><CardContent>
              <div className="space-y-2">
                <div className="grid grid-cols-7 gap-2 text-xs font-semibold p-2 bg-gray-50 rounded">
                  <div>Element</div><div>Axial (kN)</div><div>Shear Y (kN)</div><div>Shear Z (kN)</div><div>Torsion (kNm)</div><div>Moment Y (kNm)</div><div>Moment Z (kNm)</div>
                </div>
                {[1,2,3,4,5].map(i => (
                  <div key={i} className="grid grid-cols-7 gap-2 text-xs p-2 border-b">
                    <div>{i}</div><div>{(Math.random()*100).toFixed(1)}</div><div>{(Math.random()*50).toFixed(1)}</div><div>{(Math.random()*50).toFixed(1)}</div><div>{(Math.random()*20).toFixed(1)}</div><div>{(Math.random()*100).toFixed(1)}</div><div>{(Math.random()*100).toFixed(1)}</div>
                  </div>
                ))}
              </div>
            </CardContent></Card>
          </TabsContent>
          <TabsContent value="stresses">
            <Card><CardHeader><CardTitle className="text-sm">Element Stresses</CardTitle></CardHeader><CardContent>
              <div className="space-y-2">
                <div className="grid grid-cols-5 gap-2 text-xs font-semibold p-2 bg-gray-50 rounded">
                  <div>Element</div><div>σx (MPa)</div><div>σy (MPa)</div><div>τxy (MPa)</div><div>Von Mises (MPa)</div>
                </div>
                {[1,2,3,4,5].map(i => (
                  <div key={i} className="grid grid-cols-5 gap-2 text-xs p-2 border-b">
                    <div>{i}</div><div>{(Math.random()*200).toFixed(1)}</div><div>{(Math.random()*200).toFixed(1)}</div><div>{(Math.random()*100).toFixed(1)}</div><div>{(Math.random()*250).toFixed(1)}</div>
                  </div>
                ))}
              </div>
            </CardContent></Card>
          </TabsContent>
          <TabsContent value="reactions">
            <Card><CardHeader><CardTitle className="text-sm">Support Reactions</CardTitle></CardHeader><CardContent>
              <div className="space-y-2">
                <div className="grid grid-cols-7 gap-2 text-xs font-semibold p-2 bg-gray-50 rounded">
                  <div>Node</div><div>Rx (kN)</div><div>Ry (kN)</div><div>Rz (kN)</div><div>Mx (kNm)</div><div>My (kNm)</div><div>Mz (kNm)</div>
                </div>
                {[1,2,3].map(i => (
                  <div key={i} className="grid grid-cols-7 gap-2 text-xs p-2 border-b">
                    <div>{i}</div><div>{(Math.random()*500).toFixed(1)}</div><div>{(Math.random()*500).toFixed(1)}</div><div>{(Math.random()*1000).toFixed(1)}</div><div>{(Math.random()*200).toFixed(1)}</div><div>{(Math.random()*200).toFixed(1)}</div><div>{(Math.random()*100).toFixed(1)}</div>
                  </div>
                ))}
              </div>
            </CardContent></Card>
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
}
