import { NavLink, useNavigate } from 'react-router-dom'
import { MessageSquare, PieChart, TrendingUp, Sparkles, LogOut, Plus, Trash2, MessageCircle } from 'lucide-react'
import { classNames } from '@/utils/format'
import { useAuth } from '@/context/AuthContext'
import { useApp } from '@/context/AppContext'
import { Modal } from '../ui/Modal'
import { useState } from 'react'

const navItems = [
  { to: '/chat', label: 'Chat', icon: MessageSquare, hint: 'Ask Finnie anything' },
  { to: '/portfolio', label: 'Portfolio', icon: PieChart, hint: 'Holdings & risk' },
  { to: '/market', label: 'Market', icon: TrendingUp, hint: 'Live quotes' },
]

export function Sidebar() {
  const { user, signOut } = useAuth()
  const { sessions, activeSessionId, createNewSession, switchSession, deleteSession } = useApp()
  const navigate = useNavigate()

  const [open, setOpen] = useState<boolean>(false)

  const handleLogout = async () => {
    setOpen(false)
    await signOut()
    navigate('/')
  }

  return (
    <>
    <aside className="w-72 shrink-0 border-r border-white/[0.06] bg-ink-950/60 backdrop-blur-sm flex flex-col h-screen sticky top-0">
      
      <div className="p-6 border-b border-white/[0.06]">
        <div className="flex items-center gap-3 cursor-pointer" onClick={() => navigate('/')}>
          <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-emerald-accent to-emerald-dark flex items-center justify-center shadow-glow-emerald">
            <Sparkles className="w-4 h-4 text-ink-950" strokeWidth={2.5} />
          </div>
          <div>
            <h1 className="font-display text-xl font-semibold text-bone-50 leading-none">
              Finnie
            </h1>
            <p className="text-[10px] uppercase tracking-[0.2em] text-bone-400 mt-1">
              Financial Companion
            </p>
          </div>
        </div>
      </div>

      
      <nav className="p-4 space-y-1">
        <p className="label-overline px-3 mb-3">Workspace</p>
        {navItems.map(({ to, label, icon: Icon, hint }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              classNames(
                'group flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200',
                isActive
                  ? 'bg-emerald-accent/10 text-emerald-accent border border-emerald-accent/20'
                  : 'text-bone-300 hover:bg-ink-800 hover:text-bone-50 border border-transparent'
              )
            }
          >
            <Icon className="w-4 h-4" />
            <div className="flex-1">
              <div className="text-sm font-medium">{label}</div>
              <div className="text-[11px] text-bone-400 group-hover:text-bone-300">
                {hint}
              </div>
            </div>
          </NavLink>
        ))}
      </nav>

      <div className="flex-1 overflow-y-auto px-4 pb-4">
        <div className="flex items-center justify-between mb-3">
          <p className="label-overline px-3">Chat History</p>
          <button
            onClick={createNewSession}
            className="text-bone-400 hover:text-emerald-accent transition-colors p-1"
            title="New chat"
          >
            <Plus className="w-3.5 h-3.5" />
          </button>
        </div>
        <div className="space-y-1">
          {sessions.map((s) => (
            <div
              key={s.id}
              className={classNames(
                'group flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer transition-all text-sm',
                activeSessionId === s.id
                  ? 'bg-ink-800 text-bone-50'
                  : 'text-bone-400 hover:bg-ink-900 hover:text-bone-200'
              )}
              onClick={() => switchSession(s.id)}
            >
              <MessageCircle className="w-3.5 h-3.5 shrink-0" />
              <span className="flex-1 truncate text-xs">
                {s.title === 'New Chat' ? 'New Chat' : s.title}
              </span>
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  deleteSession(s.id)
                }}
                className="opacity-0 group-hover:opacity-100 text-bone-500 hover:text-crimson-accent transition-all"
              >
                <Trash2 className="w-3 h-3" />
              </button>
            </div>
          ))}
        </div>
      </div>

      <div className="p-4 border-t border-white/[0.06]">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-ink-800 border border-ink-700 flex items-center justify-center text-bone-300 text-xs font-semibold">
            {user?.email?.[0]?.toUpperCase() || '?'}
          </div>
          <div className="flex-1 min-w-0">
            <div className="text-xs text-bone-200 truncate">{user?.email}</div>
          </div>
          <button
            onClick={() => setOpen(true)}
            className="text-bone-500 hover:text-crimson-accent transition-colors"
            title="Sign out"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </aside>
    <Modal open={open} onClose={() => setOpen(false)}>
        <h2 className="text-lg font-semibold text-center text-black">Are you sure</h2>
        <button onClick={handleLogout} className='bg-green-500 text-white rounded-md pt-2 pb-2 pr-5 pl-5'>Logout</button>
      </Modal>
    </>
  )
}