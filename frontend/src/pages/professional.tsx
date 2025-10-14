import { useState } from 'react'
import dynamic from 'next/dynamic'
import ProfessionalLayout from '@/components/ProfessionalLayout'
import '../styles/professional.css'

const Enhanced3DViewer = dynamic(() => import('@/components/Enhanced3DViewer'), { ssr: false })

export default function ProfessionalView() {
  const [activeModule, setActiveModule] = useState<'model' | 'analysis' | 'design' | 'detailing'>('model')

  return (
    <ProfessionalLayout>
      <Enhanced3DViewer showGrid={true} showAxes={true} />
    </ProfessionalLayout>
  )
}
