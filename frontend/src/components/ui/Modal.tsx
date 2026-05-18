import { createPortal } from 'react-dom'

export function Modal({ open, onClose, children }: any) {
  if (!open) return null

  return createPortal(
    <div className="fixed inset-0 z-[999] flex items-center justify-center">
      
      <div
        className="absolute inset-0 bg-black/50"
        onClick={onClose}
      />

      <div className="relative bg-white rounded-lg w-96 z-10 pb-2">
        <span className='bg-red-500 text-white absolute right-1 top-1 pr-3 pl-3 pt-1 pb-1 rounded-md cursor-pointer hover:bg-red-600' onClick={onClose}>X</span>
        <div className='pt-10 pb-10 flex flex-col items-center space-y-5'>
            {children}
        </div>
        
      </div>
    </div>,
    document.body
  )
}