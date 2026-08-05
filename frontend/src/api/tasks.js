import apiClient from './client'

export async function createTask(payload) {
  const { data } = await apiClient.post('/tasks', payload)
  return data
}

export async function updateTask(id, payload) {
  const { data } = await apiClient.put(`/tasks/${id}`, payload)
  return data
}

export async function deleteTask(id) {
  const { data } = await apiClient.delete(`/tasks/${id}`)
  return data
}
