import apiClient from './client'

export async function listTaskComments(taskId) {
  const { data } = await apiClient.get(`/tasks/${taskId}/comments`)
  return data
}

export async function addTaskComment(taskId, comment) {
  const { data } = await apiClient.post(`/tasks/${taskId}/comments`, { comment })
  return data
}
