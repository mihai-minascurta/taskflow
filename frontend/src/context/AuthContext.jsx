import { createContext, useContext, useEffect, useState } from 'react'
import * as authApi from '../api/auth'

const AuthContext = createContext(null)

const TOKEN_KEY = 'taskflow_token'
const USER_KEY = 'taskflow_user'

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [initializing, setInitializing] = useState(true)

  // Restore session from localStorage on first load. This is a simple
  // client-side "remember me" — the token itself is never validated here,
  // only when an actual API call is made (see api/client.js).
  useEffect(() => {
    const storedUser = localStorage.getItem(USER_KEY)
    const storedToken = localStorage.getItem(TOKEN_KEY)
    if (storedUser && storedToken) {
      try {
        setUser(JSON.parse(storedUser))
      } catch {
        localStorage.removeItem(USER_KEY)
        localStorage.removeItem(TOKEN_KEY)
      }
    }
    setInitializing(false)
  }, [])

  async function login(username, password) {
    const { token, user: loggedInUser } = await authApi.login(username, password)
    localStorage.setItem(TOKEN_KEY, token)
    localStorage.setItem(USER_KEY, JSON.stringify(loggedInUser))
    setUser(loggedInUser)
    return loggedInUser
  }

  function logout() {
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
    setUser(null)
  }

  const value = {
    user,
    isAuthenticated: Boolean(user),
    initializing,
    login,
    logout,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return ctx
}
