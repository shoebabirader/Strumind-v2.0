import React from 'react'
import MenuBar from './MenuBar'
import Toolbar from './Toolbar'
import StatusBar from './StatusBar'

interface MainLayoutProps {
  children: React.ReactNode
}

export default function MainLayout({ children }: MainLayoutProps) {
  return (
    <div className="h-screen flex flex-col" style={{ background: 'var(--bg-primary)', color: 'var(--text-primary)' }}>
      <MenuBar />
      <Toolbar />
      <div className="flex-1 overflow-hidden">
        {children}
      </div>
      <StatusBar />
    </div>
  )
}
