import { useEffect, useRef } from 'react'
import { MessageSquare, RotateCcw } from 'lucide-react'
import { useApp } from '@/context/AppContext'
import { useChat } from '@/hooks/useChat'
import { MessageBubble } from '@/components/chat/MessageBubble'
import { ChatInput } from '@/components/chat/ChatInput'
import { CitationList } from '@/components/chat/CitationList'
import { AgentTrace } from '@/components/chat/AgentTrace'
import { EmptyState } from '@/components/ui/EmptyState'
import { Button } from '@/components/ui/Button'
import { Spinner } from '@/components/ui/Spinner'

const SUGGESTIONS = [
  'What is a stock and how do dividends work?',
  'Explain the Sharpe ratio in simple terms',
  'How is RELIANCE.NS performing today?',
  'What is SIP and how does it work in India?',
]

export function ChatPage() {
  const { chatHistory, createNewSession, dataReady } = useApp()
  const { send, isLoading, lastResponse } = useChat()
  const endRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [chatHistory])

  if (!dataReady) {
    return (
      <div className="flex items-center justify-center h-[60vh]">
        <div className="flex items-center gap-3 text-bone-400">
          <Spinner size={20} />
          <span>Loading your chats...</span>
        </div>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-[1fr_320px] gap-6 min-h-[calc(100vh-4rem)]">
      <div className="flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <p className="label-overline">Conversation</p>
            <h1 className="font-display text-3xl font-semibold text-bone-50 mt-1">
              Ask Finnie
            </h1>
          </div>
          {chatHistory.length > 0 && (
            <Button variant="ghost" onClick={createNewSession}>
              <RotateCcw className="w-4 h-4" />
              New chat
            </Button>
          )}
        </div>

        {/* Messages */}
        <div className="flex-1 space-y-5 mb-6">
          {chatHistory.length === 0 ? (
            <EmptyState
              icon={MessageSquare}
              title="Your personal financial tutor"
              description="Ask about any financial concept, get real-time market data, or analyze news sentiment — Finnie orchestrates six specialized agents to answer."
            />
          ) : (
            chatHistory.map((m, i) => <MessageBubble key={i} message={m} />)
          )}
          {isLoading && (
            <div className="flex items-center gap-2 text-sm text-bone-400 animate-pulse-soft pl-12">
              <span>Finnie is thinking</span>
              <span className="flex gap-0.5">
                <span className="w-1 h-1 bg-emerald-accent rounded-full animate-bounce" />
                <span className="w-1 h-1 bg-emerald-accent rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                <span className="w-1 h-1 bg-emerald-accent rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
              </span>
            </div>
          )}
          <div ref={endRef} />
        </div>

        {/* Suggestions */}
        {chatHistory.length === 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2 mb-4">
            {SUGGESTIONS.map((s) => (
              <button
                key={s}
                onClick={() => send(s)}
                className="card card-hover p-3 text-left text-sm text-bone-200 hover:text-bone-50"
              >
                {s}
              </button>
            ))}
          </div>
        )}

        {/* Input */}
        <ChatInput onSubmit={send} disabled={isLoading} />

        {/* Disclaimers */}
        {lastResponse?.disclaimers && lastResponse.disclaimers.length > 0 && (
          <div className="mt-4 space-y-1">
            {lastResponse.disclaimers.map((d, i) => (
              <p key={i} className="text-[11px] text-bone-500 italic leading-relaxed">
                · {d}
              </p>
            ))}
          </div>
        )}
      </div>

      {/* Sidebar: citations + trace */}
      <div className="space-y-4">
        {lastResponse?.citations && <CitationList citations={lastResponse.citations} />}
        {lastResponse?.agent_trace && <AgentTrace trace={lastResponse.agent_trace} />}
      </div>
    </div>
  )
}