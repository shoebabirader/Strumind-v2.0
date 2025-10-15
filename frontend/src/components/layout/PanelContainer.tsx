import React from 'react'

interface PanelContainerProps {
  left?: React.ReactNode
  center: React.ReactNode
  right?: React.ReactNode
  bottom?: React.ReactNode
}

export default function PanelContainer({ left, center, right, bottom }: PanelContainerProps) {
  return (
    <div className="flex-1 flex flex-col overflow-hidden">
      <div className="flex-1 flex overflow-hidden">
        {left && <div className="flex-shrink-0">{left}</div>}
        <div className="flex-1 flex flex-col overflow-hidden">
          <div className="flex-1 overflow-hidden">{center}</div>
          {bottom && <div className="flex-shrink-0">{bottom}</div>}
        </div>
        {right && <div className="flex-shrink-0">{right}</div>}
      </div>
    </div>
  )
}
