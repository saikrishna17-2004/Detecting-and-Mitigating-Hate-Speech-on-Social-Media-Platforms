import axios from 'axios';

// Prefer env-configured base URL; fall back to CRA proxy ('/api') in dev,
// and finally to explicit localhost for direct calls.
const API_BASE_URL =
  process.env.REACT_APP_API_BASE_URL ||
  (process.env.NODE_ENV === 'development' ? '/api' : 'http://localhost:5000/api');

// API service layer
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Auth APIs
export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  logout: () => api.post('/auth/logout'),
};

// Post APIs
export const postAPI = {
  getFeed: (page = 1) => api.get(`/posts?page=${page}`),
  createPost: (postData) => api.post('/posts', postData),
  likePost: (postId) => api.post(`/posts/${postId}/like`),
  unlikePost: (postId) => api.post(`/posts/${postId}/unlike`),
  addComment: (postId, comment) => api.post(`/posts/${postId}/comments`, { comment }),
  // Provide userId so backend can verify ownership before deleting
  deletePost: (postId, userId) => api.delete(`/posts/${postId}`, { data: { user_id: userId } }),
};

// User APIs
export const userAPI = {
  getProfile: (userId) => api.get(`/users/${userId}`),
  updateProfile: (userId, data) => api.put(`/users/${userId}`, data),
  getUserPosts: (userId) => api.get(`/users/${userId}/posts`),
};

// Hate Speech Analysis
export const analysisAPI = {
  analyzeText: (text, userId, username) => 
    api.post('/analyze', { text, user_id: userId, username }),
};

// Admin APIs
export const adminAPI = {
  getUsers: () => api.get('/users'),
  getUser: (userId) => api.get(`/users/${userId}`),
  warnUser: (userId) => api.post(`/users/${userId}/warn`),
  suspendUser: (userId) => api.post(`/users/${userId}/suspend`),
  unsuspendUser: (userId) => api.post(`/users/${userId}/unsuspend`),
  getViolations: (page = 1) => api.get(`/violations?page=${page}`),
  getStatistics: () => api.get('/statistics'),
  reloadLexicon: (path) => api.post('/admin/lexicon/reload', path ? { path } : {}),
  getLexiconStats: () => api.get('/admin/lexicon/stats'),
  updateLexicon: (content, mode = 'append', path) => api.post('/admin/lexicon/update', { content, mode, ...(path ? { path } : {}) }),
};

export default api;
