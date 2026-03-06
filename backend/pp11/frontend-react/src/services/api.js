import axios from 'axios';

const API_BASE_URL =
  process.env.REACT_APP_API_BASE_URL ||
  (process.env.NODE_ENV === 'development' ? 'http://127.0.0.1:5000/api' : 'http://localhost:5000/api');

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Auth API
export const authAPI = {
  register: async (username, email, password) => {
    const response = await api.post('/auth/register', {
      username,
      email,
      password
    });
    return response.data;
  },

  login: async (username, password) => {
    const response = await api.post('/auth/login', {
      username,
      password
    });
    return response.data;
  },

  logout: async () => {
    const response = await api.post('/auth/logout');
    return response.data;
  }
};

// Post API
export const postAPI = {
  getFeed: async () => {
    const response = await api.get('/posts');
    return response.data;
  },

  createPost: async (content, imageUrl = null) => {
    const response = await api.post('/posts', {
      content,
      image_url: imageUrl
    });
    return response.data;
  },

  likePost: async (postId) => {
    const response = await api.post(`/posts/${postId}/like`);
    return response.data;
  },

  unlikePost: async (postId) => {
    const response = await api.post(`/posts/${postId}/unlike`);
    return response.data;
  },

  addComment: async (postId, content) => {
    const response = await api.post(`/posts/${postId}/comments`, {
      content
    });
    return response.data;
  }
};

// User API
export const userAPI = {
  getUser: async (userId) => {
    const response = await api.get(`/users/${userId}`);
    return response.data;
  },

  getUserPosts: async (userId) => {
    const response = await api.get(`/users/${userId}/posts`);
    return response.data;
  }
};

// Admin API
export const adminAPI = {
  getAllUsers: async () => {
    const response = await api.get('/users');
    return response.data;
  },

  getViolations: async () => {
    const response = await api.get('/violations');
    return response.data;
  },

  getStatistics: async () => {
    const response = await api.get('/statistics');
    return response.data;
  },

  warnUser: async (userId) => {
    const response = await api.post(`/users/${userId}/warn`);
    return response.data;
  },

  suspendUser: async (userId) => {
    const response = await api.post(`/users/${userId}/suspend`);
    return response.data;
  },

  unsuspendUser: async (userId) => {
    const response = await api.post(`/users/${userId}/unsuspend`);
    return response.data;
  }
};

export default { authAPI, postAPI, userAPI, adminAPI };
