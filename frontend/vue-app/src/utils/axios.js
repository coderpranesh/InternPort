import axios from 'axios'

const apiClient = axios.create({
  baseURL: process.env.NODE_ENV === 'production' 
    ? ''  // Empty string for production as we'll use relative paths
    : 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json'
  },
  withCredentials: false
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default apiClient