// Shared HTTP helper with silent JWT refresh support
// Usage:
//  - Call setAuthProvider({ getAccess, refresh, logout }) once (e.g., in main.js)
//  - Use apiFetch(url, { method, headers, body }, { auth: true|false })
//    - When auth=true, it will attach Authorization: Bearer <access> if available
//    - On 401 responses, it will attempt refresh() once and retry the request

let authProvider = null

export function setAuthProvider(provider) {
  authProvider = provider || null
}

export function getAuthProvider() {
  return authProvider
}

export function normalizeErrors(data, httpStatus) {
  const err = new Error('Request failed')
  // Preserve the real HTTP status so callers (e.g., refresh logic) can react to 401/403
  err.status = typeof httpStatus === 'number' ? httpStatus : (data?.status || 400)
  err.details = data
  if (typeof data === 'string') {
    err.message = data
  } else if (data?.detail) {
    err.message = Array.isArray(data.detail) ? data.detail.join(' ') : String(data.detail)
  } else {
    const parts = []
    for (const [k, v] of Object.entries(data || {})) {
      if (Array.isArray(v)) parts.push(`${k}: ${v.join(' ')}`)
      else if (typeof v === 'string') parts.push(`${k}: ${v}`)
      else if (v && typeof v === 'object') parts.push(`${k}: ${Object.values(v).join(' ')}`)
    }
    if (parts.length) err.message = parts.join('\n')
  }
  return err
}

function ensureHeaders(h) {
  const headers = new Headers(h || {})
  if (!headers.has('Content-Type')) headers.set('Content-Type', 'application/json')
  return headers
}

async function doFetch(input, init) {
  const res = await fetch(input, init)
  let data = null
  try { data = await res.json() } catch (_) { data = {} }
  if (!res.ok) throw normalizeErrors(data, res.status)
  return data
}

export async function apiFetch(input, init = {}, options = {}) {
  const { auth = false, provider = null } = options
  const headers = ensureHeaders(init.headers)

  // Choose provider: per-request override or global
  const providerToUse = provider || authProvider

  // Attach access token if requested and available
  if (auth && providerToUse && typeof providerToUse.getAccess === 'function') {
    const access = await providerToUse.getAccess()
    if (access) headers.set('Authorization', `Bearer ${access}`)
  }

  try {
    return await doFetch(input, { ...init, headers })
  } catch (err) {
    // If unauthorized and we can refresh, try once
    if (auth && err && (err.status === 401 || err.status === 403) && providerToUse && typeof providerToUse.refresh === 'function') {
      try {
        const newAccess = await providerToUse.refresh()
        if (newAccess) {
          headers.set('Authorization', `Bearer ${newAccess}`)
          return await doFetch(input, { ...init, headers })
        }
      } catch (_) {
        // fallthrough to logout
      }
      if (providerToUse && typeof providerToUse.logout === 'function') providerToUse.logout()
    }
    throw err
  }
}
