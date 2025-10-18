import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { materialsApi } from '@/lib/api';

export function useMaterials(projectId?: number) {
  const queryClient = useQueryClient();

  const { data: materials, isLoading } = useQuery({
    queryKey: ['materials', projectId],
    queryFn: () => projectId ? materialsApi.list(projectId) : Promise.resolve([]),
    enabled: !!projectId,
  });

  const { data: library } = useQuery({
    queryKey: ['materials', 'library'],
    queryFn: () => materialsApi.getLibrary(),
  });

  const createMutation = useMutation({
    mutationFn: (data: any) => materialsApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['materials', projectId] });
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) => materialsApi.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['materials', projectId] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => materialsApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['materials', projectId] });
    },
  });

  return {
    materials: materials || [],
    library: library || [],
    isLoading,
    createMaterial: createMutation.mutateAsync,
    updateMaterial: updateMutation.mutateAsync,
    deleteMaterial: deleteMutation.mutateAsync,
  };
}
