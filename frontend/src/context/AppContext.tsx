import { createContext, useContext, useState, useEffect, useMemo, useCallback, type ReactNode } from 'react'
import { useAuth } from '@/context/AuthContext'
import {
  fetchSessions, createSession, deleteSession as apiDeleteSession,
  fetchMessages, saveMessage,
  fetchHoldings, upsertHolding, deleteHolding as apiDeleteHolding,
  fetchWatchlist, addToWatchlist, removeFromWatchlist,
} from '@/api/userData'
import type { ChatMessage, Holding } from '@/types'

interface ChatSession {
  id: string
  title: string
  created_at: string
  updated_at: string
}

interface AppContextValue {
  sessions: ChatSession[]
  activeSessionId: string | null
  createNewSession: () => Promise<void>
  switchSession: (id: string) => Promise<void>
  deleteSession: (id: string) => Promise<void>

  chatHistory: ChatMessage[]
  setChatHistory: (msgs: ChatMessage[]) => void
  saveChatMessage: (msg: {
    role: string
    content: string
    citations?: any[]
    agent_trace?: any[]
    disclaimers?: string[]
    extra_data?: any
  }) => Promise<void>

  holdings: Holding[]
  addHolding: (h: Holding) => Promise<void>
  removeHolding: (ticker: string) => Promise<void>

  watchlist: string[]
  addTicker: (ticker: string) => Promise<void>
  removeTicker: (ticker: string) => Promise<void>

  dataReady: boolean
}

const AppContext = createContext<AppContextValue | null>(null)

