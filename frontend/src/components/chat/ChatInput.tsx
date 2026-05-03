import { type FormEvent, useState } from 'react'
import { Send } from 'lucide-react'
import { Spinner } from '@/components/ui/Spinner'

interface Props {
  onSubmit: (value: string) => void
  disabled?: boolean
}

export function ChatInput({ onSubmit, disabled }: Props) {
  const [value, setValue] = useState('')

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    const trimmed = value.trim()
    if (!trimmed || disabled) return
    onSubmit(trimmed)
    setValue('')
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="card p-2 flex items-center gap-2 focus-within:border-emerald-accent/40 focus-within:shadow-glow-emerald transition-all"
    >
      <input
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Ask about stocks, explain a concept, or paste a ticker…"
        disabled={disabled}
        className="flex-1 bg-transparent px-3 py-2 text-bone-100 placeholder:text-ink-500 focus:outline-none"
      />
      <button
        type="submit"
        disabled={disabled || !value.trim()}
        className="btn-primary !px-3 !py-2 disabled:opacity-40"
      >
        {disabled ? <Spinner size={16} /> : <Send className="w-4 h-4" />}
      </button>
    </form>
  )
}