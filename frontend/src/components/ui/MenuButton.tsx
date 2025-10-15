import React, { useState, useRef, useEffect } from 'react'
import { ChevronDown } from 'lucide-react'

interface MenuItem {
  label: string
  onClick?: () => void
  divider?: boolean
}

interface MenuButtonProps {
  label: string
  items: MenuItem[]
}

export default function MenuButton({ label, items }: MenuButtonProps) {
  const [isOpen, setIsOpen] = useState(false)
  const menuRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setIsOpen(false)
      }
    }

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside)
      return () => document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [isOpen])

  return (
    <div className="relative" ref={menuRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="px-2 py-1 hover:bg-gray-700 rounded flex items-center space-x-1"
      >
        <span>{label}</span>
        <ChevronDown className="w-3 h-3" />
      </button>

      {isOpen && (
        <div className="absolute top-full left-0 mt-1 bg-gray-800 border border-gray-700 rounded shadow-lg py-1 min-w-[160px] z-50">
          {items.map((item, idx) => (
            <React.Fragment key={idx}>
              {item.divider && <div className="border-t border-gray-700 my-1" />}
              <button
                className="w-full px-3 py-2 text-left text-xs hover:bg-gray-700"
                onClick={() => {
                  item.onClick?.()
                  setIsOpen(false)
                }}
              >
                {item.label}
              </button>
            </React.Fragment>
          ))}
        </div>
      )}
    </div>
  )
}
