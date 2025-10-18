'use client';

import { useState, useEffect } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { collaborationApi } from '@/lib/api';
import { useModelStore } from '@/stores/modelStore';
import { Users, MessageSquare } from 'lucide-react';

interface CollaborationDialogProps {
  open: boolean;
  onClose: () => void;
}

export function CollaborationDialog({ open, onClose }: CollaborationDialogProps) {
  const { currentProject } = useModelStore();
  const [activeUsers, setActiveUsers] = useState<any[]>([]);
  const [comments, setComments] = useState<any[]>([]);
  const [newComment, setNewComment] = useState('');
  const [selectedElement, setSelectedElement] = useState('');

  useEffect(() => {
    if (open && currentProject) {
      loadActiveUsers();
    }
  }, [open, currentProject]);

  const loadActiveUsers = async () => {
    if (!currentProject) return;
    try {
      const users = await collaborationApi.getActiveUsers(currentProject.id);
      setActiveUsers(users);
    } catch (error) {
      console.error('Failed to load active users:', error);
    }
  };

  const handleAddComment = async () => {
    if (!newComment.trim() || !selectedElement) return;

    try {
      await collaborationApi.addComment({
        element_id: selectedElement,
        user_id: 'current_user',
        text: newComment,
      });
      setNewComment('');
      // Reload comments
    } catch (error) {
      console.error('Failed to add comment:', error);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(isOpen) => !isOpen && onClose()}>
      <DialogContent className="sm:max-w-[700px] h-[600px] flex flex-col">
        <DialogHeader>
          <DialogTitle>Collaboration</DialogTitle>
        </DialogHeader>

        <div className="flex-1 overflow-y-auto space-y-4">
          {/* Active Users */}
          <div className="p-4 bg-gray-50 rounded-lg">
            <div className="flex items-center space-x-2 mb-3">
              <Users className="h-4 w-4" />
              <h3 className="font-medium text-sm">Active Users</h3>
            </div>
            <div className="flex flex-wrap gap-2">
              {activeUsers.length === 0 ? (
                <p className="text-sm text-gray-500">No other users online</p>
              ) : (
                activeUsers.map((user, index) => (
                  <Badge key={index} variant="secondary">
                    {user.email}
                  </Badge>
                ))
              )}
            </div>
          </div>

          {/* Comments Section */}
          <div className="p-4 bg-gray-50 rounded-lg">
            <div className="flex items-center space-x-2 mb-3">
              <MessageSquare className="h-4 w-4" />
              <h3 className="font-medium text-sm">Comments</h3>
            </div>

            <div className="space-y-3 mb-4">
              {comments.length === 0 ? (
                <p className="text-sm text-gray-500">No comments yet</p>
              ) : (
                comments.map((comment, index) => (
                  <div key={index} className="bg-white p-3 rounded border">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm font-medium">{comment.user_id}</span>
                      <span className="text-xs text-gray-500">{comment.timestamp}</span>
                    </div>
                    <p className="text-sm text-gray-700">{comment.text}</p>
                  </div>
                ))
              )}
            </div>

            <div className="space-y-2">
              <Input
                placeholder="Element ID"
                value={selectedElement}
                onChange={(e) => setSelectedElement(e.target.value)}
              />
              <Textarea
                placeholder="Add a comment..."
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                rows={3}
              />
              <Button onClick={handleAddComment} size="sm">
                Add Comment
              </Button>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
