import { useMutation } from '@tanstack/react-query';
import { bimApi } from '@/lib/api';

export function useBIM() {
  const exportIFCMutation = useMutation({
    mutationFn: (data: any) => bimApi.exportIFC(data),
  });

  const importIFCMutation = useMutation({
    mutationFn: (file: File) => bimApi.importIFC(file),
  });

  const generateSceneMutation = useMutation({
    mutationFn: (data: any) => bimApi.generateScene(data),
  });

  const stressVisualizationMutation = useMutation({
    mutationFn: (data: any) => bimApi.generateStressVisualization(data),
  });

  const deformationVisualizationMutation = useMutation({
    mutationFn: (data: any) => bimApi.generateDeformationVisualization(data),
  });

  return {
    exportIFC: exportIFCMutation.mutateAsync,
    importIFC: importIFCMutation.mutateAsync,
    generateScene: generateSceneMutation.mutateAsync,
    generateStressVisualization: stressVisualizationMutation.mutateAsync,
    generateDeformationVisualization: deformationVisualizationMutation.mutateAsync,
    isLoading: exportIFCMutation.isPending || importIFCMutation.isPending,
  };
}
