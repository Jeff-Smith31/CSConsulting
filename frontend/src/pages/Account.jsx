import React from 'react'
import { useAuth } from '../auth.jsx'
import { apiFetch } from '../api'

export default function Account() {
  const { token, user } = useAuth()
  const [currentPassword, setCurrentPassword] = React.useState('')
  const [newPassword, setNewPassword] = React.useState('')
  const [confirm, setConfirm] = React.useState('')
  const [saving, setSaving] = React.useState(false)
  const [msg, setMsg] = React.useState('')
  const [err, setErr] = React.useState('')

  async function onSubmit(e) {
    e.preventDefault()
    setMsg(''); setErr('')
    if (newPassword !== confirm) { setErr('New passwords do not match'); return }
    setSaving(true)
    try {
      await apiFetch('/auth/change-password', { method: 'POST', token, body: { current_password: currentPassword, new_password: newPassword } })
      setMsg('Password updated')
      setCurrentPassword(''); setNewPassword(''); setConfirm('')
    } catch (e) {
      setErr(e.message)
    } finally {
      setSaving(false)
    }
  }

  return (
    <section>
      <h2>Account</h2>
      <div className="card" style={{marginBottom:16}}>
        <p className="section-muted">Signed in as</p>
        <div><strong>{user?.email}</strong></div>
      </div>
      <div className="card">
        <h3>Change Password</h3>
        <form onSubmit={onSubmit}>
          <label>Current Password<input type="password" value={currentPassword} onChange={e=>setCurrentPassword(e.target.value)} required /></label>
          <label>New Password<input type="password" value={newPassword} onChange={e=>setNewPassword(e.target.value)} required minLength={8} /></label>
          <label>Confirm New Password<input type="password" value={confirm} onChange={e=>setConfirm(e.target.value)} required minLength={8} /></label>
          {err && <div className="error">{err}</div>}
          {msg && <div className="success">{msg}</div>}
          <button className="button" disabled={saving}>{saving ? 'Updating...' : 'Update password'}</button>
        </form>
      </div>
    </section>
  )
}
