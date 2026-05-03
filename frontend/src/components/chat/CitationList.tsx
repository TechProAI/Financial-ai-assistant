import { BookOpen } from 'lucide-react'
import type { Citation } from '@/types'

export function CitationList({ citations }: { citations: Citation[] }) {
  if (!citations.length) return null
  return (
    <div className="card p-4 space-y-3">
      <div className="flex items-center gap-2 label-overline">
        <BookOpen className="w-3 h-3" />
        <span>Sources</span>
      </div>
      <ul className="space-y-2">
        {citations.map((c, i) => (
          <li
            key={i}
            className="text-sm border-l-2 border-emerald-accent/40 pl-3 py-1"
          >
            <div className="font-medium text-bone-50">
              [{i + 1}] {c.title}
            </div>
            <div className="text-xs text-bone-400 mt-0.5 line-clamp-2">
              {c.snippet}
            </div>
            <div className="text-[10px] font-mono text-emerald-accent/70 mt-1">
              relevance {(c.score * 100).toFixed(0)}%
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}