import { useQueries } from '@tanstack/react-query'
import { useState } from 'react'
import { TrendingUp } from 'lucide-react'
import { useApp } from '@/context/AppContext'
import { getQuote } from '@/api/market'
import { TickerSearch } from '@/components/market/TickerSearch'
import { QuoteCard } from '@/components/market/QuoteCard'
import { PriceChart } from '@/components/market/PriceChart'
import { EmptyState } from '@/components/ui/EmptyState'
import { Spinner } from '@/components/ui/Spinner'

export function MarketPage() {
  const { watchlist, addTicker, removeTicker, dataReady } = useApp()
  const [selected, setSelected] = useState<string>(watchlist[0] || '')

  const queries = useQueries({
    queries: watchlist.map((t) => ({
      queryKey: ['quote', t],
      queryFn: () => getQuote(t),
      staleTime: 30_000,
    })),
  })

  const handleAddTicker = (t: string) => {
    addTicker(t)
    setSelected(t)
  }

  const handleRemoveTicker = (t: string) => {
    removeTicker(t)
    if (selected === t) {
      const next = watchlist.filter((x) => x !== t)
      if (next.length) setSelected(next[0])
    }
  }

  if (!dataReady) {
    return (
      <div className="flex items-center justify-center h-[60vh]">
        <div className="flex items-center gap-3 text-bone-400">
          <Spinner size={20} />
          <span>Loading watchlist...</span>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <p className="label-overline">Market Intelligence</p>
        <h1 className="font-display text-3xl font-semibold text-bone-50 mt-1">
          Live Quotes & Trends
        </h1>
      </div>

      <TickerSearch onSearch={handleAddTicker} />

      {watchlist.length === 0 ? (
        <EmptyState
          icon={TrendingUp}
          title="Watchlist is empty"
          description="Search for a ticker above to start tracking real-time quotes."
        />
      ) : (
        <>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {queries.map((q, i) => {
              const ticker = watchlist[i]
              if (!ticker) return null
              if (q.isLoading) {
                return (
                  <div key={ticker} className="card p-4 h-[126px] animate-pulse bg-ink-900/30" />
                )
              }
              if (q.error || !q.data) {
                return (
                  <div key={ticker} className="card p-4 text-xs text-crimson-accent">
                    <div className="font-mono font-bold">{ticker}</div>
                    <div className="mt-2">Failed to load</div>
                    <button onClick={() => handleRemoveTicker(ticker)} className="mt-2 text-bone-400 underline">
                      Remove
                    </button>
                  </div>
                )
              }
              return (
                <QuoteCard
                  key={ticker}
                  quote={q.data}
                  active={selected === ticker}
                  onSelect={() => setSelected(ticker)}
                  onRemove={() => handleRemoveTicker(ticker)}
                />
              )
            })}
          </div>

          {selected && (
            <PriceChart
              ticker={selected}
              currency={queries.find((q) => q.data?.ticker === selected)?.data?.currency}
            />
          )}
        </>
      )}
    </div>
  )
}