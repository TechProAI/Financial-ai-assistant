export type Role = 'user' | 'assistant' | 'system'

export interface ChatMessage {
  role: Role
  content: string
  timestamp?: string
}

export interface UserProfile {
  risk_appetite: 'conservative' | 'moderate' | 'aggressive'
  experience_level: 'beginner' | 'intermediate' | 'advanced'
  goals: string[]
}

export interface Citation {
  source: string
  title: string
  snippet: string
  score: number
}

export interface AgentTraceItem {
  agent: string
  action: string
  duration_ms: number
}

export interface ChatRequest {
  session_id: string
  message: string
  history: ChatMessage[]
  user_profile?: UserProfile
}

export interface ChatResponse {
  session_id: string
  answer: string
  citations: Citation[]
  agent_trace: AgentTraceItem[]
  disclaimers: string[]
  data: {
    intent?: string
    tickers?: string[]
    market_data?: Record<string, Quote>
    news_items?: NewsItem[]
  }
}

export interface Quote {
  ticker: string
  price: number
  change: number
  change_percent: number
  volume: number
  market_cap?: number | null
  pe_ratio?: number | null
  day_high?: number | null
  day_low?: number | null
  company_name?: string
  sector?: string
  currency?: string
  timestamp: string
}

export interface HistoryPoint {
  date: string
  open: number
  high: number
  low: number
  close: number
  volume: number
}

export interface NewsItem {
  title: string
  summary: string
  url: string
  published: string
  source: string
  sentiment: string | null
  sentiment_score: number | null
}

export interface Holding {
  ticker: string
  quantity: number
  avg_cost: number
}

export interface PortfolioAnalysis {
  total_value: number
  total_cost: number
  total_return_pct: number
  allocations: Record<string, number>
  metrics: {
    annualized_return_pct: number
    annualized_volatility_pct: number
    sharpe_ratio: number
    beta: number | null
    max_drawdown_pct: number
    num_positions: number
  }
  recommendations: string[]
}