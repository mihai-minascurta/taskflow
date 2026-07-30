import apiClient from './client'

export async function listTaskComments(taskId) {
  const { data } = await apiClient.get(`/api/tasks/${taskId}/comments`)
  return data
}

export async function addTaskComment(taskId, comment) {
  const { data } = await apiClient.post(`/api/tasks/${taskId}/comments`, { comment })
  return data
}
