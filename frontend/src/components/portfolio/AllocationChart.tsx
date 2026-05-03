import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts'

const COLORS = ['#4ade80', '#fbbf24', '#60a5fa', '#f87171', '#a78bfa', '#34d399', '#fb923c', '#22d3ee']

export function AllocationChart({ allocations }: { allocations: Record<string, number> }) {
  const data = Object.entries(allocations).map(([name, value]) => ({ name, value }))
  if (!data.length) return null

  return (
    <div className="card p-5">
      <p className="label-overline mb-4">Allocation</p>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              dataKey="value"
              nameKey="name"
              innerRadius={60}
              outerRadius={90}
              paddingAngle={2}
              stroke="#0a0f1a"
              strokeWidth={2}
            >
              {data.map((_, i) => (
                <Cell key={i} fill={COLORS[i % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{
                backgroundColor: '#141c2e',
                border: '1px solid #2a3550',
                borderRadius: 8,
                fontFamily: 'JetBrains Mono',
                fontSize: 12,
              }}
              formatter={(v) => `${(v as number).toFixed(2)}%`}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
      <div className="grid grid-cols-2 gap-2 mt-3">
        {data.map((d, i) => (
          <div key={d.name} className="flex items-center gap-2 text-xs">
            <span
              className="w-2 h-2 rounded-sm"
              style={{ backgroundColor: COLORS[i % COLORS.length] }}
            />
            <span className="font-mono text-bone-200">{d.name}</span>
            <span className="text-bone-400 ml-auto font-mono">
              {d.value.toFixed(1)}%
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}