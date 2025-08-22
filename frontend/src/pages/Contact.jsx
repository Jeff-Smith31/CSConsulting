import React from 'react'

import { apiFetch } from '../api'

export default function Contact() {
  const [loading, setLoading] = React.useState(false)
  const [error, setError] = React.useState('')
  const [success, setSuccess] = React.useState('')

  async function onSubmit(e) {
    e.preventDefault()
    setError(''); setSuccess(''); setLoading(true)
    const form = new FormData(e.currentTarget)
    const name = form.get('name')
    const email = form.get('email')
    const message = form.get('message')
    try {
      await apiFetch('/contact', { method: 'POST', body: { name, email, message } })
      setSuccess('Thanks! We received your message and will get back to you soon.')
      e.currentTarget.reset()
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <section>
      <h2>Contact</h2>
      <form onSubmit={onSubmit}>
        <label>Name<input name="name" required /></label>
        <label>Email<input name="email" type="email" required /></label>
        <label>Message<textarea name="message" required rows={5}></textarea></label>
        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}
        <button className="button" disabled={loading}>{loading ? 'Sending...' : 'Send'}</button>
      </form>
    </section>
  )
}
