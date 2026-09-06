import apiClient from './client'

export async function sendChatMessage(message, previousResponseId) {
  const { data } = await apiClient.post('/chat', {
    message,
    previous_response_id: previousResponseId || undefined,
  })
  return data
}
