const TechStack = () => {
    return (
        <>
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
        </>
    )
}

export default TechStack