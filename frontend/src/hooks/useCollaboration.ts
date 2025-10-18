import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { collaborationApi } from '@/lib/api';

export function useCollaboration(projectId?: number) {
  const queryClient = useQueryClient();

  const { data: activeUsers } = useQuery({
    queryKey: ['activeUsers', projectId],
    queryFn: () => projectId ? collaborationApi.getActiveUsers(projectId) : Promise.resolve([]),
    enabled: !!projectId,
    refetchInterval: 5000, // Refresh every 5 seconds
  });

  const addCommentMutation = useMutation({
    mutationFn: (data: any) => collaborationApi.addComment(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['comments'] });
    },
  });

  const getCommentsMutation = useMutation({
    mutationFn: (elementId: string) => collaborationApi.getComments(elementId),
  });

  return {
    activeUsers: activeUsers || [],
    addComment: addCommentMutation.mutateAsync,
    getComments: getCommentsMutation.mutateAsync,
  };
}
