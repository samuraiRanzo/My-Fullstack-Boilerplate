// Admin Blog API service (uses per-request auth provider)
// Base: /admin-api/blog/
// Pagination: DRF PageNumberPagination { count, next, previous, results }
import { apiFetch } from './http.js'

export async function adminBlogList(params = {}, provider) {
  const qs = new URLSearchParams()
  if (params.page) qs.set('page', params.page)
  if (params.page_size) qs.set('page_size', params.page_size)
  if (params.status) qs.set('status', params.status)
  if (params.author_id) qs.set('author_id', params.author_id)
  const url = `/admin-api/blog/${qs.toString() ? `?${qs.toString()}` : ''}`
  return await apiFetch(url, { method: 'GET' }, { auth: true, provider })
}

export async function adminBlogRetrieve(id, provider) {
  return await apiFetch(`/admin-api/blog/${id}/`, { method: 'GET' }, { auth: true, provider })
}

export async function adminBlogCreate(payload, provider) {
  // payload may include { title, content, status, author_id }
  return await apiFetch(`/admin-api/blog/`, {
    method: 'POST',
    body: payload,
  }, { auth: true, provider })
}

export async function adminBlogUpdate(id, payload, provider, method = 'PUT') {
  return await apiFetch(`/admin-api/blog/${id}/`, {
    method,
    body: payload,
  }, { auth: true, provider })
}

export async function adminBlogDelete(id, provider) {
  // We expect empty response body; apiFetch will attempt to JSON.parse. Backend should return 204.
  // Our doFetch currently tries to parse JSON always; for 204 it will throw on json(). Adjust by returning {} on catch, which we have.
  return await apiFetch(`/admin-api/blog/${id}/`, { method: 'DELETE' }, { auth: true, provider })
}
