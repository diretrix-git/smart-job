import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
});

// Interceptor to attach JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (username, password) => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    return api.post('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
  },
  register: (username, email, password) => api.post('/auth/register', { username, email, password }),
  getMe: () => api.get('/auth/me'),
};

export const resumesAPI = {
  upload: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/resumes/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  },
};

export const recommendationsAPI = {
  getJobs: () => api.get('/recommendations/jobs'),
  getCourses: () => api.get('/recommendations/courses'),
};

export default api;
