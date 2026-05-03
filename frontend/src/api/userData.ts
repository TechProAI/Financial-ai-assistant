import { api } from './client'

export async function fetchSessions() {
  const { data } = await api.get('/user/sessions')
  return data
}

export async function createSession() {
  const { data } = await api.post('/user/sessions')
  return data
}

export async function deleteSession(sessionId: string) {
  await api.delete(`/user/sessions/${sessionId}`)
}

export async function fetchMessages(sessionId: string) {
  const { data } = await api.get(`/user/sessions/${sessionId}/messages`)
  return data
}

export async function saveMessage(msg: {
  session_id: string
  role: string
  content: string
  citations?: any[]
  agent_trace?: any[]
  disclaimers?: string[]
  extra_data?: any
}) {
  const { data } = await api.post('/user/messages', msg)
  return data
}

export async function fetchHoldings() {
  const { data } = await api.get('/user/holdings')
  return data
}

export async function upsertHolding(holding: { ticker: string; quantity: number; avg_cost: number }) {
  const { data } = await api.post('/user/holdings', holding)
  return data
}

export async function deleteHolding(ticker: string) {
  await api.delete(`/user/holdings/${ticker}`)
}

export async function fetchWatchlist() {
  const { data } = await api.get('/user/watchlist')
  return data
}

export async function addToWatchlist(ticker: string) {
  const { data } = await api.post('/user/watchlist', { ticker })
  return data
}

export async function removeFromWatchlist(ticker: string) {
  await api.delete(`/user/watchlist/${ticker}`)
}