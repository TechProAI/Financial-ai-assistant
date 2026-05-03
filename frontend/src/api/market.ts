import { api } from './client'
import type { Quote, HistoryPoint } from '@/types'

export async function getQuote(ticker: string): Promise<Quote> {
  const { data } = await api.get<Quote>(`/market/quote/${ticker.toUpperCase()}`)
  return data
}

export async function getHistory(
  ticker: string,
  period = '3mo',
  interval = '1d'
): Promise<{ ticker: string; data: HistoryPoint[] }> {
  const { data } = await api.get(`/market/history/${ticker.toUpperCase()}`, {
    params: { period, interval },
  })
  return data
}

export async function searchSymbol(
  q: string
): Promise<{ results: { symbol: string; name: string }[] }> {
  const { data } = await api.get('/market/search', { params: { q } })
  return data
}