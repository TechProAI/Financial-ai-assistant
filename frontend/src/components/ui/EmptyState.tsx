import type { ReactNode } from 'react'
import type { LucideIcon } from 'lucide-react'

export function EmptyState({
  icon: Icon,
  title,
  description,
  action,
}: {
  icon: LucideIcon
  title: string
  description: string
  action?: ReactNode
}) {
  return (
    <div className="flex flex-col items-center justify-center text-center py-16 px-6">
      <div className="w-14 h-14 rounded-full bg-ink-800 border border-ink-700 flex items-center justify-center mb-4">
        <Icon className="w-6 h-6 text-bone-400" />
      </div>
      <h3 className="font-display text-xl font-semibold text-bone-50 mb-2">
        {title}
      </h3>
      <p className="text-sm text-bone-400 max-w-sm mb-5">{description}</p>
      {action}
    </div>
  )
}