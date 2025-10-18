import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { cacheApi } from '@/lib/api';

export function useCache() {
  const queryClient = useQueryClient();

  const { data: stats } = useQuery({
    queryKey: ['cache', 'stats'],
    queryFn: () => cacheApi.getStats(),
  });

  const clearMutation = useMutation({
    mutationFn: () => cacheApi.clear(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['cache'] });
    },
  });

  return {
    stats: stats || { size: 0, entries: 0, hitRate: 0 },
    clearCache: clearMutation.mutateAsync,
    isLoading: clearMutation.isPending,
  };
}
