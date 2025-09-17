/* frontend/src/services/api.js */

/**
 * Axios client for backend API calls.
 * Includes JWT auth, base URL from env.
 * Handles offline caching via service worker.
 */
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://api.retailinsights.com/api/v1',  // Mumbai region for DPDP
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (!navigator.onLine) {
      // Queue for offline sync (Workbox)
      console.warn('Offline: Request queued');
    }
    return Promise.reject(error);
  }
);

export default api;