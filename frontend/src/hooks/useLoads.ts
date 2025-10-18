import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { loadsApi } from '@/lib/api';

export function useLoads(projectId?: number) {
  const queryClient = useQueryClient();

  const { data: loads, isLoading } = useQuery({
    queryKey: ['loads', projectId],
    queryFn: () => projectId ? loadsApi.list(projectId) : Promise.resolve([]),
    enabled: !!projectId,
  });

  const createMutation = useMutation({
    mutationFn: (data: any) => loadsApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['loads', projectId] });
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) => loadsApi.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['loads', projectId] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => loadsApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['loads', projectId] });
    },
  });

  return {
    loads: loads || [],
    isLoading,
    createLoad: createMutation.mutateAsync,
    updateLoad: updateMutation.mutateAsync,
    deleteLoad: deleteMutation.mutateAsync,
  };
}
