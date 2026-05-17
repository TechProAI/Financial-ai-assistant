import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import { Sparkles, Menu, X } from "lucide-react";
import HeroSection from "./HeroSection";
import { useAuth } from "@/context/AuthContext";

const NavSection = () => {
    const [scrolled, setScrolled] = useState(false)
    const [mobileOpen, setMobileOpen] = useState(false)
    const navigate = useNavigate()
    const { user } = useAuth()

    useEffect(() => {
        const h = () => setScrolled(window.scrollY > 40)
        window.addEventListener('scroll', h, { passive: true })
        return () => window.removeEventListener('scroll', h)
    }, [])

    return (
        <>
            <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${scrolled ? 'bg-ink-950/80 backdrop-blur-xl border-b border-white/[0.06] py-3' : 'py-5'}`}>
                <div className="max-w-7xl mx-auto px-6 flex items-center justify-between">
                    
                    <div className="flex items-center gap-3">
                        <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-emerald-accent to-emerald-dark flex items-center justify-center shadow-glow-emerald">
                            <Sparkles className="w-4 h-4 text-ink-950" strokeWidth={2.5} />
                        </div>
                        <span className="font-display text-xl font-semibold text-bone-50 tracking-tight">
                            Finnie <span className="text-emerald-accent"> AI</span>
                        </span>
                    </div>

                    
                    <div className="hidden md:flex items-center gap-8">
                        {['Features', 'How It Works', 'Tech Stack'].map((item) => (
                            <a key={item} href={`#${item.toLowerCase().replace(/ /g, '-')}`} className="text-sm text-bone-300 hover:text-bone-50 transition-colors">
                                {item}
                            </a>
                        ))}
                    </div>

                    <div className="hidden md:flex items-center gap-3">
                        {!user ? (
                            <button onClick={() => navigate('/auth')} className="text-sm text-bone-200 hover:text-bone-50 transition-colors px-4 py-2">
                                Login
                            </button>
                        ) : ""

                        }

                        <button
                            onClick={() => navigate('/chat')}
                            className="text-sm font-medium bg-emerald-accent text-ink-950 px-5 py-2 rounded-lg hover:bg-emerald-deep transition-colors"
                        >
                            Get Started
                        </button>
                    </div>

                    <button className="md:hidden text-bone-200" onClick={() => setMobileOpen(!mobileOpen)}>
                        {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
                    </button>
                </div>

                {mobileOpen && (
                    <div className="md:hidden bg-ink-950/95 backdrop-blur-xl border-t border-white/[0.06] px-6 py-4 space-y-3">
                        {['Features', 'How It Works', 'Pricing', 'FAQ'].map((l) => (
                            <a key={l} href={`#${l.toLowerCase().replace(/ /g, '-')}`} className="block text-sm text-bone-300 py-2" onClick={() => setMobileOpen(false)}>
                                {l}
                            </a>
                        ))}
                        <button onClick={() => navigate('/chat')} className="w-full text-sm font-medium bg-emerald-accent text-ink-950 px-5 py-2.5 rounded-lg mt-2">
                            Get Started Free
                        </button>
                    </div>
                )}
            </nav>
            <HeroSection />
        </>
    )
}

export default NavSection