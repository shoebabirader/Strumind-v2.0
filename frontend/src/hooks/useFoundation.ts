import { useMutation } from '@tanstack/react-query';
import { foundationApi } from '@/lib/api';

export function useFoundation() {
  const designMutation = useMutation({
    mutationFn: (data: any) => foundationApi.design(data),
  });

  const isolatedFootingMutation = useMutation({
    mutationFn: (data: any) => foundationApi.isolatedFooting(data),
  });

  const matFoundationMutation = useMutation({
    mutationFn: (data: any) => foundationApi.matFoundation(data),
  });

  const pileFoundationMutation = useMutation({
    mutationFn: (data: any) => foundationApi.pileFoundation(data),
  });

  return {
    design: designMutation.mutateAsync,
    designIsolatedFooting: isolatedFootingMutation.mutateAsync,
    designMatFoundation: matFoundationMutation.mutateAsync,
    designPileFoundation: pileFoundationMutation.mutateAsync,
    isLoading: designMutation.isPending || isolatedFootingMutation.isPending || 
               matFoundationMutation.isPending || pileFoundationMutation.isPending,
  };
}
