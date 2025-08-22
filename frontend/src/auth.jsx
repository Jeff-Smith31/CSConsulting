import React from 'react'
import { apiFetch } from './api'

const AuthContext = React.createContext()

export function AuthProvider({ children }) {
  const [token, setToken] = React.useState(() => localStorage.getItem('token'))
  const [refresh, setRefresh] = React.useState(() => localStorage.getItem('refresh'))
  const [user, setUser] = React.useState(null) // { user_id, email, name, is_admin }

  const login = (accessToken, refreshToken) => {
    setToken(accessToken)
    setRefresh(refreshToken)
    localStorage.setItem('token', accessToken)
    localStorage.setItem('refresh', refreshToken)
    // Load user after login
    loadMe(accessToken)
  }

  const logout = () => {
    setToken(null)
    setRefresh(null)
    setUser(null)
    localStorage.removeItem('token')
    localStorage.removeItem('refresh')
  }

  async function loadMe(tkn = token) {
    if (!tkn) { setUser(null); return }
    try {
      const me = await apiFetch('/auth/me', { token: tkn })
      setUser(me)
    } catch (_e) {
      // ignore; leave user as null
    }
  }

  React.useEffect(() => {
    // when token changes (e.g., page reload), fetch /auth/me
    if (token) loadMe(token); else setUser(null)
  }, [token])

  return (
    <AuthContext.Provider value={{ token, refresh, user, login, logout, loadMe }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return React.useContext(AuthContext)
}
