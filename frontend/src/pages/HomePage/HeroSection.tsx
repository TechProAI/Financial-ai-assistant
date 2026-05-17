import { Check, Sparkles, ArrowRight } from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";
import { useNavigate } from "react-router-dom";
import Features from "./Features";

const HeroSection = () => {
    const navigate = useNavigate()
    return (
        <>
            <section className="max-w-6xl mx-auto relative pt-20 pb-20 md:pt-44 md:pb-32 overflow-hidden mb-10">
                
                <div className="absolute top-0 left-1/4 w-[600px] h-[600px] bg-emerald-accent/[0.07] rounded-full blur-[120px] -translate-y-1/2" />
                <div className="absolute bottom-0 right-1/4 w-[400px] h-[400px] bg-amber-accent/[0.05] rounded-full blur-[100px] translate-y-1/2" />

                <div className="max-w-7xl mx-auto px-6">
                    <div className="grid md:grid-cols-2 gap-12 md:gap-16 items-center">
                        
                        <div>
                            <Reveal>
                                <div className="inline-flex items-center gap-2 text-[11px] uppercase tracking-[0.2em] text-emerald-accent bg-emerald-accent/10 border border-emerald-accent/20 rounded-full px-4 py-1.5 mb-6">
                                    <Sparkles className="w-3 h-3" />
                                    AI-Powered Financial Companion
                                </div>
                            </Reveal>

                            <Reveal delay={100}>
                                <h1 className="font-display text-4xl md:text-[3.5rem] md:leading-[1.1] font-semibold text-bone-50 mb-6">
                                    Learn Investing with{' '}
                                    <span className="relative inline-block">
                                        <span className="relative z-10 text-emerald-accent">Six AI Agents</span>
                                        <span className="absolute bottom-1 left-0 right-0 h-3 bg-emerald-accent/15 -skew-x-3 rounded" />
                                    </span>{' '}
                                    Working for You
                                </h1>
                            </Reveal>

                            <Reveal delay={200}>
                                <p className="text-lg text-bone-300 leading-relaxed mb-8 max-w-xl">
                                    Ask about stocks, analyze your portfolio, track live markets, and master financial
                                    concepts — all in one intelligent conversation. Built for Indian investors, powered by GPT&#8209;4o.
                                </p>
                            </Reveal>

                            <Reveal delay={300}>
                                <div className="flex flex-wrap gap-3 mb-8">
                                    <button
                                        onClick={() => navigate('/chat')}
                                        className="inline-flex items-center gap-2 bg-emerald-accent text-ink-950 font-semibold px-6 py-3 rounded-xl hover:bg-emerald-deep transition-all shadow-glow-emerald hover:shadow-emerald-accent/40"
                                    >
                                        Try Finnie
                                        <ArrowRight className="w-4 h-4" />
                                    </button>
                                </div>
                            </Reveal>

                            <Reveal delay={400}>
                                <div className="flex flex-wrap gap-5 text-sm text-bone-400">
                                    {['200+ Knowledge Articles', 'Real-time NSE & BSE', '100% Free to Start'].map((t) => (
                                        <span key={t} className="flex items-center gap-1.5">
                                            <Check className="w-3.5 h-3.5 text-emerald-accent" />
                                            {t}
                                        </span>
                                    ))}
                                </div>
                            </Reveal>
                        </div>

                        
                        <Reveal delay={200} className="hidden md:block">
                            <div className="relative">
                                <div className="absolute inset-0 bg-gradient-to-br from-emerald-accent/10 to-transparent rounded-3xl blur-2xl scale-110" />
                                <div className="relative bg-ink-900/70 backdrop-blur-sm border border-white/[0.08] rounded-2xl p-6 shadow-2xl">
                                    {/* Header */}
                                    <div className="flex items-center gap-3 mb-5 pb-4 border-b border-white/[0.06]">
                                        <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-emerald-accent to-emerald-dark flex items-center justify-center">
                                            <Sparkles className="w-3 h-3 text-ink-950" />
                                        </div>
                                        <div>
                                            <div className="text-sm font-semibold text-bone-50">Finnie AI</div>
                                            <div className="text-[10px] text-emerald-accent">● Online</div>
                                        </div>
                                    </div>

                                    
                                    <div className="space-y-4 mb-4">
                                        <div className="flex justify-end">
                                            <div className="bg-ink-800 border border-ink-700 rounded-2xl rounded-tr-sm px-4 py-2.5 text-sm text-bone-100 max-w-[80%]">
                                                What is a Sharpe ratio and why does it matter?
                                            </div>
                                        </div>
                                        <div className="flex gap-3">
                                            <div className="w-6 h-6 rounded-md bg-gradient-to-br from-emerald-accent to-emerald-dark flex items-center justify-center shrink-0 mt-1">
                                                <Sparkles className="w-3 h-3 text-ink-950" />
                                            </div>
                                            <div className="bg-ink-900/80 border border-white/[0.06] rounded-2xl rounded-tl-sm px-4 py-2.5 text-sm text-bone-200 max-w-[85%]">
                                                <p>The <strong className="text-bone-50">Sharpe ratio</strong> measures how much extra return you earn for each unit of risk. Think of it as "bang for your buck" in investing.</p>
                                                <p className="mt-2">A ratio above <strong className="text-bone-50">1.0</strong> is good, above <strong className="text-bone-50">2.0</strong> is excellent. <span className="text-emerald-accent">[1]</span></p>
                                            </div>
                                        </div>
                                    </div>

                                    
                                    <div className="bg-ink-950/60 rounded-lg px-3 py-2 border-l-2 border-emerald-accent/50">
                                        <div className="text-[10px] uppercase tracking-wider text-bone-400 mb-1">Source</div>
                                        <div className="text-xs text-bone-200">[1] Sharpe Ratio Explained</div>
                                        <div className="text-[10px] text-emerald-accent/70 font-mono mt-0.5">relevance 94%</div>
                                    </div>

                                    
                                    <div className="mt-4 pt-3 border-t border-white/[0.06]">
                                        <div className="text-[10px] uppercase tracking-wider text-bone-400 mb-2">Agent Trace</div>
                                        <div className="flex gap-1 items-center">
                                            {[
                                                { name: 'supervisor', w: '15%', ms: '340ms' },
                                                { name: 'education', w: '75%', ms: '1.8s' },
                                                { name: 'compliance', w: '2%', ms: '1ms' },
                                            ].map((a) => (
                                                <div key={a.name} className="group relative" style={{ width: a.w }}>
                                                    <div className="h-2 rounded-full bg-gradient-to-r from-emerald-accent to-emerald-dark" />
                                                    <div className="absolute -top-7 left-1/2 -translate-x-1/2 bg-ink-800 text-[9px] text-bone-200 px-1.5 py-0.5 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap font-mono">
                                                        {a.name} {a.ms}
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </Reveal>
                    </div>
                </div>
            </section>
            <Features />
        </>
    );
}

export default HeroSection
