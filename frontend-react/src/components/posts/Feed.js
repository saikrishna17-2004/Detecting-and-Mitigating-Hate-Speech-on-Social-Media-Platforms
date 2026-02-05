import React, { useState, useEffect } from 'react';
import { Container, Box, CircularProgress, Typography } from '@mui/material';
import { postAPI } from '../../services/api';
import PostCard from './PostCard';

function Feed({ user, onModerationAlert }) {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      const response = await postAPI.getFeed();
      setPosts(response.data.posts || []);
    } catch (err) {
      setError('Failed to load posts');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleLike = async (postId) => {
    try {
      await postAPI.likePost(postId);
      // Update local state
      setPosts(posts.map(post => 
        post.id === postId 
          ? { ...post, likes_count: post.likes_count + 1, isLiked: true }
          : post
      ));
    } catch (err) {
      console.error('Failed to like post:', err);
    }
  };

  const handleUnlike = async (postId) => {
    try {
      await postAPI.unlikePost(postId);
      setPosts(posts.map(post => 
        post.id === postId 
          ? { ...post, likes_count: post.likes_count - 1, isLiked: false }
          : post
      ));
    } catch (err) {
      console.error('Failed to unlike post:', err);
    }
  };

  const handleComment = async (postId, commentText) => {
    try {
      const response = await postAPI.addComment(postId, commentText);
      
      // Check for hate speech detection
      if (response.data.moderation_alert) {
        onModerationAlert(response.data.moderation_alert);
      }

      // Update post with new comment
      setPosts(posts.map(post => 
        post.id === postId 
          ? { ...post, comments: [...post.comments, response.data.comment] }
          : post
      ));
    } catch (err) {
      console.error('Failed to add comment:', err);
    }
  };

  const handleDelete = async (postId) => {
    try {
      if (!user || !user.id) {
        console.warn('No current user set; cannot delete post');
        return;
      }

      await postAPI.deletePost(postId, user.id);
      setPosts(posts.filter(p => p.id !== postId));
    } catch (err) {
      console.error('Failed to delete post:', err);
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Container maxWidth="sm">
        <Typography color="error" align="center" sx={{ mt: 4 }}>
          {error}
        </Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="sm" sx={{ mt: 2, mb: 4 }}>
      {posts.length === 0 ? (
        <Typography align="center" color="text.secondary" sx={{ mt: 4 }}>
          No posts yet. Start sharing your moments!
        </Typography>
      ) : (
        posts.map(post => (
          <PostCard
            key={post.id}
            post={post}
            currentUser={user}
            onLike={handleLike}
            onUnlike={handleUnlike}
            onComment={handleComment}
            onDelete={handleDelete}
          />
        ))
      )}
    </Container>
  );
}

export default Feed;
