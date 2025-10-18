import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { pluginsApi } from '@/lib/api';

export function usePlugins() {
  const queryClient = useQueryClient();

  const { data: plugins, isLoading } = useQuery({
    queryKey: ['plugins'],
    queryFn: () => pluginsApi.list(),
  });

  return {
    plugins: plugins || [],
    isLoading,
  };
}
