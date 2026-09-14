import apiClient from './client'

export async function sendChatMessage(message, messages) {
  const { data } = await apiClient.post('/chat', {
    message,
    messages,
  })

  return data
}

