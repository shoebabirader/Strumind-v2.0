import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { sectionsApi } from '@/lib/api';

export function useSections(projectId?: number) {
  const queryClient = useQueryClient();

  const { data: sections, isLoading } = useQuery({
    queryKey: ['sections', projectId],
    queryFn: () => projectId ? sectionsApi.list(projectId) : Promise.resolve([]),
    enabled: !!projectId,
  });

  const { data: library } = useQuery({
    queryKey: ['sections', 'library'],
    queryFn: () => sectionsApi.getLibrary(),
  });

  const createMutation = useMutation({
    mutationFn: (data: any) => sectionsApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sections', projectId] });
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) => sectionsApi.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sections', projectId] });
    },
  });

  const deleteMutation = useMutation({
    mutationFn: (id: number) => sectionsApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sections', projectId] });
    },
  });

  return {
    sections: sections || [],
    library: library || [],
    isLoading,
    createSection: createMutation.mutateAsync,
    updateSection: updateMutation.mutateAsync,
    deleteSection: deleteMutation.mutateAsync,
  };
}
