import { useQuery } from '@tanstack/react-query'
import {
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Area,
  AreaChart,
} from 'recharts'
import { getHistory } from '@/api/market'
import { Spinner } from '@/components/ui/Spinner'
import { formatCurrency } from '@/utils/format'
import { useState } from 'react'
import { classNames } from '@/utils/format'

const PERIODS = [
  { label: '1M', value: '1mo' },
  { label: '3M', value: '3mo' },
  { label: '6M', value: '6mo' },
  { label: '1Y', value: '1y' },
  { label: '5Y', value: '5y' },
]

export function PriceChart({ ticker, currency = 'USD' }: { ticker: string; currency?: string }) {
  const [period, setPeriod] = useState('3mo')
  const { data, isLoading, error } = useQuery({
    queryKey: ['history', ticker, period],
    queryFn: () => getHistory(ticker, period),
    enabled: !!ticker,
  })

  const chartData =
    data?.data.map((d) => ({
      date: d.date.slice(0, 10),
      close: d.close,
    })) ?? []

  const firstClose = chartData[0]?.close ?? 0
  const lastClose = chartData[chartData.length - 1]?.close ?? 0
  const positive = lastClose >= firstClose
  const color = positive ? '#4ade80' : '#f87171'

  return (
    <div className="card p-5">
      <div className="flex items-center justify-between mb-4">
        <div>
          <p className="label-overline">Price history</p>
          <h3 className="font-display text-xl font-semibold text-bone-50 mt-1">
            {ticker}
          </h3>
        </div>
        <div className="flex gap-1">
          {PERIODS.map((p) => (
            <button
              key={p.value}
              onClick={() => setPeriod(p.value)}
              className={classNames(
                'px-2.5 py-1 rounded text-xs font-mono transition-colors',
                period === p.value
                  ? 'bg-emerald-accent/10 text-emerald-accent border border-emerald-accent/30'
                  : 'text-bone-400 hover:text-bone-200 border border-transparent'
              )}
            >
              {p.label}
            </button>
          ))}
        </div>
      </div>

      <div className="h-80">
        {isLoading ? (
          <div className="h-full flex items-center justify-center">
            <Spinner size={24} />
          </div>
        ) : error ? (
          <div className="h-full flex items-center justify-center text-sm text-crimson-accent">
            {(error as Error).message}
          </div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={chartData}>
              <defs>
                <linearGradient id={`grad-${ticker}`} x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor={color} stopOpacity={0.3} />
                  <stop offset="100%" stopColor={color} stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid
                strokeDasharray="3 3"
                stroke="#2a3550"
                vertical={false}
              />
              <XAxis
                dataKey="date"
                stroke="#78745f"
                fontSize={10}
                fontFamily="JetBrains Mono"
                tickLine={false}
                axisLine={false}
              />
              <YAxis
                stroke="#78745f"
                fontSize={10}
                fontFamily="JetBrains Mono"
                tickLine={false}
                axisLine={false}
                domain={['auto', 'auto']}
                tickFormatter={(v) =>
                  currency === 'INR' ? `₹${v.toFixed(0)}` : `$${v.toFixed(0)}`
                }
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#141c2e',
                  border: '1px solid #2a3550',
                  borderRadius: 8,
                  fontFamily: 'JetBrains Mono',
                  fontSize: 12,
                }}
                labelStyle={{ color: '#d4cfbd' }}
                formatter={(v) => formatCurrency(v as number, currency)}
              />
              <Area
                type="monotone"
                dataKey="close"
                stroke={color}
                strokeWidth={2}
                fill={`url(#grad-${ticker})`}
              />
            </AreaChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  )
}