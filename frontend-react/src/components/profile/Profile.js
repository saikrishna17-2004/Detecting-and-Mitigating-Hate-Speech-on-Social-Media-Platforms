import React, { useState, useEffect, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import {
  Container,
  Box,
  Avatar,
  Typography,
  Grid,
  Paper,
  CircularProgress,
} from '@mui/material';
import { userAPI, postAPI } from '../../services/api';
import PostCard from '../posts/PostCard';

function Profile({ user }) {
  const { userId } = useParams();
  const [profile, setProfile] = useState(null);
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchProfile = useCallback(async () => {
    try {
      const response = await userAPI.getProfile(userId);
      setProfile(response.data.user);
    } catch (err) {
      console.error('Failed to fetch profile:', err);
    }
  }, [userId]);

  const fetchUserPosts = useCallback(async () => {
    try {
      const response = await userAPI.getUserPosts(userId);
      setPosts(response.data.posts || []);
    } catch (err) {
      console.error('Failed to fetch posts:', err);
    } finally {
      setLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    fetchProfile();
    fetchUserPosts();
  }, [fetchProfile, fetchUserPosts]);

  const handleDelete = async (postId) => {
    try {
      if (!user || !user.id) return;
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

  if (!profile) {
    return (
      <Container>
        <Typography align="center" sx={{ mt: 4 }}>
          Profile not found
        </Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Paper sx={{ p: 3, mb: 4 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
          <Avatar
            sx={{
              width: 100,
              height: 100,
              fontSize: 40,
              bgcolor: 'primary.main',
              mr: 3,
            }}
          >
            {profile.username?.[0]?.toUpperCase()}
          </Avatar>
          <Box>
            <Typography variant="h5" gutterBottom>
              {profile.username}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {profile.email}
            </Typography>
            {profile.is_suspended && (
              <Typography variant="body2" color="error" sx={{ mt: 1 }}>
                ⚠️ Account Suspended
              </Typography>
            )}
            {profile.warning_count > 0 && (
              <Typography variant="body2" color="warning.main" sx={{ mt: 1 }}>
                Warnings: {profile.warning_count}/3
              </Typography>
            )}
          </Box>
        </Box>

        <Grid container spacing={3} textAlign="center">
          <Grid item xs={4}>
            <Typography variant="h6">{posts.length}</Typography>
            <Typography variant="body2" color="text.secondary">
              Posts
            </Typography>
          </Grid>
          <Grid item xs={4}>
            <Typography variant="h6">0</Typography>
            <Typography variant="body2" color="text.secondary">
              Followers
            </Typography>
          </Grid>
          <Grid item xs={4}>
            <Typography variant="h6">0</Typography>
            <Typography variant="body2" color="text.secondary">
              Following
            </Typography>
          </Grid>
        </Grid>
      </Paper>

      <Typography variant="h6" gutterBottom>
        Posts
      </Typography>

      {posts.length === 0 ? (
        <Typography align="center" color="text.secondary" sx={{ mt: 4 }}>
          No posts yet
        </Typography>
      ) : (
        posts.map(post => (
          <PostCard
            key={post.id}
            post={post}
            currentUser={user}
            onLike={() => {}}
            onUnlike={() => {}}
            onComment={() => {}}
            onDelete={handleDelete}
          />
        ))
      )}
    </Container>
  );
}

export default Profile;
