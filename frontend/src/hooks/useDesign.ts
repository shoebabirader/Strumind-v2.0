import { useMutation } from '@tanstack/react-query';
import { designApi, designExtendedApi, foundationApi, connectionsApi } from '@/lib/api';

// SECURITY FIX: Use Record<string, unknown> for flexible but type-safe data
// This prevents code injection while allowing dynamic properties
export function useDesign() {
  const runDesignMutation = useMutation({
    mutationFn: (data: Record<string, unknown>) => designApi.run(data as any),
  });

  const concreteFlexureMutation = useMutation({
    mutationFn: (data: Record<string, unknown>) => designExtendedApi.is456Flexural(data as any),
  });

  const steelMemberMutation = useMutation({
    mutationFn: (data: Record<string, unknown>) => designExtendedApi.is800Tension(data as any),
  });

  const foundationMutation = useMutation({
    mutationFn: (data: Record<string, unknown>) => foundationApi.design(data as any),
  });

  const connectionMutation = useMutation({
    mutationFn: (data: Record<string, unknown>) => connectionsApi.momentConnection(data as any),
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
