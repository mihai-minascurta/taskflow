import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Attach the fake auth token (see backend/app/routes/auth.py) to every
// outgoing request, if we have one stored.
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('taskflow_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Normalize error responses so callers can always read `error.message`.
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error.response?.data?.error ||
      error.message ||
      'Something went wrong. Please try again.'

    if (error.response?.status === 401) {
      // Fake token was invalid/missing — clear local session so the UI
      // returns to the login screen next render.
      localStorage.removeItem('taskflow_token')
      localStorage.removeItem('taskflow_user')
    }

    return Promise.reject(new Error(message))
  }
)

export default apiClient
export { API_URL }
