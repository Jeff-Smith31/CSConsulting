import React from 'react'
import { AuthProvider } from './auth.jsx'

export default function Root({ children }) {
  return (
    <AuthProvider>
      {children}
    </AuthProvider>
  )
}
