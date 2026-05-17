import { useForm } from 'react-hook-form'
import { Plus } from 'lucide-react'
import { Input } from '@/components/ui/Input'
import { Button } from '@/components/ui/Button'
import type { Holding } from '@/types'
import { searchSymbol } from '@/api/market'
import {  useState, useEffect, useRef } from 'react'
import type { TickerResult } from '../market/TickerSearch'
import { createPortal } from 'react-dom'

interface Props {
  onAdd: (h: Holding) => void
}

export function AddHoldingForm({ onAdd }: Props) {

  const [results, setResults] = useState<TickerResult[]>([])
  const [open, setOpen] = useState<boolean>(false)
  const [rect, setRect] = useState<DOMRect | null>(null)
  const [stock, setStock] = useState<string | null>(null)

  const { register, handleSubmit, watch, reset, setValue, formState: { errors } } = useForm<Holding>({
    defaultValues: { ticker: '', quantity: 0, avg_cost: 0 },
  })

  const inputRef = useRef<HTMLDivElement | null>(null)
  const tickerValue = watch('ticker')

  useEffect(() => {
    if (inputRef.current) {
    setRect(inputRef.current.getBoundingClientRect())
  }
    
    if (!tickerValue || tickerValue.trim().length < 2) {
      setStock(null)
      setResults([])
      return
    }
    if (tickerValue === '') return
    const timer = setTimeout(async () => {

      try {
        const  {results}  = await searchSymbol(tickerValue.trim())
        setResults(results)
        if(!stock){
          setOpen(true)
        }
      } catch {
        setResults([])
      } finally {
        
      }
    }, 300)
    return () => clearTimeout(timer)
  },[tickerValue])

  useEffect(() => {
  if (!open) return

  const updatePosition = () => {
    if (inputRef.current) {
      setRect(inputRef.current.getBoundingClientRect())
    }
  }

  updatePosition()

  window.addEventListener('scroll', updatePosition)
  window.addEventListener('resize', updatePosition)

  return () => {
    window.removeEventListener('scroll', updatePosition)
    window.removeEventListener('resize', updatePosition)
  }
}, [open])

  const submit = (data: Holding) => {
    onAdd({
      ticker: data.ticker.toUpperCase().trim(),
      quantity: Number(data.quantity),
      avg_cost: Number(data.avg_cost),
    })
    reset()
  }

  const pick = (symbol: string) => {
  setValue('ticker', symbol)
  setStock(symbol)
  setOpen(false)
  setResults([])
}

  return (
    <form
      onSubmit={handleSubmit(submit)}
      className="grid grid-cols-1 md:grid-cols-[1fr_1fr_1fr_auto] gap-3 items-end"
    >
      <div className='relative' ref={inputRef}>
          <Input
        label="Ticker"
        placeholder="AAPL"
        autoComplete="off"
        spellCheck="false"
        {...register('ticker', { required: 'Required' })}
        error={errors.ticker?.message}
      />

      {open && results.length > 0 && rect && createPortal(
        <div className=" mt-2 card p-2 z-[999] max-h-80 overflow-y-auto" style={{
        position: 'fixed',
        top: rect.bottom,
        left: rect.left,
        width: rect.width,
        zIndex: 999,
      }}>
          {results.map((r) => (
            <button
              type="button"
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
        </div>, document.body
      )}
      </div>
      
      
      <Input
        label="Quantity"
        type="number"
        step="0.01"
        placeholder="10"
        autoComplete="off"
        {...register('quantity', {
          required: 'Required',
          min: { value: 0.000001, message: 'Must be > 0' },
          valueAsNumber: true,
        })}
        error={errors.quantity?.message}
      />
      <Input
        label="Avg Cost"
        type="number"
        step="0.01"
        placeholder="150.00"
        autoComplete="off"
        {...register('avg_cost', {
          required: 'Required',
          min: { value: 0, message: 'Must be ≥ 0' },
          valueAsNumber: true,
        })}
        error={errors.avg_cost?.message}
      />
      <Button type="submit">
        <Plus className="w-4 h-4" />
        Add
      </Button>
      
    </form>
  )
}