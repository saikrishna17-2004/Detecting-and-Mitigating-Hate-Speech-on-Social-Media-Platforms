import React, { useState } from 'react';
import {
  Card,
  CardHeader,
  CardContent,
  CardActions,
  Avatar,
  IconButton,
  Typography,
  TextField,
  Button,
  Box,
  Chip
} from '@mui/material';
import {
  Favorite,
  FavoriteBorder,
  ChatBubbleOutline
} from '@mui/icons-material';
import { Link } from 'react-router-dom';
import { postAPI } from '../../services/api';

function PostCard({ post, currentUser, onUpdate }) {
  const [showComments, setShowComments] = useState(false);
  const [commentText, setCommentText] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleLike = async () => {
    try {
      if (post.is_liked) {
        await postAPI.unlikePost(post.id);
      } else {
        await postAPI.likePost(post.id);
      }
      onUpdate();
    } catch (error) {
      console.error('Error liking post:', error);
    }
  };

  const handleComment = async () => {
    if (!commentText.trim()) return;

    setSubmitting(true);
    try {
      await postAPI.addComment(post.id, commentText);
      setCommentText('');
      onUpdate();
    } catch (error) {
      console.error('Error adding comment:', error);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Card sx={{ mb: 2 }}>
      <CardHeader
        avatar={
          <Avatar sx={{ bgcolor: 'primary.main' }}>
            {post.user.username[0].toUpperCase()}
          </Avatar>
        }
        title={
          <Link to={`/profile/${post.user.id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
            {post.user.username}
          </Link>
        }
        subheader={new Date(post.created_at).toLocaleString()}
      />
      
      {post.image_url && (
        <Box
          component="img"
          src={post.image_url}
          alt="Post"
          sx={{ width: '100%', maxHeight: 500, objectFit: 'cover' }}
        />
      )}

      <CardContent>
        <Typography variant="body1">{post.content}</Typography>
        {post.hate_detected && (
          <Chip 
            label={`Warning: ${post.hate_category}`} 
            color="error" 
            size="small" 
            sx={{ mt: 1 }} 
          />
        )}
      </CardContent>

      <CardActions disableSpacing>
        <IconButton onClick={handleLike}>
          {post.is_liked ? <Favorite color="error" /> : <FavoriteBorder />}
        </IconButton>
        <Typography variant="body2">{post.likes_count}</Typography>

        <IconButton onClick={() => setShowComments(!showComments)}>
          <ChatBubbleOutline />
        </IconButton>
        <Typography variant="body2">{post.comments?.length || 0}</Typography>
      </CardActions>

      {showComments && (
        <CardContent>
          <Box sx={{ mb: 2 }}>
            {post.comments?.map((comment, index) => (
              <Box key={index} sx={{ mb: 1 }}>
                <Typography variant="body2">
                  <strong>{comment.user.username}</strong>: {comment.content}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  {new Date(comment.created_at).toLocaleString()}
                </Typography>
              </Box>
            ))}
          </Box>
          <Box sx={{ display: 'flex', gap: 1 }}>
            <TextField
              size="small"
              fullWidth
              placeholder="Add a comment..."
              value={commentText}
              onChange={(e) => setCommentText(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleComment()}
            />
            <Button 
              variant="contained" 
              onClick={handleComment}
              disabled={submitting || !commentText.trim()}
            >
              Post
            </Button>
          </Box>
        </CardContent>
      )}
    </Card>
  );
}

export default PostCard;
