import { Trash2 } from 'lucide-react'
import type { Holding } from '@/types'
import { formatCurrency, formatNumber } from '@/utils/format'

interface Props {
  holdings: Holding[]
  onRemove: (ticker: string) => void
}

function inferCurrency(ticker: string): string {
  return ticker.endsWith('.NS') || ticker.endsWith('.BO') ? 'INR' : 'USD'
}

export function HoldingsTable({ holdings, onRemove }: Props) {
  if (!holdings.length) {
    return (
      <p className="text-sm text-bone-400 italic text-center py-6">
        No holdings yet — add one above to get started.
      </p>
    )
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="text-left">
            <th className="label-overline pb-3">Ticker</th>
            <th className="label-overline pb-3 text-right">Qty</th>
            <th className="label-overline pb-3 text-right">Avg Cost</th>
            <th className="label-overline pb-3 text-right">Cost Basis</th>
            <th className="pb-3" />
          </tr>
        </thead>
        <tbody className="divide-y divide-ink-800">
          {holdings.map((h) => (
            <tr key={h.ticker} className="hover:bg-ink-900/50 transition-colors">
              <td className="py-3 font-mono font-semibold text-bone-50">
                {h.ticker}
              </td>
              <td className="py-3 text-right font-mono text-bone-200">
                {formatNumber(h.quantity, 2)}
              </td>
              <td className="py-3 text-right font-mono text-bone-200">
                {formatCurrency(h.avg_cost, inferCurrency(h.ticker))}
              </td>
              <td className="py-3 text-right font-mono text-bone-50">
                {formatCurrency(h.avg_cost * h.quantity, inferCurrency(h.ticker))}
              </td>
              <td className="py-3 text-right">
                <button
                  onClick={() => onRemove(h.ticker)}
                  className="text-bone-500 hover:text-crimson-accent transition-colors"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}