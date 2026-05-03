import ReactMarkdown from 'react-markdown'
import { User, Sparkles } from 'lucide-react'
import type { ChatMessage } from '@/types'
import { classNames } from '@/utils/format'

export function MessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === 'user'
  return (
    <div
      className={classNames(
        'flex gap-4 animate-fade-up',
        isUser ? 'flex-row-reverse' : ''
      )}
    >
      <div
        className={classNames(
          'w-8 h-8 rounded-lg flex items-center justify-center shrink-0',
          isUser
            ? 'bg-ink-800 text-bone-300 border border-ink-700'
            : 'bg-linear-to-br from-emerald-accent to-emerald-dark text-ink-950'
        )}
      >
        {isUser ? (
          <User className="w-4 h-4" />
        ) : (
          <Sparkles className="w-4 h-4" strokeWidth={2.5} />
        )}
      </div>

      <div
        className={classNames(
          'max-w-[75%] rounded-2xl px-4 py-3',
          isUser
            ? 'bg-ink-800 border border-ink-700 text-bone-100'
            : 'bg-ink-900/60 border border-white/[0.06] text-bone-100'
        )}
      >
        <div className="prose prose-invert prose-sm max-w-none prose-p:my-2 prose-headings:font-display prose-headings:text-bone-50 prose-strong:text-bone-50 prose-a:text-emerald-accent">
          <ReactMarkdown>{message.content}</ReactMarkdown>
        </div>
      </div>
    </div>
  )
}