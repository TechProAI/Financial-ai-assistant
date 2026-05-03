export function formatCurrency(
  n: number | null | undefined,
  currency: string = 'USD',
  digits = 2
): string {
  if (n == null || !isFinite(n)) return '—'
  try {
    return new Intl.NumberFormat(currency === 'INR' ? 'en-IN' : 'en-US', {
      style: 'currency',
      currency,
      minimumFractionDigits: digits,
      maximumFractionDigits: digits,
    }).format(n)
  } catch {
    return `${currency} ${n.toFixed(digits)}`
  }
}

export function formatCompact(n: number | null | undefined): string {
  if (n == null || !isFinite(n)) return '—'
  return new Intl.NumberFormat('en-US', {
    notation: 'compact',
    maximumFractionDigits: 2,
  }).format(n)
}

export function formatPct(n: number | null | undefined, digits = 2): string {
  if (n == null || !isFinite(n)) return '—'
  return `${n >= 0 ? '+' : ''}${n.toFixed(digits)}%`
}

export function formatNumber(n: number | null | undefined, digits = 2): string {
  if (n == null || !isFinite(n)) return '—'
  return n.toLocaleString('en-US', {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  })
}

export function classNames(...parts: (string | false | null | undefined)[]): string {
  return parts.filter(Boolean).join(' ')
}