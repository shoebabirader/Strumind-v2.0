'use client';

import { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import { generativeApi } from '@/lib/api';

interface GenerativeDesignDialogProps {
  open: boolean;
  onClose: () => void;
}

export function GenerativeDesignDialog({ open, onClose }: GenerativeDesignDialogProps) {
  const [loading, setLoading] = useState(false);
  const [numDesigns, setNumDesigns] = useState('10');
  const [objectives, setObjectives] = useState({
    minimize_weight: true,
    minimize_cost: false,
    minimize_carbon: false,
    maximize_stiffness: true,
  });

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const selectedObjectives = Object.entries(objectives)
        .filter(([_, value]) => value)
        .map(([key]) => key);

      await generativeApi.generateDesigns({
        design_space: {},
        objectives: selectedObjectives,
        constraints: {},
        num_designs: parseInt(numDesigns),
      });
      onClose();
    } catch (error) {
      console.error('Generative design failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>AI Generative Design</DialogTitle>
        </DialogHeader>

        <div className="space-y-4">
          <div>
            <Label htmlFor="num_designs">Number of Design Alternatives</Label>
            <Input
              id="num_designs"
              type="number"
              value={numDesigns}
              onChange={(e) => setNumDesigns(e.target.value)}
              min="1"
              max="50"
            />
          </div>

          <div>
            <Label className="mb-3 block">Optimization Objectives</Label>
            <div className="space-y-3">
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="minimize_weight"
                  checked={objectives.minimize_weight}
                  onCheckedChange={(checked) =>
                    setObjectives({ ...objectives, minimize_weight: checked as boolean })
                  }
                />
                <Label htmlFor="minimize_weight" className="font-normal">
                  Minimize Weight
                </Label>
              </div>

              <div className="flex items-center space-x-2">
                <Checkbox
                  id="minimize_cost"
                  checked={objectives.minimize_cost}
                  onCheckedChange={(checked) =>
                    setObjectives({ ...objectives, minimize_cost: checked as boolean })
                  }
                />
                <Label htmlFor="minimize_cost" className="font-normal">
                  Minimize Cost
                </Label>
              </div>

              <div className="flex items-center space-x-2">
                <Checkbox
                  id="minimize_carbon"
                  checked={objectives.minimize_carbon}
                  onCheckedChange={(checked) =>
                    setObjectives({ ...objectives, minimize_carbon: checked as boolean })
                  }
                />
                <Label htmlFor="minimize_carbon" className="font-normal">
                  Minimize Carbon Footprint
                </Label>
              </div>

              <div className="flex items-center space-x-2">
                <Checkbox
                  id="maximize_stiffness"
                  checked={objectives.maximize_stiffness}
                  onCheckedChange={(checked) =>
                    setObjectives({ ...objectives, maximize_stiffness: checked as boolean })
                  }
                />
                <Label htmlFor="maximize_stiffness" className="font-normal">
                  Maximize Stiffness
                </Label>
              </div>
            </div>
          </div>

          <div className="p-4 bg-blue-50 rounded-lg text-sm">
            <p className="font-medium mb-2">AI will generate:</p>
            <ul className="space-y-1 text-gray-700">
              <li>• Multiple design alternatives</li>
              <li>• Pareto-optimal solutions</li>
              <li>• Performance comparisons</li>
              <li>• Recommended best design</li>
            </ul>
          </div>
        </div>

        <DialogFooter>
          <Button type="button" variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <Button onClick={handleGenerate} disabled={loading}>
            {loading ? 'Generating...' : 'Generate Designs'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
