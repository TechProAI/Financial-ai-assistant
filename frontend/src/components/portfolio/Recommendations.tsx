import { Lightbulb } from 'lucide-react'

export function Recommendations({ items }: { items: string[] }) {
  if (!items.length) return null
  return (
    <div className="card p-5">
      <div className="flex items-center gap-2 label-overline mb-3">
        <Lightbulb className="w-3 h-3" />
        <span>Recommendations</span>
      </div>
      <ul className="space-y-2">
        {items.map((r, i) => (
          <li
            key={i}
            className="text-sm text-bone-200 pl-4 border-l-2 border-amber-accent/40 py-1"
          >
            {r}
          </li>
        ))}
      </ul>
    </div>
  )
}