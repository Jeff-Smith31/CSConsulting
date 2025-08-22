import React from 'react'
import { useAuth } from '../auth.jsx'
import { apiFetch } from '../api'

function Section({ title, children }) {
  return (
    <div className="card">
      <h3>{title}</h3>
      {children}
    </div>
  )
}

export default function Dashboard() {
  const { token } = useAuth()
  const [requests, setRequests] = React.useState([])
  const [bills, setBills] = React.useState([])
  const [error, setError] = React.useState('')

  async function load() {
    try {
      const req = await apiFetch('/service-requests', { token })
      const bl = await apiFetch('/bills', { token })
      setRequests(req)
      setBills(bl)
    } catch (e) {
      setError(e.message)
    }
  }

  React.useEffect(() => { load() }, [])

  async function onCreateRequest(e) {
    e.preventDefault()
    const form = new FormData(e.currentTarget)
    const title = form.get('title')
    const description = form.get('description')
    const priority = form.get('priority')
    await apiFetch('/service-requests', { method: 'POST', body: { title, description, priority }, token })
    e.currentTarget.reset()
    await load()
  }

  async function createDemoBill() {
    await apiFetch('/bills/demo-create', { method: 'POST', token })
    await load()
  }

  async function pay(billId) {
    await apiFetch('/payments', { method: 'POST', body: { bill_id: billId, method: 'card' }, token })
    await load()
  }

  return (
    <section>
      <h2>Dashboard</h2>
      {error && <div className="error">{error}</div>}
      <div className="grid">
        <Section title="Create Service Request">
          <form onSubmit={onCreateRequest}>
            <label>Title<input name="title" required /></label>
            <label>Description<textarea name="description" required /></label>
            <label>Priority
              <select name="priority">
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </label>
            <button className="button">Submit</button>
          </form>
        </Section>

        <Section title="Your Service Requests">
          {requests.length === 0 ? <p>No requests yet.</p> : (
            <ul className="list">
              {requests.map(r => (
                <li key={r.request_id}>
                  <strong>{r.title}</strong> — {r.status} — {new Date(r.created_at).toLocaleString()}
                </li>
              ))}
            </ul>
          )}
        </Section>

        <Section title="Your Bills">
          <button className="button button-outline" onClick={createDemoBill}>Create Demo Bill</button>
          {bills.length === 0 ? <p>No bills yet.</p> : (
            <ul className="list">
              {bills.map(b => (
                <li key={b.bill_id}>
                  <strong>{b.description}</strong> — ${(b.amount_cents/100).toFixed(2)} — {b.status}
                  {b.status === 'unpaid' && (
                    <button className="button small" onClick={() => pay(b.bill_id)} style={{ marginLeft: 8 }}>Pay</button>
                  )}
                </li>
              ))}
            </ul>
          )}
        </Section>
      </div>
    </section>
  )
}
