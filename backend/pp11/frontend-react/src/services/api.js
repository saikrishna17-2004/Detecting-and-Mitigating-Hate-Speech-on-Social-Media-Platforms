import axios from 'axios';

const API_BASE_URL = '/api';

// Auth API
export const authAPI = {
  register: async (username, email, password) => {
    const response = await axios.post(`${API_BASE_URL}/auth/register`, {
      username,
      email,
      password
    });
    return response.data;
  },

  login: async (username, password) => {
    const response = await axios.post(`${API_BASE_URL}/auth/login`, {
      username,
      password
    });
    return response.data;
  },

  logout: async () => {
    const response = await axios.post(`${API_BASE_URL}/auth/logout`);
    return response.data;
  }
};

// Post API
export const postAPI = {
  getFeed: async () => {
    const response = await axios.get(`${API_BASE_URL}/posts`);
    return response.data;
  },

  createPost: async (content, imageUrl = null) => {
    const response = await axios.post(`${API_BASE_URL}/posts`, {
      content,
      image_url: imageUrl
    });
    return response.data;
  },

  likePost: async (postId) => {
    const response = await axios.post(`${API_BASE_URL}/posts/${postId}/like`);
    return response.data;
  },

  unlikePost: async (postId) => {
    const response = await axios.post(`${API_BASE_URL}/posts/${postId}/unlike`);
    return response.data;
  },

  addComment: async (postId, content) => {
    const response = await axios.post(`${API_BASE_URL}/posts/${postId}/comments`, {
      content
    });
    return response.data;
  }
};

// User API
export const userAPI = {
  getUser: async (userId) => {
    const response = await axios.get(`${API_BASE_URL}/users/${userId}`);
    return response.data;
  },

  getUserPosts: async (userId) => {
    const response = await axios.get(`${API_BASE_URL}/users/${userId}/posts`);
    return response.data;
  }
};

// Admin API
export const adminAPI = {
  getAllUsers: async () => {
    const response = await axios.get(`${API_BASE_URL}/users`);
    return response.data;
  },

  getViolations: async () => {
    const response = await axios.get(`${API_BASE_URL}/violations`);
    return response.data;
  },

  getStatistics: async () => {
    const response = await axios.get(`${API_BASE_URL}/statistics`);
    return response.data;
  },

  warnUser: async (userId) => {
    const response = await axios.post(`${API_BASE_URL}/users/${userId}/warn`);
    return response.data;
  },

  suspendUser: async (userId) => {
    const response = await axios.post(`${API_BASE_URL}/users/${userId}/suspend`);
    return response.data;
  },

  unsuspendUser: async (userId) => {
    const response = await axios.post(`${API_BASE_URL}/users/${userId}/unsuspend`);
    return response.data;
  }
};

export default { authAPI, postAPI, userAPI, adminAPI };
