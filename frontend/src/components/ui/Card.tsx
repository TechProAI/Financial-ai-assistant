import type { ReactNode } from 'react'
import { classNames } from '@/utils/format'

interface CardProps {
  children: ReactNode
  className?: string
  hover?: boolean
}

export function Card({ children, className, hover }: CardProps) {
  return (
    <div className={classNames('card p-5', hover && 'card-hover', className)}>
      {children}
    </div>
  )
}

export function CardHeader({
  title,
  subtitle,
  action,
}: {
  title: string
  subtitle?: string
  action?: ReactNode
}) {
  return (
    <div className="flex items-start justify-between mb-4">
      <div>
        <h3 className="font-display text-lg font-semibold text-bone-50">
          {title}
        </h3>
        {subtitle && (
          <p className="text-sm text-bone-400 mt-0.5">{subtitle}</p>
        )}
      </div>
      {action}
    </div>
  )
}