const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8080'

export async function apiFetch(path, { method = 'GET', body, token } = {}) {
  const headers = { 'Content-Type': 'application/json' }
  if (token) headers['Authorization'] = `Bearer ${token}`
  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  })
  if (!res.ok) {
    const text = await res.text()
    let err
    try { err = JSON.parse(text) } catch { err = { detail: text } }
    throw new Error(err.detail || 'Request failed')
  }
  return res.json()
}
