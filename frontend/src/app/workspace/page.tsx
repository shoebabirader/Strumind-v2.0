'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import dynamic from 'next/dynamic';
import { useAuth } from '@/hooks/useAuth';
import { useModelStore } from '@/stores/modelStore';
import { MainLayout } from '@/components/layout/MainLayout';

const Canvas3D = dynamic(() => import('@/components/viewport/Canvas3D').then(mod => ({ default: mod.Canvas3D })), {
  ssr: false,
  loading: () => <div className="w-full h-full flex items-center justify-center">Loading 3D Viewport...</div>
});

export default function WorkspacePage() {
  const router = useRouter();
  const { isAuthenticated } = useAuth();
  const { currentProject, setCurrentProject } = useModelStore();

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, router]);

  // Create a default project if none exists
  useEffect(() => {
    if (isAuthenticated && !currentProject) {
      // Create a temporary default project
      const defaultProject = {
        id: 1,
        name: 'Default Project',
        description: 'Auto-created project',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };
      setCurrentProject(defaultProject);
      console.log('Created default project:', defaultProject);
    }
  }, [isAuthenticated, currentProject, setCurrentProject]);

  if (!isAuthenticated) {
    return null;
  }

  return (
    <MainLayout>
      <Canvas3D />
    </MainLayout>
  );
}
