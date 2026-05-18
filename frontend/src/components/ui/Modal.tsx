import { createPortal } from 'react-dom'
import { X } from 'lucide-react'
import { useEffect, type ReactNode } from 'react'

interface ModalProps {
  open: boolean
  onClose: () => void
  children: ReactNode
}

export function Modal({ open, onClose, children }: ModalProps) {
  useEffect(() => {
    if (!open) return
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose()
    }
    document.addEventListener('keydown', handler)
    return () => document.removeEventListener('keydown', handler)
  }, [open, onClose])

  if (!open) return null

  return createPortal(
    <div
      className="fixed inset-0 z-[999] flex items-center justify-center p-4"
      role="dialog"
      aria-modal="true"
    >
      <div
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        onClick={onClose}
        aria-hidden="true"
      />

      <div className="relative bg-ink-900 border border-ink-700 rounded-lg shadow-2xl w-full max-w-md z-10">
        <button
          onClick={onClose}
          aria-label="Close"
          className="absolute right-3 top-3 p-1.5 rounded-md text-bone-400 hover:text-bone-100 hover:bg-ink-800 transition-colors"
        >
          <X className="w-4 h-4" />
        </button>
        <div className="p-6">
          {children}
        </div>
      </div>
    </div>,
    document.body
  )
}