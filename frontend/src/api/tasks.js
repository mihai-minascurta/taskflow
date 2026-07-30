import apiClient from './client'

export async function createTask(payload) {
  const { data } = await apiClient.post('/api/tasks', payload)
  return data
}

export async function updateTask(id, payload) {
  const { data } = await apiClient.put(`/api/tasks/${id}`, payload)
  return data
}

export async function deleteTask(id) {
  const { data } = await apiClient.delete(`/api/tasks/${id}`)
  return data
}
