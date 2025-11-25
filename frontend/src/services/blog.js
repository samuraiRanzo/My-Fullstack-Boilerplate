// Blog API service using apiFetch with silent refresh
// Endpoints (proxied via Vite dev server):
//  - GET    /api/blog/             (public, approved only)
//  - POST   /api/blog/             (auth, create)
//  - GET    /api/blog/my/          (auth, current user's posts)
//  - GET    /api/blog/:id/         (public if approved; otherwise author/staff only)
//  - PUT    /api/blog/:id/         (auth, author or staff)
//  - PATCH  /api/blog/:id/         (auth, author or staff)

import { apiFetch } from './http.js'

export async function listPublic() {
  return await apiFetch(`/blog/`, { method: 'GET' }, { auth: false })
}

export async function listMine(_accessToken) {
  // auth:true attaches token and auto-refreshes; parameter kept for compatibility
  return await apiFetch(`/blog/my/`, { method: 'GET' }, { auth: true })
}

export async function retrieve(id, _accessToken) {
  // If viewer is authenticated, backend may reveal pending posts
  return await apiFetch(`/blog/${id}/`, { method: 'GET' }, { auth: true })
}

export async function createPost(payload, _accessToken) {
  return await apiFetch(`/blog/`, { method: 'POST', body: payload }, { auth: true })
}

export async function updatePost(id, payload, _accessToken) {
  return await apiFetch(`/blog/${id}/`, { method: 'PUT', body: payload }, { auth: true })
}
