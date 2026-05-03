import { api } from './client'
import type { ChatRequest, ChatResponse } from '@/types'

export async function sendChat(req: ChatRequest): Promise<ChatResponse> {
  const { data } = await api.post<ChatResponse>('/chat', req)
  return data
}