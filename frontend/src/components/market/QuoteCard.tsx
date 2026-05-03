import { TrendingUp, TrendingDown, X } from 'lucide-react'
import type { Quote } from '@/types'
import { formatCurrency, formatCompact, formatPct, classNames } from '@/utils/format'

interface Props {
  quote: Quote
  onSelect?: () => void
  onRemove?: () => void
  active?: boolean
}

export function QuoteCard({ quote, onSelect, onRemove, active }: Props) {
  const positive = quote.change >= 0
  const Icon = positive ? TrendingUp : TrendingDown

  return (
    <div
      className={classNames(
        'card card-hover p-4 cursor-pointer relative group',
        active && 'border-emerald-accent/50 shadow-glow-emerald'
      )}
      onClick={onSelect}
    >
      {onRemove && (
        <button
          onClick={(e) => {
            e.stopPropagation()
            onRemove()
          }}
          className="absolute top-2 right-2 text-bone-500 hover:text-crimson-accent opacity-0 group-hover:opacity-100 transition-opacity"
        >
          <X className="w-4 h-4" />
        </button>
      )}
      <div className="flex items-start justify-between mb-3">
        <div>
          <div className="font-mono font-bold text-bone-50">{quote.ticker}</div>
          {quote.company_name && (
            <div className="text-[11px] text-bone-400 line-clamp-1 max-w-[180px]">
              {quote.company_name}
            </div>
          )}
        </div>
        <div
          className={classNames(
            'flex items-center gap-1 text-xs font-mono px-2 py-0.5 rounded',
            positive
              ? 'bg-emerald-accent/10 text-emerald-accent'
              : 'bg-crimson-accent/10 text-crimson-accent'
          )}
        >
          <Icon className="w-3 h-3" />
          {formatPct(quote.change_percent)}
        </div>
      </div>
      <div className="metric-value text-bone-50">
        {formatCurrency(quote.price, quote.currency)}
      </div>
      <div className="flex justify-between text-[11px] text-bone-400 mt-2 font-mono">
        <span>Vol {formatCompact(quote.volume)}</span>
        <span>
          {quote.currency === 'INR' ? '₹' : quote.currency === 'USD' ? '$' : ''}
          {formatCompact(quote.market_cap ?? null)}
        </span>
      </div>
    </div>
  )
}