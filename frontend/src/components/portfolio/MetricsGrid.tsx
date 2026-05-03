import type { PortfolioAnalysis } from '@/types'
import { formatCurrency, formatPct, classNames } from '@/utils/format'

export function MetricsGrid({
  analysis,
  currency = 'USD',
}: {
  analysis: PortfolioAnalysis
  currency?: string
}) {
  const gainPositive = analysis.total_return_pct >= 0
  const cards = [
    {
      label: 'Total Value',
      value: formatCurrency(analysis.total_value, currency),
      sub: `Cost ${formatCurrency(analysis.total_cost, currency)}`,
      accent: 'emerald' as const,
    },
    {
      label: 'Total Return',
      value: formatPct(analysis.total_return_pct),
      sub: `${analysis.metrics.num_positions} positions`,
      accent: gainPositive ? ('emerald' as const) : ('crimson' as const),
    },
    {
      label: 'Sharpe Ratio',
      value: analysis.metrics.sharpe_ratio.toFixed(2),
      sub: 'risk-adjusted return',
      accent: 'amber' as const,
    },
    {
      label: 'Volatility (ann.)',
      value: formatPct(analysis.metrics.annualized_volatility_pct),
      sub: `Beta ${analysis.metrics.beta?.toFixed(2) ?? '—'}`,
      accent: 'neutral' as const,
    },
    {
      label: 'Max Drawdown',
      value: formatPct(analysis.metrics.max_drawdown_pct),
      sub: 'peak-to-trough',
      accent: 'crimson' as const,
    },
    {
      label: 'Ann. Return',
      value: formatPct(analysis.metrics.annualized_return_pct),
      sub: 'vs benchmark',
      accent: 'emerald' as const,
    },
  ]

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
      {cards.map((c) => (
        <div key={c.label} className="card p-4">
          <p className="label-overline">{c.label}</p>
          <p
            className={classNames(
              'metric-value mt-2',
              c.accent === 'emerald' && 'text-emerald-accent',
              c.accent === 'crimson' && 'text-crimson-accent',
              c.accent === 'amber' && 'text-amber-accent',
              c.accent === 'neutral' && 'text-bone-50'
            )}
          >
            {c.value}
          </p>
          <p className="text-xs text-bone-400 mt-1">{c.sub}</p>
        </div>
      ))}
    </div>
  )
}