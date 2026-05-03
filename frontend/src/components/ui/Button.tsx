import type { ButtonHTMLAttributes, ReactNode } from 'react'
import { classNames } from '@/utils/format'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'ghost' | 'outline'
  children: ReactNode
}

export function Button({
  variant = 'primary',
  className,
  children,
  ...rest
}: ButtonProps) {
  const variantClass =
    variant === 'primary'
      ? 'btn-primary'
      : variant === 'ghost'
      ? 'btn-ghost'
      : 'btn border border-ink-700 text-bone-200 hover:border-emerald-accent/50 hover:text-bone-50'
  return (
    <button className={classNames(variantClass, className)} {...rest}>
      {children}
    </button>
  )
}