import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { versioningApi } from '@/lib/api';

export function useVersioning(projectId?: number) {
  const queryClient = useQueryClient();

  const { data: versions, isLoading } = useQuery({
    queryKey: ['versions', projectId],
    queryFn: () => projectId ? versioningApi.listVersions(projectId) : Promise.resolve([]),
    enabled: !!projectId,
  });

  const createVersionMutation = useMutation({
    mutationFn: (data: any) => versioningApi.createVersion(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['versions', projectId] });
    },
  });

  const restoreVersionMutation = useMutation({
    mutationFn: ({ projectId, versionNumber }: { projectId: number; versionNumber: number }) =>
      versioningApi.restoreVersion(projectId, versionNumber),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['versions', projectId] });
    },
  });

  const compareVersionsMutation = useMutation({
    mutationFn: ({ projectId, v1, v2 }: { projectId: number; v1: number; v2: number }) =>
      versioningApi.compareVersions(projectId, v1, v2),
  });

  return {
    versions: versions || [],
    isLoading,
    createVersion: createVersionMutation.mutateAsync,
    restoreVersion: restoreVersionMutation.mutateAsync,
    compareVersions: compareVersionsMutation.mutateAsync,
  };
}
