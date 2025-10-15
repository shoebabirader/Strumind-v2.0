import React from 'react'

interface GridHelperProps {
  size?: number
  divisions?: number
  color?: string
}

export default function GridHelper({ 
  size = 100, 
  divisions = 10, 
  color = 'var(--grid-color)' 
}: GridHelperProps) {
  return (
    <div 
      className="absolute inset-0 opacity-20 pointer-events-none" 
      style={{
        backgroundImage: `linear-gradient(${color} 1px, transparent 1px), linear-gradient(90deg, ${color} 1px, transparent 1px)`,
        backgroundSize: `${size / divisions}px ${size / divisions}px`
      }} 
    />
  )
}
