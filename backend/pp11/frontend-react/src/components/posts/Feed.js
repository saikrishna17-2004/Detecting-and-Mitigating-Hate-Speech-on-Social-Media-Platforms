import React, { useState, useEffect } from 'react';
import { Container, Box, Typography, CircularProgress } from '@mui/material';
import { postAPI } from '../../services/api';
import CreatePost from './CreatePost';
import PostCard from './PostCard';

function Feed({ user, onModerationAlert }) {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadFeed = async () => {
    try {
      const data = await postAPI.getFeed();
      setPosts(data.posts || []);
    } catch (error) {
      console.error('Error loading feed:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadFeed();
  }, []);

  const handlePostCreated = (newPost, moderationData) => {
    if (moderationData) {
      onModerationAlert(moderationData);
    }
    if (newPost) {
      setPosts([newPost, ...posts]);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        Feed
      </Typography>
      
      <CreatePost user={user} onPostCreated={handlePostCreated} />

      <Box sx={{ mt: 3 }}>
        {posts.length === 0 ? (
          <Typography variant="body1" color="text.secondary" align="center">
            No posts yet. Be the first to post!
          </Typography>
        ) : (
          posts.map((post) => (
            <PostCard key={post.id} post={post} currentUser={user} onUpdate={loadFeed} />
          ))
        )}
      </Box>
    </Container>
  );
}

export default Feed;
