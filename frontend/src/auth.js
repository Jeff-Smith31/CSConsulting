import React from 'react'

const AuthContext = React.createContext()

export function AuthProvider({ children }) {
  const [token, setToken] = React.useState(() => localStorage.getItem('token'))
  const [refresh, setRefresh] = React.useState(() => localStorage.getItem('refresh'))

  const login = (accessToken, refreshToken) => {
    setToken(accessToken)
    setRefresh(refreshToken)
    localStorage.setItem('token', accessToken)
    localStorage.setItem('refresh', refreshToken)
  }

  const logout = () => {
    setToken(null)
    setRefresh(null)
    localStorage.removeItem('token')
    localStorage.removeItem('refresh')
  }

  return (
    <AuthContext.Provider value={{ token, refresh, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return React.useContext(AuthContext)
}
