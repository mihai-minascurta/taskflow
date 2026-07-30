import apiClient from './client'

export async function listProjects() {
  const { data } = await apiClient.get('/api/projects')
  return data
}

export async function getProject(id) {
  const { data } = await apiClient.get(`/api/projects/${id}`)
  return data
}

export async function createProject(payload) {
  const { data } = await apiClient.post('/api/projects', payload)
  return data
}

export async function updateProject(id, payload) {
  const { data } = await apiClient.put(`/api/projects/${id}`, payload)
  return data
}

export async function deleteProject(id) {
  const { data } = await apiClient.delete(`/api/projects/${id}`)
  return data
}

export async function listProjectTasks(id) {
  const { data } = await apiClient.get(`/api/projects/${id}/tasks`)
  return data
}
