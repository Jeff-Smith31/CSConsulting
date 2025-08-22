import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { apiFetch } from '../api'
import { useAuth } from '../auth.jsx'

export default function Login() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [loading, setLoading] = React.useState(false)
  const [error, setError] = React.useState('')

  async function onSubmit(e) {
    e.preventDefault()
    setError(''); setLoading(true)
    const form = new FormData(e.currentTarget)
    const email = form.get('email')
    const password = form.get('password')
    try {
      const res = await apiFetch('/auth/login', { method: 'POST', body: { email, password } })
      login(res.access_token, res.refresh_token)
      navigate('/dashboard')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="auth">
      <h2>Log in</h2>
      <form onSubmit={onSubmit}>
        <label>Email<input name="email" type="email" required /></label>
        <label>Password<input name="password" type="password" required /></label>
        {error && <div className="error">{error}</div>}
        <button className="button" disabled={loading}>{loading ? 'Signing in...' : 'Sign in'}</button>
      </form>
      <p>No account? <Link to="/signup">Create one</Link></p>
    </section>
  )
}
