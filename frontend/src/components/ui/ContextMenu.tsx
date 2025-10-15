import React, { useEffect, useRef } from 'react'
import { Plus, Edit, Trash2, Copy } from 'lucide-react'

interface MenuItem {
  label: string
  icon?: React.ReactNode
  onClick: () => void
  divider?: boolean
}

interface ContextMenuProps {
  x: number
  y: number
  items: MenuItem[]
  onClose: () => void
}

export default function ContextMenu({ x, y, items, onClose }: ContextMenuProps) {
  const menuRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        onClose()
      }
    }

    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
    }

    document.addEventListener('mousedown', handleClickOutside)
    document.addEventListener('keydown', handleEscape)
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
      document.removeEventListener('keydown', handleEscape)
    }
  }, [onClose])

  return (
    <div
      ref={menuRef}
      className="fixed z-50 bg-gray-800 border border-gray-700 rounded shadow-lg py-1 min-w-[160px]"
      style={{ left: x, top: y }}
    >
      {items.map((item, idx) => (
        <React.Fragment key={idx}>
          {item.divider && <div className="border-t border-gray-700 my-1" />}
          <button
            className="w-full px-3 py-2 text-left text-sm hover:bg-gray-700 flex items-center space-x-2"
            onClick={() => {
              item.onClick()
              onClose()
            }}
          >
            {item.icon}
            <span>{item.label}</span>
          </button>
        </React.Fragment>
      ))}
    </div>
  )
}

export { Plus, Edit, Trash2, Copy }
