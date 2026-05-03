import {
    PieChart,
    Shield,
    BookOpen,
    Brain,
    Newspaper,
    BarChart3,
} from 'lucide-react'
import TechStack from './TechStack'

const HowItWorks = () => {
    return (
        <>
            <section className="max-w-6xl mx-auto pt-10 px-6 pb-20 md:pb-28" id="how-it-works">
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
            <TechStack />
        </>
    )
}

export default HowItWorks