import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' }
});

// Интерсептор для добавления токена
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Интерсептор для обновления токена при 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      // В данном проекте refresh token не реализован для простоты,
      // просто сбрасываем и перенаправляем на логин
      localStorage.removeItem('access_token');
      window.location = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth
export const register = (email, password) => api.post('/auth/register', { email, password });
export const login = (email, password) => api.post('/auth/login', { email, password });

// Products
export const getProducts = () => api.get('/products');
export const createProduct = (data) => api.post('/products', data);
export const updateProduct = (id, data) => api.patch(`/products/${id}`, data);
export const deleteProduct = (id) => api.delete(`/products/${id}`);

// Prices
export const getPriceHistory = (productId, days = 30) => api.get(`/prices/history/${productId}?days=${days}`);
export const getProductWithPrices = (productId, days = 30) => api.get(`/prices/product/${productId}/full?days=${days}`);

export default api;