import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Sparkles, Mail, Lock, User, ArrowRight } from 'lucide-react'
import { useAuth } from '@/context/AuthContext'

export function AuthPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [name, setName] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { authType, setMode, signIn, signUp, signInWithGoogle } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      if (authType === 'login') {
        await signIn(email, password)
      } else {
        await signUp(email, password, name)
      }
      navigate('/chat')
    } catch (err: any) {
      setError(err.message || 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  const handleGoogle = async () => {
    try {
      await signInWithGoogle()
    } catch (err: any) {
      setError(err.message)
    }
  }

  return (
    <div className="min-h-screen bg-ink-950 flex items-center justify-center px-4">
      <div className="w-full max-w-sm">
        
        <div className="flex items-center justify-center gap-2.5 mb-8">
          <div className="w-9 h-9 rounded-lg bg-gradient-to-br from-emerald-accent to-emerald-dark flex items-center justify-center">
            <Sparkles className="w-4 h-4 text-ink-950" strokeWidth={2.5} />
          </div>
          <span className="font-display text-2xl font-semibold text-bone-50">Finnie</span>
        </div>

        
        <div className="bg-ink-900/60 border border-white/[0.06] rounded-2xl p-7">
          <h2 className="font-display text-xl font-semibold text-bone-50 text-center mb-1">
            {authType === 'login' ? 'Welcome back' : 'Create your account'}
          </h2>
          <p className="text-sm text-bone-400 text-center mb-6">
            {authType === 'login'
              ? 'Sign in to access your chats and portfolio'
              : 'Start your financial learning journey'}
          </p>

          
          <button
            onClick={handleGoogle}
            className="w-full flex items-center justify-center gap-2 bg-ink-800 border border-ink-700 rounded-lg py-2.5 text-sm text-bone-200 hover:bg-ink-700 hover:text-bone-50 transition-colors mb-5"
          >
            <svg className="w-4 h-4" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" />
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
            </svg>
            Continue with Google
          </button>

          <div className="flex items-center gap-3 mb-5">
            <div className="flex-1 h-px bg-ink-700" />
            <span className="text-xs text-bone-500">or</span>
            <div className="flex-1 h-px bg-ink-700" />
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {authType === 'signup' && (
              <div>
                <label className="text-[11px] uppercase tracking-widest text-bone-400 block mb-1.5">Name</label>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-bone-500" />
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Your name"
                    required
                    className="input-base pl-10"
                  />
                </div>
              </div>
            )}

            <div>
              <label className="text-[11px] uppercase tracking-widest text-bone-400 block mb-1.5">Email</label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-bone-500" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@example.com"
                  required
                  className="input-base pl-10"
                />
              </div>
            </div>

            <div>
              <label className="text-[11px] uppercase tracking-widest text-bone-400 block mb-1.5">Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-bone-500" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Min 6 characters"
                  required
                  minLength={6}
                  className="input-base pl-10"
                />
              </div>
            </div>

            {error && (
              <p className="text-xs text-crimson-accent bg-crimson-accent/10 border border-crimson-accent/20 rounded-lg px-3 py-2">
                {error}
              </p>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full flex items-center justify-center gap-2 bg-emerald-accent text-ink-950 font-semibold py-2.5 rounded-lg hover:bg-emerald-deep transition-colors disabled:opacity-50"
            >
              {loading ? 'Please wait...' : authType === 'login' ? 'Sign In' : 'Create Account'}
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>

          <p className="text-sm text-bone-400 text-center mt-5">
            {authType === 'login' ? "Don't have an account?" : 'Already have an account?'}{' '}
            <button
              onClick={() => { setMode(authType === 'login' ? 'signup' : 'login'); setError('') }}
              className="text-emerald-accent hover:underline"
            >
              {authType === 'login' ? 'Sign up' : 'Sign in'}
            </button>
          </p>
        </div>
      </div>
    </div>
  )
}