import { useMutation } from '@tanstack/react-query';
import { optimizationApi } from '@/lib/api';

export function useOptimization() {
  const beamSectionMutation = useMutation({
    mutationFn: (data: any) => optimizationApi.beamSection(data),
  });

  const columnSectionMutation = useMutation({
    mutationFn: (data: any) => optimizationApi.columnSection(data),
  });

  const multiObjectiveMutation = useMutation({
    mutationFn: (data: any) => optimizationApi.multiObjective(data),
  });

  return {
    optimizeBeamSection: beamSectionMutation.mutateAsync,
    optimizeColumnSection: columnSectionMutation.mutateAsync,
    multiObjective: multiObjectiveMutation.mutateAsync,
    isLoading: beamSectionMutation.isPending || columnSectionMutation.isPending || 
               multiObjectiveMutation.isPending,
  };
}
