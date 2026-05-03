import { Routes, Route } from 'react-router-dom'
import { Layout } from './components/layout/Layout'
import { AuthPage } from './pages/AuthPage'
import { ChatPage } from './pages/ChatPage'
import { PortfolioPage } from './pages/PortfolioPage'
import { MarketPage } from './pages/MarketPage'
import { ProtectedRoute } from './components/ProtectedRoute'
import HomePage from './pages/HomePage/HomePage'

function App() {
  return (
    <Routes>
      {/* Public pages */}
      <Route index element={<HomePage />} />
      <Route path="auth" element={<AuthPage />} />

      {/* Protected dashboard */}
      <Route
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route path="chat" element={<ChatPage />} />
        <Route path="portfolio" element={<PortfolioPage />} />
        <Route path="market" element={<MarketPage />} />
      </Route>
    </Routes>
  )
}

export default App