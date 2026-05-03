import { FormEvent, useState, useEffect, useRef } from 'react'
import { Search, Loader2 } from 'lucide-react'
import { searchSymbol } from '@/api/market'

interface Props {
  onSearch: (ticker: string) => void
}
export interface TickerResult {
  symbol: string,
  name: string
}

export function TickerSearch({ onSearch }: Props) {
  const [value, setValue] = useState('')
  const [results, setResults] = useState<TickerResult[]>([])
  const [loading, setLoading] = useState(false)
  const [open, setOpen] = useState(false)
  const containerRef = useRef<HTMLDivElement>(null)

  // Debounced search as the user types
  useEffect(() => {
    if (value.trim().length < 2) {
      setResults([])
      return
    }
    const timer = setTimeout(async () => {
      setLoading(true)
      try {
        const { results } = await searchSymbol(value.trim())
        setResults(results)
        setOpen(true)
      } catch {
        setResults([])
      } finally {
        setLoading(false)
      }
    }, 300)
    return () => clearTimeout(timer)
  }, [value])

  // Close dropdown when clicking outside
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setOpen(false)
      }
    }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  const submit = (e: FormEvent) => {
    e.preventDefault()
    if (value.trim()) {
      pick(value.trim().toUpperCase())
    }
  }

  const pick = (symbol: string) => {
    onSearch(symbol)
    setValue('')
    setResults([])
    setOpen(false)
  }

  return (
    <div ref={containerRef} className="relative">
      <form onSubmit={submit} className="card p-2 flex items-center gap-2">
        <Search className="w-4 h-4 text-bone-400 ml-2" />
        <input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onFocus={() => results.length && setOpen(true)}
          placeholder="Search any stock — Reliance, TCS, Apple, RELIANCE.NS, TSLA…"
          className="flex-1 bg-transparent px-2 py-2 text-bone-100 placeholder:text-ink-500 focus:outline-none"
        />
        {loading && <Loader2 className="w-4 h-4 text-bone-400 animate-spin" />}
        <button type="submit" className="btn-primary !py-2">
          Look up
        </button>
      </form>

      {open && results.length > 0 && (
        <div className="absolute top-full left-0 right-0 mt-2 card p-2 z-20 max-h-80 overflow-y-auto">
          {results.map((r) => (
            <button
              key={r.symbol}
              onClick={() => pick(r.symbol)}
              className="w-full flex items-center justify-between gap-3 px-3 py-2 rounded-md text-left hover:bg-ink-800 transition-colors"
            >
              <span className="font-mono text-sm text-bone-50 font-semibold">
                {r.symbol}
              </span>
              <span className="text-xs text-bone-400 truncate">{r.name}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  )
}