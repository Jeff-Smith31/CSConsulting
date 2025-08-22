import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { apiFetch } from '../api'

export default function Signup() {
  const navigate = useNavigate()
  const [loading, setLoading] = React.useState(false)
  const [error, setError] = React.useState('')
  const [success, setSuccess] = React.useState('')
  const [captcha, setCaptcha] = React.useState({ captcha_id: '', question: '' })

  async function loadCaptcha() {
    try {
      const c = await apiFetch('/auth/captcha')
      setCaptcha(c)
    } catch (e) {
      setCaptcha({ captcha_id: '', question: 'Unable to load captcha. Please try again.' })
    }
  }

  React.useEffect(() => { loadCaptcha() }, [])

  async function onSubmit(e) {
    e.preventDefault()
    setError(''); setSuccess(''); setLoading(true)
    const form = new FormData(e.currentTarget)
    const email = form.get('email')
    const name = form.get('name')
    const password = form.get('password')
    const password_confirm = form.get('password_confirm')
    const captcha_answer = form.get('captcha_answer')

    if (password !== password_confirm) {
      setError('Passwords do not match')
      setLoading(false)
      return
    }

    try {
      await apiFetch('/auth/signup', { method: 'POST', body: { email, name, password, password_confirm, captcha_id: captcha.captcha_id, captcha_answer } })
      setSuccess('Account created! You can now log in.')
      setTimeout(() => navigate('/login'), 800)
    } catch (err) {
      setError(err.message)
      // refresh captcha on error
      loadCaptcha()
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="auth">
      <h2>Create your account</h2>
      <form onSubmit={onSubmit}>
        <label>Name<input name="name" type="text" required /></label>
        <label>Email<input name="email" type="email" required /></label>
        <label>Password<input name="password" type="password" required minLength={8} /></label>
        <label>Confirm Password<input name="password_confirm" type="password" required minLength={8} /></label>
        <div className="card">
          <div style={{ marginBottom: 8 }}>Captcha: {captcha.question} <button type="button" className="button small button-outline" onClick={loadCaptcha} style={{ marginLeft: 8 }}>Refresh</button></div>
          <label>Your Answer<input name="captcha_answer" type="text" required /></label>
        </div>
        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}
        <button className="button" disabled={loading}>{loading ? 'Creating...' : 'Create account'}</button>
      </form>
      <p>Already have an account? <Link to="/login">Log in</Link></p>
    </section>
  )
}
