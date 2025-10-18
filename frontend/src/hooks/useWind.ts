import { useMutation } from '@tanstack/react-query';
import { windApi } from '@/lib/api';

export function useWind() {
  const designPressureMutation = useMutation({
    mutationFn: (data: any) => windApi.calculateDesignPressure(data),
  });

  const windForcesMutation = useMutation({
    mutationFn: (data: any) => windApi.calculateWindForces(data),
  });

  const gustFactorMutation = useMutation({
    mutationFn: (data: any) => windApi.calculateGustFactor(data),
  });

  const alongWindMutation = useMutation({
    mutationFn: (data: any) => windApi.calculateAlongWindResponse(data),
  });

  const acrossWindMutation = useMutation({
    mutationFn: (data: any) => windApi.calculateAcrossWindResponse(data),
  });

  return {
    calculateDesignPressure: designPressureMutation.mutateAsync,
    calculateWindForces: windForcesMutation.mutateAsync,
    calculateGustFactor: gustFactorMutation.mutateAsync,
    calculateAlongWind: alongWindMutation.mutateAsync,
    calculateAcrossWind: acrossWindMutation.mutateAsync,
    isLoading: designPressureMutation.isPending || windForcesMutation.isPending,
  };
}
