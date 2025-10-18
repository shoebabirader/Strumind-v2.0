import { useMutation } from '@tanstack/react-query';
import { seismicApi } from '@/lib/api';

export function useSeismic() {
  const baseShearMutation = useMutation({
    mutationFn: (data: any) => seismicApi.calculateBaseShear(data),
  });

  const responseSpectrumMutation = useMutation({
    mutationFn: (data: any) => seismicApi.responseSpectrum(data),
  });

  const storyDriftMutation = useMutation({
    mutationFn: (data: any) => seismicApi.checkStoryDrift(data),
  });

  const loadDistributionMutation = useMutation({
    mutationFn: (data: any) => seismicApi.distributeLoads(data),
  });

  return {
    calculateBaseShear: baseShearMutation.mutateAsync,
    responseSpectrumAnalysis: responseSpectrumMutation.mutateAsync,
    checkStoryDrift: storyDriftMutation.mutateAsync,
    distributeLoads: loadDistributionMutation.mutateAsync,
    isLoading: baseShearMutation.isPending || responseSpectrumMutation.isPending,
  };
}
