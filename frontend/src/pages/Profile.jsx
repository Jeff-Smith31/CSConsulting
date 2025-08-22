import React from 'react'
import { useAuth } from '../auth.jsx'
import { apiFetch } from '../api'

export default function Profile() {
  const { token, user, loadMe } = useAuth()
  const [firstName, setFirstName] = React.useState(user?.first_name || '')
  const [lastName, setLastName] = React.useState(user?.last_name || '')
  const [phone, setPhone] = React.useState(user?.phone || '')
  const [address, setAddress] = React.useState(user?.address || '')
  const [avatarUrl, setAvatarUrl] = React.useState(user?.avatar_url || '')
  const [displayName, setDisplayName] = React.useState(user?.name || '')
  const [saving, setSaving] = React.useState(false)
  const [msg, setMsg] = React.useState('')
  const [err, setErr] = React.useState('')

  const [newEmail, setNewEmail] = React.useState('')
  const [currentPw, setCurrentPw] = React.useState('')
  const [emailMsg, setEmailMsg] = React.useState('')
  const [emailErr, setEmailErr] = React.useState('')

  React.useEffect(() => {
    setFirstName(user?.first_name || '')
    setLastName(user?.last_name || '')
    setPhone(user?.phone || '')
    setAddress(user?.address || '')
    setAvatarUrl(user?.avatar_url || '')
    setDisplayName(user?.name || '')
  }, [user])

  async function onSubmit(e) {
    e.preventDefault()
    setErr(''); setMsg(''); setSaving(true)
    try {
      await apiFetch('/auth/profile', { method: 'PUT', token, body: {
        first_name: firstName || undefined,
        last_name: lastName || undefined,
        phone: phone || undefined,
        address: address || undefined,
        avatar_url: avatarUrl || undefined,
        name: displayName || undefined,
      } })
      setMsg('Saved!')
      await loadMe(token)
    } catch (e) {
      setErr(e.message)
    } finally {
      setSaving(false)
    }
  }

  async function onChangeEmail(e) {
    e.preventDefault()
    setEmailErr(''); setEmailMsg('')
    try {
      await apiFetch('/auth/change-email', { method: 'POST', token, body: { current_password: currentPw, new_email: newEmail } })
      setEmailMsg('Email updated. Please use the new email next time you log in.')
      setCurrentPw(''); setNewEmail('')
      await loadMe(token)
    } catch (e) {
      setEmailErr(e.message)
    }
  }

  return (
    <section>
      <h2>Your Profile</h2>
      <div className="grid">
        <div className="card">
          <h3>Contact & Profile</h3>
          <form onSubmit={onSubmit}>
            <div style={{display:'flex', gap:12, alignItems:'center'}}>
              <span className="avatar" style={{width:48,height:48}}>
                {avatarUrl ? <img src={avatarUrl} alt="avatar" /> : <span className="avatar-initial">{(user?.name||user?.email||'?')[0]?.toUpperCase?.()}</span>}
              </span>
              <label style={{flex:1}}>Avatar URL<input value={avatarUrl} onChange={e=>setAvatarUrl(e.target.value)} placeholder="https://..." /></label>
            </div>
            <label>First Name<input value={firstName} onChange={e=>setFirstName(e.target.value)} /></label>
            <label>Last Name<input value={lastName} onChange={e=>setLastName(e.target.value)} /></label>
            <label>Display Name<input value={displayName} onChange={e=>setDisplayName(e.target.value)} /></label>
            <label>Phone<input value={phone} onChange={e=>setPhone(e.target.value)} placeholder="(555) 555-5555" /></label>
            <label>Address<textarea value={address} onChange={e=>setAddress(e.target.value)} rows={3} /></label>
            {err && <div className="error">{err}</div>}
            {msg && <div className="success">{msg}</div>}
            <button className="button" disabled={saving}>{saving ? 'Saving...' : 'Save changes'}</button>
          </form>
        </div>
        <div className="card">
          <h3>Change Email</h3>
          <p className="section-muted">Current: <strong>{user?.email}</strong></p>
          <form onSubmit={onChangeEmail}>
            <label>New Email<input type="email" value={newEmail} onChange={e=>setNewEmail(e.target.value)} required /></label>
            <label>Current Password<input type="password" value={currentPw} onChange={e=>setCurrentPw(e.target.value)} required /></label>
            {emailErr && <div className="error">{emailErr}</div>}
            {emailMsg && <div className="success">{emailMsg}</div>}
            <button className="button">Update email</button>
          </form>
        </div>
      </div>
    </section>
  )
}
