'use client';

import { useAuth } from '@/hooks/useAuth';
import { useModelStore } from '@/stores/modelStore';
import { Button } from '@/components/ui/button';
import { User, Settings, LogOut } from 'lucide-react';

export function Header() {
  const { user, logout } = useAuth();
  const { currentProject } = useModelStore();

  return (
    <header className="h-14 bg-white border-b border-gray-200 flex items-center justify-between px-4">
      <div className="flex items-center space-x-4">
        <h1 className="text-xl font-bold text-gray-900">StruMind</h1>
        {currentProject && (
          <div className="flex items-center space-x-2">
            <span className="text-gray-400">|</span>
            <span className="text-sm text-gray-600">{currentProject.name}</span>
          </div>
        )}
      </div>

      <div className="flex items-center space-x-4">
        <span className="text-sm text-gray-600">{user?.email}</span>
        <Button variant="ghost" size="sm">
          <Settings className="h-4 w-4" />
        </Button>
        <Button variant="ghost" size="sm" onClick={logout}>
          <LogOut className="h-4 w-4" />
        </Button>
      </div>
    </header>
  );
}
