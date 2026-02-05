import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Container,
  Box,
  Paper,
  Avatar,
  Typography,
  Grid,
  CircularProgress,
  Chip
} from '@mui/material';
import { Warning } from '@mui/icons-material';
import { userAPI } from '../../services/api';
import PostCard from '../posts/PostCard';

function Profile({ currentUser }) {
  const { userId } = useParams();
  const [user, setUser] = useState(null);
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProfile();
  }, [userId]);

  const loadProfile = async () => {
    try {
      const userData = await userAPI.getUser(userId);
      const userPosts = await userAPI.getUserPosts(userId);
      setUser(userData);
      setPosts(userPosts.posts || []);
    } catch (error) {
      console.error('Error loading profile:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  if (!user) {
    return (
      <Container maxWidth="md" sx={{ py: 4 }}>
        <Typography variant="h5">User not found</Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Paper elevation={3} sx={{ p: 4, mb: 3 }}>
        <Box display="flex" alignItems="center" mb={3}>
          <Avatar sx={{ width: 80, height: 80, bgcolor: 'primary.main', mr: 3 }}>
            {user.username[0].toUpperCase()}
          </Avatar>
          <Box>
            <Typography variant="h4">{user.username}</Typography>
            <Typography variant="body1" color="text.secondary">{user.email}</Typography>
            {user.is_suspended && (
              <Chip
                icon={<Warning />}
                label="Account Suspended"
                color="error"
                size="small"
                sx={{ mt: 1 }}
              />
            )}
          </Box>
        </Box>

        <Grid container spacing={3}>
          <Grid item xs={4}>
            <Box textAlign="center">
              <Typography variant="h5">{posts.length}</Typography>
              <Typography variant="body2" color="text.secondary">Posts</Typography>
            </Box>
          </Grid>
          <Grid item xs={4}>
            <Box textAlign="center">
              <Typography variant="h5">{user.warnings}</Typography>
              <Typography variant="body2" color="text.secondary">Warnings</Typography>
            </Box>
          </Grid>
          <Grid item xs={4}>
            <Box textAlign="center">
              <Typography variant="h5">{user.violations}</Typography>
              <Typography variant="body2" color="text.secondary">Violations</Typography>
            </Box>
          </Grid>
        </Grid>
      </Paper>

      <Typography variant="h5" gutterBottom>Posts</Typography>
      {posts.length === 0 ? (
        <Typography variant="body1" color="text.secondary">
          No posts yet
        </Typography>
      ) : (
        posts.map((post) => (
          <PostCard key={post.id} post={post} currentUser={currentUser} onUpdate={loadProfile} />
        ))
      )}
    </Container>
  );
}

export default Profile;
