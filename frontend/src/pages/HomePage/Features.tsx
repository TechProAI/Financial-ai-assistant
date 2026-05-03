import {
    MessageSquare,
    PieChart,
    TrendingUp
} from 'lucide-react'
import HowItWorks from './HowItWorks'

const Features = () => {
    return (
        <>
            <section className="max-w-6xl mx-auto mt-12 px-6 pb-20 md:pb-28" id="features">
                <p className="text-[11px] uppercase tracking-[0.2em] text-emerald-accent mb-3">
                    Features
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
            <HowItWorks />
        </>
    )
}

export default Features