import { useMutation } from '@tanstack/react-query'
import { sendChat } from '@/api/chat'
import { useApp } from '@/context/AppContext'
import type { ChatMessage, ChatResponse } from '@/types'

export function useChat() {
  const { activeSessionId, chatHistory, setChatHistory, saveChatMessage } = useApp()

  const mutation = useMutation<ChatResponse, Error, string>({
    mutationFn: async (message: string) => {
      return sendChat({
        session_id: activeSessionId || 'default',
        message,
        history: chatHistory,
      })
    },
  })

  async function send(message: string) {
    const userMsg: ChatMessage = {
      role: 'user',
      content: message,
      timestamp: new Date().toISOString(),
    }
    const nextHistory = [...chatHistory, userMsg]
    setChatHistory(nextHistory)

    // Save user message to Supabase
    await saveChatMessage({ role: 'user', content: message })

    try {
      const res = await mutation.mutateAsync(message)
      const assistantMsg: ChatMessage = {
        role: 'assistant',
        content: res.answer,
        timestamp: new Date().toISOString(),
      }
      setChatHistory([...nextHistory, assistantMsg])

      await saveChatMessage({
        role: 'assistant',
        content: res.answer,
        citations: res.citations,
        agent_trace: res.agent_trace,
        disclaimers: res.disclaimers,
        extra_data: res.data,
      })

      return res
    } catch (err) {
      const errorMsg: ChatMessage = {
        role: 'assistant',
        content: `⚠︎ I ran into an error: ${(err as Error).message}`,
        timestamp: new Date().toISOString(),
      }
      setChatHistory([...nextHistory, errorMsg])
      throw err
    }
  }

  return {
    send,
    isLoading: mutation.isPending,
    lastResponse: mutation.data,
    error: mutation.error,
  }
}