import { useNavigate } from 'react-router-dom'
import {
  Sparkles,
  MessageSquare,
  PieChart,
  TrendingUp,
  Shield,
  BookOpen,
  Brain,
  ArrowRight,
  Newspaper,
  BarChart3,
} from 'lucide-react'

export function LandingPage() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-ink-950 text-bone-100">
      {/* ── Navbar ── */}
      <nav className="max-w-6xl mx-auto px-6 py-6 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-emerald-accent to-emerald-dark flex items-center justify-center">
            <Sparkles className="w-4 h-4 text-ink-950" strokeWidth={2.5} />
          </div>
          <span className="font-display text-xl font-semibold text-bone-50">Finnie</span>
        </div>
        <button
          onClick={() => navigate('/chat')}
          className="text-sm font-medium bg-emerald-accent text-ink-950 px-5 py-2 rounded-lg hover:bg-emerald-deep transition-colors"
        >
          Open App
        </button>
      </nav>

      {/* ── Hero ── */}
      <section className="max-w-6xl mx-auto px-6 pt-16 pb-20 md:pt-24 md:pb-28">
        <div className="max-w-3xl">
          <p className="text-[11px] uppercase tracking-[0.2em] text-emerald-accent mb-4">
            AI-Powered Financial Assistant
          </p>
          <h1 className="font-display text-4xl md:text-5xl font-semibold text-bone-50 leading-tight mb-6">
            Learn investing through{' '}
            <span className="text-emerald-accent">intelligent conversation</span>
          </h1>
          <p className="text-lg text-bone-300 leading-relaxed mb-8">
            Finnie is a multi-agent AI system that teaches financial concepts, fetches live market
            data, analyzes portfolios, and monitors news sentiment — all through a single chat
            interface. Built for Indian investors.
          </p>
          <button
            onClick={() => navigate('/chat')}
            className="inline-flex items-center gap-2 bg-emerald-accent text-ink-950 font-semibold px-6 py-3 rounded-xl hover:bg-emerald-deep transition-all"
          >
            Try Finnie
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </section>

      {/* ── What It Does (3 features) ── */}
      <section className="max-w-6xl mx-auto px-6 pb-20 md:pb-28">
        <p className="text-[11px] uppercase tracking-[0.2em] text-emerald-accent mb-3">
          What It Does
        </p>
        <h2 className="font-display text-2xl md:text-3xl font-semibold text-bone-50 mb-10">
          Three tools, one interface
        </h2>

        <div className="grid md:grid-cols-3 gap-5">
          {[
            {
              icon: MessageSquare,
              title: 'AI Chat',
              desc: 'Ask any financial question in plain English. Finnie retrieves answers from a knowledge base of 200+ articles using RAG, with source citations on every response.',
            },
            {
              icon: PieChart,
              title: 'Portfolio Analysis',
              desc: 'Enter your holdings and get Sharpe ratio, beta, volatility, max drawdown, allocation breakdown, and personalized rebalancing recommendations.',
            },
            {
              icon: TrendingUp,
              title: 'Live Market Data',
              desc: 'Real-time stock quotes from NSE, BSE, and global exchanges. Historical price charts from 1 month to 5 years. News sentiment scoring for any ticker.',
            },
          ].map((f) => (
            <div
              key={f.title}
              className="bg-ink-900/50 border border-white/[0.06] rounded-xl p-6 hover:border-emerald-accent/25 transition-colors"
            >
              <f.icon className="w-5 h-5 text-emerald-accent mb-4" />
              <h3 className="font-display text-lg font-semibold text-bone-50 mb-2">{f.title}</h3>
              <p className="text-sm text-bone-400 leading-relaxed">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── How It Works (the 6 agents) ── */}
      <section className="max-w-6xl mx-auto px-6 pb-20 md:pb-28">
        <p className="text-[11px] uppercase tracking-[0.2em] text-emerald-accent mb-3">
          How It Works
        </p>
        <h2 className="font-display text-2xl md:text-3xl font-semibold text-bone-50 mb-4">
          Six specialized agents, one workflow
        </h2>
        <p className="text-bone-400 mb-10 max-w-2xl">
          Every question flows through a LangGraph orchestrated pipeline. A supervisor agent
          classifies your intent and routes to the right specialist. The compliance agent
          reviews every response before it reaches you.
        </p>

        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
          {[
            { icon: Brain, name: 'Supervisor', desc: 'Classifies intent, extracts tickers, routes to the right agent' },
            { icon: BookOpen, name: 'Education', desc: 'Searches Pinecone knowledge base using RAG, generates cited answers' },
            { icon: BarChart3, name: 'Market Intelligence', desc: 'Fetches live quotes from yfinance, summarizes price action' },
            { icon: PieChart, name: 'Portfolio Analysis', desc: 'Computes risk metrics — Sharpe, beta, volatility, drawdown' },
            { icon: Newspaper, name: 'News & Sentiment', desc: 'Pulls recent headlines, scores positive/negative/neutral sentiment' },
            { icon: Shield, name: 'Compliance', desc: 'Filters risky language, adds disclaimers, ensures safe output' },
          ].map((a) => (
            <div
              key={a.name}
              className="bg-ink-900/40 border border-white/[0.06] rounded-xl p-5 hover:border-emerald-accent/20 transition-colors"
            >
              <a.icon className="w-5 h-5 text-emerald-accent mb-3" />
              <h3 className="text-sm font-semibold text-bone-50 mb-1">{a.name}</h3>
              <p className="text-xs text-bone-400 leading-relaxed">{a.desc}</p>
            </div>
          ))}
        </div>

        {/* Simple flow diagram */}
        <div className="mt-10 bg-ink-900/30 border border-white/[0.06] rounded-xl p-6 overflow-x-auto">
          <div className="flex items-center gap-3 min-w-[600px] justify-center text-xs font-mono">
            <span className="bg-ink-800 border border-ink-700 rounded-lg px-3 py-2 text-bone-200">User</span>
            <span className="text-bone-500">→</span>
            <span className="bg-ink-800 border border-ink-700 rounded-lg px-3 py-2 text-bone-200">FastAPI</span>
            <span className="text-bone-500">→</span>
            <span className="bg-emerald-accent/10 border border-emerald-accent/30 rounded-lg px-3 py-2 text-emerald-accent">Supervisor</span>
            <span className="text-bone-500">→</span>
            <span className="bg-ink-800 border border-ink-700 rounded-lg px-3 py-2 text-bone-200">Domain Agent</span>
            <span className="text-bone-500">→</span>
            <span className="bg-amber-accent/10 border border-amber-accent/30 rounded-lg px-3 py-2 text-amber-accent">Compliance</span>
            <span className="text-bone-500">→</span>
            <span className="bg-ink-800 border border-ink-700 rounded-lg px-3 py-2 text-bone-200">Response</span>
          </div>
        </div>
      </section>

      {/* ── Tech Stack ── */}
      <section className="max-w-6xl mx-auto px-6 pb-20 md:pb-28">
        <p className="text-[11px] uppercase tracking-[0.2em] text-emerald-accent mb-3">
          Tech Stack
        </p>
        <h2 className="font-display text-2xl md:text-3xl font-semibold text-bone-50 mb-10">
          What we used to build this
        </h2>

        <div className="grid md:grid-cols-2 gap-5">
          {[
            { category: 'Orchestration', items: ['LangGraph — multi-agent state machine with conditional routing', 'LangSmith — full observability, prompt tracing, token tracking'] },
            { category: 'AI / LLM', items: ['OpenAI GPT-4o-mini — intent classification and text generation', 'text-embedding-3-small — 1536-dim embeddings for semantic search'] },
            { category: 'Data & Storage', items: ['Pinecone — vector database for RAG (900+ indexed chunks)', 'yfinance + curl_cffi — real-time market data from NSE/BSE/NYSE'] },
            { category: 'Backend', items: ['FastAPI — async Python API with Pydantic validation', 'pytest — 85%+ test coverage across agents, services, and endpoints'] },
            { category: 'Frontend', items: ['React + TypeScript + Vite — type-safe SPA with hot reload', 'Tailwind CSS — utility-first styling with custom design tokens'] },
            { category: 'Extras', items: ['MCP Server — exposes tools to Claude Desktop and other MCP clients', 'Recharts — portfolio pie charts and historical price area charts'] },
          ].map((s) => (
            <div
              key={s.category}
              className="bg-ink-900/40 border border-white/[0.06] rounded-xl p-5"
            >
              <h3 className="text-xs uppercase tracking-widest text-emerald-accent mb-3">
                {s.category}
              </h3>
              <ul className="space-y-2">
                {s.items.map((item) => (
                  <li key={item} className="text-sm text-bone-300 leading-relaxed">
                    <span className="text-bone-50 font-medium">{item.split(' — ')[0]}</span>
                    {item.includes(' — ') && (
                      <span className="text-bone-400"> — {item.split(' — ')[1]}</span>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>

      {/* ── Key Numbers ── */}
      <section className="max-w-6xl mx-auto px-6 pb-20 md:pb-28">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-5">
          {[
            { value: '6', label: 'Specialized Agents' },
            { value: '200+', label: 'Knowledge Articles' },
            { value: '85%+', label: 'Test Coverage' },
            { value: '900+', label: 'Pinecone Vectors' },
          ].map((s) => (
            <div key={s.label} className="bg-ink-900/40 border border-white/[0.06] rounded-xl p-5 text-center">
              <div className="font-mono text-2xl font-bold text-emerald-accent">{s.value}</div>
              <div className="text-xs text-bone-400 mt-1">{s.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* ── Footer ── */}
      <footer className="border-t border-white/[0.06] py-8">
        <div className="max-w-6xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-emerald-accent" />
            <span className="font-display text-sm font-semibold text-bone-50">Finnie AI</span>
            <span className="text-xs text-bone-500 ml-2">
              Built as a capstone project for Interview Kickstart
            </span>
          </div>
        </div>
      </footer>
    </div>
  )
}