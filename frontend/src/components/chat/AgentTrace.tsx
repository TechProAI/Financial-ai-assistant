import { Activity } from 'lucide-react'
import type { AgentTraceItem } from '@/types'

export function AgentTrace({ trace }: { trace: AgentTraceItem[] }) {
  if (!trace.length) return null
  const total = trace.reduce((a, t) => a + t.duration_ms, 0)
  return (
    <div className="card p-4">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2 label-overline">
          <Activity className="w-3 h-3" />
          <span>Agent Trace</span>
        </div>
        <span className="text-xs font-mono text-bone-400">
          {total.toFixed(0)}ms
        </span>
      </div>
      <div className="space-y-1.5">
        {trace.map((t, i) => {
          const pct = (t.duration_ms / total) * 100
          return (
            <div key={i} className="text-xs">
              <div className="flex justify-between mb-1">
                <span className="text-bone-200 font-mono">{t.agent}</span>
                <span className="text-bone-400 font-mono">
                  {t.duration_ms.toFixed(0)}ms
                </span>
              </div>
              <div className="h-1 bg-ink-800 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-emerald-accent to-emerald-dark"
                  style={{ width: `${pct}%` }}
                />
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}