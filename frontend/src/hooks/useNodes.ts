import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { nodesApi } from '@/lib/api';
import type { Node, NodeCreate, NodeUpdate } from '@/types/model';

export function useNodes(projectId?: number) {
  const queryClient = useQueryClient();

  const { data: nodes, isLoading, error } = useQuery({
    queryKey: ['nodes', projectId],
    queryFn: () => projectId ? nodesApi.list(projectId) : Promise.resolve([]),
    enabled: !!projectId,
  });

  const createMutation = useMutation({
    mutationFn: (data: NodeCreate) => nodesApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['nodes', projectId] });
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: NodeUpdate }) => nodesApi.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['nodes', projectId] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => nodesApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['nodes', projectId] });
    },
  });

  return {
    nodes: nodes || [],
    isLoading,
    error,
    createNode: createMutation.mutateAsync,
    updateNode: updateMutation.mutateAsync,
    deleteNode: deleteMutation.mutateAsync,
  };
}
