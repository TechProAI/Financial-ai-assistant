import { api } from './client'
import type { Holding, PortfolioAnalysis } from '@/types'


export async function analyzePortfolio(
  holdings: Holding[],
  benchmark = '^NSEI'
): Promise<PortfolioAnalysis> {
  const { data } = await api.post<PortfolioAnalysis>('/portfolio/analyze', {
    holdings,
    benchmark,
  })
  return data
}