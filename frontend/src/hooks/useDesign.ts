import { useMutation } from '@tanstack/react-query';
import { designApi, designExtendedApi, foundationApi, connectionsApi } from '@/lib/api';

export function useDesign() {
  const runDesignMutation = useMutation({
    mutationFn: (data: any) => designApi.run(data),
  });

  const concreteFlexureMutation = useMutation({
    mutationFn: (data: any) => designExtendedApi.is456Flexural(data),
  });

  const steelMemberMutation = useMutation({
    mutationFn: (data: any) => designExtendedApi.is800Tension(data),
  });

  const foundationMutation = useMutation({
    mutationFn: (data: any) => foundationApi.design(data),
  });

  const connectionMutation = useMutation({
    mutationFn: (data: any) => connectionsApi.momentConnection(data),
  });

  return {
    runDesign: runDesignMutation.mutateAsync,
    designConcreteFlexure: concreteFlexureMutation.mutateAsync,
    designSteelMember: steelMemberMutation.mutateAsync,
    designFoundation: foundationMutation.mutateAsync,
    designConnection: connectionMutation.mutateAsync,
    isLoading: runDesignMutation.isPending || concreteFlexureMutation.isPending,
  };
}
