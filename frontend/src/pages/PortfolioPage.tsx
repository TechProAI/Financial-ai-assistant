import { useMutation } from '@tanstack/react-query'
import { PieChart as PieIcon, Play } from 'lucide-react'
import { useApp } from '@/context/AppContext'
import { analyzePortfolio } from '@/api/portfolio'
import { Card, CardHeader } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { EmptyState } from '@/components/ui/EmptyState'
import { Spinner } from '@/components/ui/Spinner'
import { AddHoldingForm } from '@/components/portfolio/AddHoldingForm'
import { HoldingsTable } from '@/components/portfolio/HoldingsTable'
import { MetricsGrid } from '@/components/portfolio/MetricsGrid'
import { AllocationChart } from '@/components/portfolio/AllocationChart'
import { Recommendations } from '@/components/portfolio/Recommendations'

export function PortfolioPage() {
  const { holdings, addHolding, removeHolding, dataReady } = useApp()

  const mutation = useMutation({
    mutationFn: () => analyzePortfolio(holdings),
  })

  if (!dataReady) {
    return (
      <div className="flex items-center justify-center h-[60vh]">
        <div className="flex items-center gap-3 text-bone-400">
          <Spinner size={20} />
          <span>Loading holdings...</span>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="label-overline">Portfolio Analytics</p>
          <h1 className="font-display text-3xl font-semibold text-bone-50 mt-1">
            Holdings & Risk
          </h1>
        </div>
        <Button
          onClick={() => mutation.mutate()}
          disabled={holdings.length === 0 || mutation.isPending}
        >
          {mutation.isPending ? <Spinner size={14} /> : <Play className="w-4 h-4" />}
          Run Analysis
        </Button>
      </div>

      <Card>
        <CardHeader title="Add a holding" subtitle="Build your portfolio snapshot" />
        <AddHoldingForm onAdd={addHolding} />
      </Card>

      <Card>
        <CardHeader title="Current holdings" />
        <HoldingsTable holdings={holdings} onRemove={removeHolding} />
      </Card>

      {mutation.error && (
        <div className="card p-4 border-crimson-accent/30 text-sm text-crimson-accent">
          {(mutation.error as Error).message}
        </div>
      )}

      {mutation.data ? (
        <>
          <MetricsGrid
            analysis={mutation.data}
            currency={
              holdings[0]?.ticker.endsWith('.NS') ||
              holdings[0]?.ticker.endsWith('.BO')
                ? 'INR'
                : 'USD'
            }
          />
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <AllocationChart allocations={mutation.data.allocations} />
            <Recommendations items={mutation.data.recommendations} />
          </div>
        </>
      ) : (
        holdings.length > 0 && (
          <EmptyState
            icon={PieIcon}
            title="Ready for analysis"
            description="Click Run Analysis to compute Sharpe ratio, volatility, beta, drawdown, and personalized recommendations."
          />
        )
      )}
    </div>
  )
}