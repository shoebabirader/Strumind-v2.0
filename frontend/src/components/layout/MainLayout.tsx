'use client';

import { ReactNode } from 'react';
import { Header } from './Header';
import { LeftPanel } from './LeftPanel';
import { RightPanel } from './RightPanel';
import { StatusBar } from './StatusBar';
import { MainToolbar } from './MainToolbar';

interface MainLayoutProps {
  children: ReactNode;
}

export function MainLayout({ children }: MainLayoutProps) {
  return (
    <div className="h-screen flex flex-col bg-gray-50">
      <Header />
      <MainToolbar />
      
      <div className="flex-1 flex overflow-hidden">
        <LeftPanel />
        
        <main className="flex-1 relative bg-gray-900">
          {children}
        </main>
        
        <RightPanel />
      </div>
      
      <StatusBar />
    </div>
  );
}
