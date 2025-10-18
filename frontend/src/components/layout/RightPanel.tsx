'use client';

import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { NodesTable } from '@/components/tables/NodesTable';
import { ElementsTable } from '@/components/tables/ElementsTable';
import { MaterialsTable } from '@/components/tables/MaterialsTable';
import { LoadsTable } from '@/components/tables/LoadsTable';

export function RightPanel() {
  return (
    <aside className="w-80 bg-white border-l border-gray-200 overflow-y-auto">
      <Tabs defaultValue="properties" className="w-full">
        <TabsList className="w-full grid grid-cols-3">
          <TabsTrigger value="properties">Properties</TabsTrigger>
          <TabsTrigger value="results">Results</TabsTrigger>
          <TabsTrigger value="tables">Tables</TabsTrigger>
        </TabsList>

        <TabsContent value="properties" className="p-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">Element Properties</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-500">
                Select an element to view properties
              </p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="results" className="p-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">Analysis Results</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-500">
                Run analysis to view results
              </p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="tables" className="p-4 space-y-4">
          <div>
            <h3 className="text-sm font-semibold mb-2">Nodes</h3>
            <NodesTable />
          </div>
          <div>
            <h3 className="text-sm font-semibold mb-2">Elements</h3>
            <ElementsTable />
          </div>
          <div>
            <h3 className="text-sm font-semibold mb-2">Materials</h3>
            <MaterialsTable />
          </div>
          <div>
            <h3 className="text-sm font-semibold mb-2">Loads</h3>
            <LoadsTable />
          </div>
        </TabsContent>
      </Tabs>
    </aside>
  );
}
