import { Navigate } from 'react-router-dom'
import { useAuth } from '@/context/AuthContext'
import { Sparkles } from 'lucide-react'

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="min-h-screen bg-ink-950 flex items-center justify-center">
        <div className="flex items-center gap-3 text-bone-400">
          <Sparkles className="w-5 h-5 text-emerald-accent animate-pulse" />
          <span>Loading...</span>
        </div>
      </div>
    )
  }

  if (!user) {
    return <Navigate to="/auth" replace />
  }

  return <>{children}</>
}