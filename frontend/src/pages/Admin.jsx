import React from 'react'
import { useAuth } from '../auth.jsx'
import { apiFetch } from '../api'
import { useNavigate } from 'react-router-dom'

export default function Admin() {
  const { token } = useAuth()
  const navigate = useNavigate()
  const [isAdmin, setIsAdmin] = React.useState(false)
  const [userFilter, setUserFilter] = React.useState('')
  const [statusFilter, setStatusFilter] = React.useState('unpaid')
  const [requests, setRequests] = React.useState([])
  const [bills, setBills] = React.useState([])
  const [error, setError] = React.useState('')

  React.useEffect(() => {
    async function fetchMe() {
      try {
        const me = await apiFetch('/auth/me', { token })
        if (!me.is_admin) {
          navigate('/')
          return
        }
        setIsAdmin(true)
      } catch (e) {
        setError(e.message)
      }
    }
    fetchMe()
  }, [])

  async function load() {
    setError('')
    try {
      const qs = userFilter ? `?user_id=${encodeURIComponent(userFilter)}` : ''
      const req = await apiFetch(`/admin/service-requests${qs}`, { token })
      const qsb = `?status=${encodeURIComponent(statusFilter)}${userFilter ? `&user_id=${encodeURIComponent(userFilter)}`:''}`
      const bl = await apiFetch(`/admin/bills${qsb}`, { token })
      setRequests(req)
      setBills(bl)
    } catch (e) {
      setError(e.message)
    }
  }

  React.useEffect(() => { if (isAdmin) load() }, [isAdmin])

  return (
    <section className="admin-page">
      <div className="admin-header">
        <h2>Admin Console</h2>
        <p className="section-muted">Review service requests and billing across all users.</p>
      </div>
      {error && <div className="error">{error}</div>}
      <div className="card admin-toolbar">
        <div className="admin-filters">
          <label>Filter by User ID<input value={userFilter} onChange={e=>setUserFilter(e.target.value)} placeholder="optional user_id" /></label>
          <label>Status
            <select value={statusFilter} onChange={e=>setStatusFilter(e.target.value)}>
              <option value="unpaid">Unpaid</option>
              <option value="paid">Paid</option>
            </select>
          </label>
          <button className="button" onClick={load}>Apply</button>
        </div>
      </div>

      <div className="grid" style={{marginTop:16}}>
        <div className="card">
          <h3>Service Requests {userFilter ? `(user ${userFilter})` : '(all users)'}</h3>
          {requests.length === 0 ? <p>No requests found.</p> : (
            <ul className="list">
              {requests.map(r => (
                <li key={r.request_id}>
                  <strong>{r.title}</strong> — {r.status} — {new Date(r.created_at).toLocaleString()} — user {r.user_id}
                </li>
              ))}
            </ul>
          )}
        </div>
        <div className="card">
          <h3>Bills ({statusFilter}) {userFilter ? `(user ${userFilter})` : '(all users)'}</h3>
          {bills.length === 0 ? <p>No bills found.</p> : (
            <ul className="list">
              {bills.map(b => (
                <li key={b.bill_id}>
                  <strong>{b.description}</strong> — ${(b.amount_cents/100).toFixed(2)} — {b.status} — user {b.user_id}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </section>
  )
}
