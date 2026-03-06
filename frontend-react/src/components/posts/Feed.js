import React, { useState, useEffect, useCallback } from 'react';
import { Container, Box, CircularProgress, Typography } from '@mui/material';
import { postAPI, userAPI } from '../../services/api';
import PostCard from './PostCard';
import { translate } from '../../i18n/translations';

function Feed({ user, onModerationAlert, uiLanguage = 'english', onLanguageChange }) {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [followLoadingByUser, setFollowLoadingByUser] = useState({});

  const fetchPosts = useCallback(async () => {
    try {
      setError('');
      const response = await postAPI.getFeed(1, user?.id);
      setPosts(response.data.posts || []);
    } catch (err) {
      setError(translate(uiLanguage, 'failedLoadPosts'));
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [uiLanguage, user]);

  useEffect(() => {
    fetchPosts();
  }, [fetchPosts]);

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
      const response = await postAPI.addComment(postId, commentText, user?.id, user?.username);
      
      // Check for hate speech detection
      if (response.data.moderation_alert) {
        onModerationAlert(response.data.moderation_alert);
      }

      // Update post with new comment
      setPosts((prevPosts) => prevPosts.map((post) => {
        if (post.id !== postId) {
          return post;
        }

        const existingComments = Array.isArray(post.comments) ? post.comments : [];
        return { ...post, comments: [...existingComments, response.data.comment] };
      }));
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

  const handleFollowToggle = async (targetUserId, currentlyFollowing) => {
    if (!user || !targetUserId || targetUserId === user.id) {
      return;
    }

    try {
      setFollowLoadingByUser((prev) => ({ ...prev, [targetUserId]: true }));
      if (currentlyFollowing) {
        await userAPI.unfollowUser(targetUserId, user.id);
      } else {
        await userAPI.followUser(targetUserId, user.id);
      }

      setPosts((prevPosts) => prevPosts.map((post) => (
        post.user_id === targetUserId
          ? { ...post, is_following: !currentlyFollowing }
          : post
      )));
    } catch (err) {
      console.error('Failed to update follow status:', err);
    } finally {
      setFollowLoadingByUser((prev) => ({ ...prev, [targetUserId]: false }));
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
          {translate(uiLanguage, 'noPostsFeed')}
        </Typography>
      ) : (
        posts.map(post => (
          <PostCard
            key={post.id}
            post={post}
            currentUser={user}
            uiLanguage={uiLanguage}
            onLike={handleLike}
            onUnlike={handleUnlike}
            onComment={handleComment}
            onDelete={handleDelete}
            onFollowToggle={handleFollowToggle}
            followLoading={!!followLoadingByUser[post.user_id]}
            onLanguageChange={onLanguageChange}
          />
        ))
      )}
    </Container>
  );
}

export default Feed;
