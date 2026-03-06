import React, { useState, useEffect, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import {
  Container,
  Box,
  Avatar,
  Typography,
  Grid,
  Paper,
  Button,
  CircularProgress,
} from '@mui/material';
import { userAPI, postAPI } from '../../services/api';
import PostCard from '../posts/PostCard';
import { translate } from '../../i18n/translations';

function Profile({ user, uiLanguage = 'english' }) {
  const { userId } = useParams();
  const [profile, setProfile] = useState(null);
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [followLoading, setFollowLoading] = useState(false);

  const fetchProfile = useCallback(async () => {
    try {
      const response = await userAPI.getProfile(userId, user?.id);
      setProfile(response.data.user);
    } catch (err) {
      console.error('Failed to fetch profile:', err);
    }
  }, [userId, user]);

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

  const isOwnProfile = !!(user && profile && Number(user.id) === Number(profile.id));

  const handleFollowToggle = async () => {
    if (!user || !profile || isOwnProfile) {
      return;
    }

    try {
      setFollowLoading(true);
      const response = profile.is_following
        ? await userAPI.unfollowUser(profile.id, user.id)
        : await userAPI.followUser(profile.id, user.id);

      const updatedProfile = response.data?.user;
      if (updatedProfile) {
        setProfile(updatedProfile);
      }
    } catch (err) {
      console.error('Failed to update follow status:', err);
    } finally {
      setFollowLoading(false);
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
          {translate(uiLanguage, 'profileNotFound')}
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
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, mb: 0.5 }}>
              <Typography variant="h5">
                {profile.username}
              </Typography>
              {!isOwnProfile && (
                <Button
                  variant={profile.is_following ? 'outlined' : 'contained'}
                  size="small"
                  onClick={handleFollowToggle}
                  disabled={followLoading}
                >
                  {translate(uiLanguage, profile.is_following ? 'unfollow' : 'follow')}
                </Button>
              )}
            </Box>
            <Typography variant="body2" color="text.secondary">
              {profile.email}
            </Typography>
            {profile.is_suspended && (
              <Typography variant="body2" color="error" sx={{ mt: 1 }}>
                {translate(uiLanguage, 'accountSuspendedFlag')}
              </Typography>
            )}
            {profile.warning_count > 0 && (
              <Typography variant="body2" color="warning.main" sx={{ mt: 1 }}>
                {translate(uiLanguage, 'warnings')}: {profile.warning_count}/3
              </Typography>
            )}
          </Box>
        </Box>

        <Grid container spacing={3} textAlign="center">
          <Grid item xs={4}>
            <Typography variant="h6">{posts.length}</Typography>
            <Typography variant="body2" color="text.secondary">
              {translate(uiLanguage, 'posts')}
            </Typography>
          </Grid>
          <Grid item xs={4}>
            <Typography variant="h6">{profile.followers_count || 0}</Typography>
            <Typography variant="body2" color="text.secondary">
              {translate(uiLanguage, 'followers')}
            </Typography>
          </Grid>
          <Grid item xs={4}>
            <Typography variant="h6">{profile.following_count || 0}</Typography>
            <Typography variant="body2" color="text.secondary">
              {translate(uiLanguage, 'following')}
            </Typography>
          </Grid>
        </Grid>
      </Paper>

      <Typography variant="h6" gutterBottom>
        {translate(uiLanguage, 'posts')}
      </Typography>

      {posts.length === 0 ? (
        <Typography align="center" color="text.secondary" sx={{ mt: 4 }}>
          {translate(uiLanguage, 'noPostsYet')}
        </Typography>
      ) : (
        posts.map(post => (
          <PostCard
            key={post.id}
            post={post}
            currentUser={user}
            uiLanguage={uiLanguage}
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
