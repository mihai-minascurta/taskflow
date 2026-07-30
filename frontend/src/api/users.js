import apiClient from './client'

export async function listUsers() {
  const { data } = await apiClient.get('/api/users')
  return data
}