export function AppProvider({ children }: { children: ReactNode }) {
  const { user, session } = useAuth()

  const [sessions, setSessions] = useState<ChatSession[]>([])
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null)
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([])
  const [holdings, setHoldings] = useState<Holding[]>([])
  const [watchlist, setWatchlist] = useState<string[]>([])
  const [dataReady, setDataReady] = useState(false)

  // ── Load user data when authenticated ──
  useEffect(() => {
    if (!user || !session) {
      setDataReady(false)
      return
    }

    let cancelled = false

    async function load() {
      try {
        // Load everything in parallel — don't let one failure block others
        const [sessionsRes, holdingsRes, watchlistRes] = await Promise.allSettled([
          fetchSessions(),
          fetchHoldings(),
          fetchWatchlist(),
        ])

        if (cancelled) return

        // Sessions
        let loadedSessions: ChatSession[] = []
        if (sessionsRes.status === 'fulfilled' && sessionsRes.value.length > 0) {
          loadedSessions = sessionsRes.value
        } else {
          // Create first session
          try {
            const newSession = await createSession()
            loadedSessions = [newSession]
          } catch (e) {
            console.error('Failed to create session:', e)
          }
        }
        setSessions(loadedSessions)

        // Load messages for the latest session
        if (loadedSessions.length > 0) {
          setActiveSessionId(loadedSessions[0].id)
          try {
            const msgs = await fetchMessages(loadedSessions[0].id)
            if (!cancelled) {
              setChatHistory(
                msgs.map((m: any) => ({ role: m.role, content: m.content, timestamp: m.created_at }))
              )
            }
          } catch {
            setChatHistory([])
          }
        }

        // Holdings
        if (holdingsRes.status === 'fulfilled') {
          setHoldings(
            holdingsRes.value.map((h: any) => ({
              ticker: h.ticker,
              quantity: Number(h.quantity),
              avg_cost: Number(h.avg_cost),
            }))
          )
        }

        // Watchlist
        if (watchlistRes.status === 'fulfilled' && watchlistRes.value.length > 0) {
          setWatchlist(watchlistRes.value.map((w: any) => w.ticker))
        } else {
          // Defaults for new users
          const defaults = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS']
          setWatchlist(defaults)
          for (const t of defaults) {
            addToWatchlist(t).catch(() => {})
          }
        }
      } catch (err) {
        console.error('Data load error:', err)
      } finally {
        if (!cancelled) setDataReady(true)
      }
    }

    load()
    return () => { cancelled = true }
  }, [user, session])

  // ── Sessions ──
  const createNewSession = useCallback(async () => {
    try {
      const newSession = await createSession()
      setSessions((prev) => [newSession, ...prev])
      setActiveSessionId(newSession.id)
      setChatHistory([])
    } catch (e) {
      console.error('Create session failed:', e)
    }
  }, [])

  const switchSession = useCallback(async (id: string) => {
    setActiveSessionId(id)
    setChatHistory([]) // clear immediately so UI doesn't show stale data
    try {
      const msgs = await fetchMessages(id)
      setChatHistory(
        msgs.map((m: any) => ({ role: m.role, content: m.content, timestamp: m.created_at }))
      )
    } catch {
      setChatHistory([])
    }
  }, [])

  const handleDeleteSession = useCallback(async (id: string) => {
    try {
      await apiDeleteSession(id)
      const remaining = sessions.filter((s) => s.id !== id)
      setSessions(remaining)

      if (activeSessionId === id) {
        if (remaining.length > 0) {
          await switchSession(remaining[0].id)
        } else {
          await createNewSession()
        }
      }
    } catch (e) {
      console.error('Delete session failed:', e)
    }
  }, [activeSessionId, sessions, switchSession, createNewSession])

  // ── Chat ──
  const saveChatMessage = useCallback(async (msg: {
    role: string
    content: string
    citations?: any[]
    agent_trace?: any[]
    disclaimers?: string[]
    extra_data?: any
  }) => {
    if (!activeSessionId) return
    try {
      await saveMessage({
        session_id: activeSessionId,
        role: msg.role,
        content: msg.content,
        citations: msg.citations || [],
        agent_trace: msg.agent_trace || [],
        disclaimers: msg.disclaimers || [],
        extra_data: msg.extra_data || {},
      })
      // Update session title from first user message
      if (msg.role === 'user') {
        setSessions((prev) =>
          prev.map((s) =>
            s.id === activeSessionId ? { ...s, title: msg.content.slice(0, 50) } : s
          )
        )
      }
    } catch (e) {
      console.error('Save message failed:', e)
    }
  }, [activeSessionId])

  // ── Holdings ──
  const handleAddHolding = useCallback(async (h: Holding) => {
    const ticker = h.ticker.toUpperCase()

    // Update UI immediately (optimistic)
    setHoldings((prev) => {
      const existing = prev.find((x) => x.ticker === ticker)
      if (existing) {
        return prev.map((x) =>
          x.ticker === ticker
            ? { ...x, quantity: x.quantity + h.quantity, avg_cost: h.avg_cost }
            : x
        )
      }
      return [...prev, { ticker, quantity: h.quantity, avg_cost: h.avg_cost }]
    })

    // Then persist to Supabase
    try {
      await upsertHolding({ ticker, quantity: h.quantity, avg_cost: h.avg_cost })
    } catch (e) {
      console.error('Upsert holding failed:', e)
    }
  }, [])

  const handleRemoveHolding = useCallback(async (ticker: string) => {
    const t = ticker.toUpperCase()

    // Update UI immediately
    setHoldings((prev) => prev.filter((h) => h.ticker !== t))

    // Then persist
    try {
      await apiDeleteHolding(t)
    } catch (e) {
      console.error('Delete holding failed:', e)
    }
  }, [])

  // ── Watchlist ──
  const handleAddTicker = useCallback(async (ticker: string) => {
    const t = ticker.toUpperCase()
    if (watchlist.includes(t)) return

    // Update UI immediately
    setWatchlist((prev) => [...prev, t])

    // Then persist
    try {
      await addToWatchlist(t)
    } catch (e) {
      console.error('Add to watchlist failed:', e)
    }
  }, [watchlist])

  const handleRemoveTicker = useCallback(async (ticker: string) => {
    const t = ticker.toUpperCase()

    // Update UI immediately
    setWatchlist((prev) => prev.filter((x) => x !== t))

    // Then persist
    try {
      await removeFromWatchlist(t)
    } catch (e) {
      console.error('Remove from watchlist failed:', e)
    }
  }, [])

  const value = useMemo(
    () => ({
      sessions, activeSessionId, createNewSession, switchSession,
      deleteSession: handleDeleteSession,
      chatHistory, setChatHistory, saveChatMessage,
      holdings, addHolding: handleAddHolding, removeHolding: handleRemoveHolding,
      watchlist, addTicker: handleAddTicker, removeTicker: handleRemoveTicker,
      dataReady,
    }),
    [sessions, activeSessionId, chatHistory, holdings, watchlist, dataReady,
     createNewSession, switchSession, handleDeleteSession, saveChatMessage,
     handleAddHolding, handleRemoveHolding, handleAddTicker, handleRemoveTicker]
  )

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>
}

export function useApp() {
  const ctx = useContext(AppContext)
  if (!ctx) throw new Error('useApp must be used inside AppProvider')
  return ctx
}