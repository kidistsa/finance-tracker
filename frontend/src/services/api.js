import axios from 'axios';

const API_BASE_URL = 'http://localhost:9000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests - FIXED
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;  // ← Fixed this line
  }
  return config;
});

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;

// Auth Services
export const authService = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
};

// Transaction Services
export const transactionService = {
  getAll: (params) => api.get('/transactions', { params }),
  getSummary: (period = 'month') => api.get('/transactions/summary', { params: { period } }),
  uploadCSV: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/transactions/upload-csv', formData, {
      headers: { 
        'Content-Type': 'multipart/form-data',
      },
      params: { bank_format: 'default' }
    });
  },
};

// Budget Services
export const budgetService = {
  getAll: (month) => api.get('/budgets', { params: { month } }),
  create: (data) => api.post('/budgets', data),
  delete: (id) => api.delete(`/budgets/${id}`),  // ← Fixed this line
};
