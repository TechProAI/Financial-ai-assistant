import { type InputHTMLAttributes, forwardRef } from 'react'
import { classNames } from '@/utils/format'

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, className, ...rest }, ref) => (
    <div className="space-y-1.5">
      {label && <label className="label-overline block">{label}</label>}
      <input
        ref={ref}
        className={classNames('input-base', error && 'border-crimson-accent/60', className)}
        {...rest}
      />
      {error && <p className="text-xs text-crimson-accent">{error}</p>}
    </div>
  )
)
Input.displayName = 'Input'