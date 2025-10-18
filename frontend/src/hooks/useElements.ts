import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { elementsApi } from '@/lib/api';
import type { Element, ElementCreate, ElementUpdate } from '@/types/model';

export function useElements(projectId?: number) {
  const queryClient = useQueryClient();

  const { data: elements, isLoading, error } = useQuery({
    queryKey: ['elements', projectId],
    queryFn: async () => {
      if (!projectId) return [];
      return await elementsApi.list(projectId);
    },
    enabled: !!projectId,
    retry: 1,
    staleTime: 5000,
  });

  const createMutation = useMutation({
    mutationFn: (data: ElementCreate) => elementsApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['elements', projectId] });
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: ElementUpdate }) => elementsApi.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['elements', projectId] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => elementsApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['elements', projectId] });
    },
  });

  return {
    elements: elements || [],
    isLoading,
    error,
    createElement: createMutation.mutateAsync,
    updateElement: updateMutation.mutateAsync,
    deleteElement: deleteMutation.mutateAsync,
  };
}
