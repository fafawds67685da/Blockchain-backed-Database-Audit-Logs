import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000';  // Must be 8000, not 8001

const api = axios.create({
  baseURL: API_BASE,
  timeout: 60000,  // Increased to 60 seconds
  headers: {
    'Content-Type': 'application/json',
  },
});

// API Methods
export const apiService = {
  // Health check
  checkHealth: () => api.get('/'),

  // Employees
  getAllEmployees: () => api.get('/employees'),
  checkDuplicateName: (name) => api.get(`/employees/check-duplicate/${name}`),
  createEmployee: (data) => api.post('/employees', data),
  searchEmployees: (filters) => api.post('/employees/search', filters),
  deleteEmployee: (id) => api.delete(`/employees/${id}`),
  deleteAllEmployees: () => api.delete('/employees/all/truncate'),

  // Verification
  verifyEmployee: (id) => api.get(`/employees/${id}/verify`),
  verifyAll: (params) => api.get('/verify-all', { params }),

  // Tampering
  tamperData: (data) => api.post('/tamper', data),

  // Transactions
  getTransactions: () => api.get('/transactions'),

  // Gas stats
  getGasStats: () => api.get('/gas-stats'),

  // Export
  exportCSV: () => api.get('/export/csv', { responseType: 'blob' }),
  exportPDF: () => api.get('/export/pdf', { responseType: 'blob' }),

  // Dashboard
  getDashboardStats: () => api.get('/dashboard-stats'),
  getDashboardQuick: () => api.get('/dashboard-quick'),
};

export default api;
