import axios from 'axios';
import { translateErrorKey, translateMessageKey } from '../i18n/translations';

// Prefer env-configured base URL; default to direct backend URL in development
// to avoid CRA proxy issues on some Windows localhost setups.
const API_BASE_URL =
  process.env.REACT_APP_API_BASE_URL ||
  (process.env.NODE_ENV === 'development' ? 'http://127.0.0.1:5000/api' : 'http://localhost:5000/api');

// API service layer
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getApiErrorMessage = (error, uiLanguage = 'english', fallbackMessage = '') => {
  const errorKey = error?.response?.data?.error_key;
  const errorText = error?.response?.data?.error;
  return translateErrorKey(uiLanguage, errorKey) || errorText || fallbackMessage || '';
};

export const getApiMessage = (response, uiLanguage = 'english', fallbackMessage = '') => {
  const messageKey = response?.data?.message_key;
  const messageParams = response?.data?.message_params;
  const messageText = response?.data?.message;
  return translateMessageKey(uiLanguage, messageKey, messageParams, messageText || fallbackMessage || '');
};

export const withApiFeedback = async ({
  request,
  uiLanguage = 'english',
  errorFallback = '',
  successFallback = '',
  setError,
  setSuccess,
}) => {
  try {
    const response = await request();
    const successMessage = getApiMessage(response, uiLanguage, successFallback);
    if (setError) {
      setError('');
    }
    if (setSuccess && successMessage) {
      setSuccess(successMessage);
    }
    return { ok: true, response, successMessage };
  } catch (error) {
    const errorMessage = getApiErrorMessage(error, uiLanguage, errorFallback);
    if (setError) {
      setError(errorMessage);
    }
    return { ok: false, error, errorMessage };
  }
};

// Auth APIs
export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  logout: () => api.post('/auth/logout'),
};

// Post APIs
export const postAPI = {
  getFeed: (page = 1, viewerId) => {
    const query = viewerId
      ? `/posts?page=${page}&viewer_id=${encodeURIComponent(viewerId)}`
      : `/posts?page=${page}`;
    return api.get(query);
  },
  createPost: (postData) => api.post('/posts', postData),
  likePost: (postId) => api.post(`/posts/${postId}/like`),
  unlikePost: (postId) => api.post(`/posts/${postId}/unlike`),
  addComment: (postId, comment, userId, username) =>
    api.post(`/posts/${postId}/comments`, { comment, user_id: userId, username }),
  // Provide userId so backend can verify ownership before deleting
  deletePost: (postId, userId) => api.delete(`/posts/${postId}`, { data: { user_id: userId } }),
};

// User APIs
export const userAPI = {
  getProfile: (userId, viewerId) => {
    const query = viewerId
      ? `/users/${userId}?viewer_id=${encodeURIComponent(viewerId)}`
      : `/users/${userId}`;
    return api.get(query);
  },
  updateProfile: (userId, data) => api.put(`/users/${userId}`, data),
  getUserPosts: (userId) => api.get(`/users/${userId}/posts`),
  searchUsers: (username, viewerId) => {
    const query = viewerId
      ? `/users?username=${encodeURIComponent(username)}&viewer_id=${encodeURIComponent(viewerId)}`
      : `/users?username=${encodeURIComponent(username)}`;
    return api.get(query);
  },
  followUser: (targetUserId, followerId) => api.post(`/users/${targetUserId}/follow`, { follower_id: followerId }),
  unfollowUser: (targetUserId, followerId) => api.post(`/users/${targetUserId}/unfollow`, { follower_id: followerId }),
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
