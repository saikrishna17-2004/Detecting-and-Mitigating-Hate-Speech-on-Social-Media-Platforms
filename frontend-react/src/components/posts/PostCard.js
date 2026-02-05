import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Card,
  CardHeader,
  CardMedia,
  CardContent,
  CardActions,
  Avatar,
  IconButton,
  Typography,
  TextField,
  Box,
  Divider,
  Menu,
  MenuItem,
} from '@mui/material';
import {
  Favorite,
  FavoriteBorder,
  ChatBubbleOutline,
  Send,
  MoreVert,
} from '@mui/icons-material';

function PostCard({ post, currentUser, onLike, onUnlike, onComment, onDelete }) {
  const [commentText, setCommentText] = useState('');
  const [showComments, setShowComments] = useState(false);
  const [menuAnchor, setMenuAnchor] = useState(null);
  const navigate = useNavigate();

  const isOwner = !!(currentUser && currentUser.id === post.user_id);

  const handleLikeToggle = () => {
    if (post.isLiked) {
      onUnlike(post.id);
    } else {
      onLike(post.id);
    }
  };

  const handleCommentSubmit = async (e) => {
    e.preventDefault();
    if (commentText.trim()) {
      await onComment(post.id, commentText);
      setCommentText('');
    }
  };

  const handleProfileClick = () => {
    navigate(`/profile/${post.user_id}`);
  };

  const handleMenuOpen = (event) => {
    setMenuAnchor(event.currentTarget);
  };

  const handleMenuClose = () => {
    setMenuAnchor(null);
  };

  return (
    <Card sx={{ mb: 2, maxWidth: 614 }}>
      <CardHeader
        avatar={
          <Avatar 
            sx={{ bgcolor: 'primary.main', cursor: 'pointer' }}
            onClick={handleProfileClick}
          >
            {post.username?.[0]?.toUpperCase() || 'U'}
          </Avatar>
        }
        action={
          <IconButton aria-label="more" onClick={handleMenuOpen}>
            <MoreVert />
          </IconButton>
        }
        title={
          <Typography 
            variant="subtitle2" 
            fontWeight="bold"
            sx={{ cursor: 'pointer' }}
            onClick={handleProfileClick}
          >
            {post.username}
          </Typography>
        }
        subheader={new Date(post.created_at).toLocaleDateString()}
      />

      {/* Actions menu */}
      <Menu
        anchorEl={menuAnchor}
        open={Boolean(menuAnchor)}
        onClose={handleMenuClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
        transformOrigin={{ vertical: 'top', horizontal: 'right' }}
      >
        <MenuItem
          onClick={() => {
            handleMenuClose();
            handleProfileClick();
          }}
        >
          View profile
        </MenuItem>

        {isOwner && onDelete && (
          <MenuItem
            onClick={async () => {
              handleMenuClose();
              const ok = window.confirm('Delete this post?');
              if (ok) {
                await onDelete(post.id);
              }
            }}
          >
            Delete post
          </MenuItem>
        )}
      </Menu>

      {post.image_url && (
        <CardMedia
          component="img"
          height="400"
          image={post.image_url}
          alt={post.content || 'Post image'}
          sx={{ objectFit: 'cover' }}
        />
      )}

      <CardActions disableSpacing>
        <IconButton onClick={handleLikeToggle} color={post.isLiked ? 'error' : 'default'}>
          {post.isLiked ? <Favorite /> : <FavoriteBorder />}
        </IconButton>
        <IconButton onClick={() => setShowComments(!showComments)}>
          <ChatBubbleOutline />
        </IconButton>
      </CardActions>

      <CardContent sx={{ pt: 0 }}>
        <Typography variant="body2" fontWeight="bold">
          {post.likes_count || 0} likes
        </Typography>

        {post.content && (
          <Typography variant="body2" sx={{ mt: 1 }}>
            <strong>{post.username}</strong> {post.content}
          </Typography>
        )}

        {post.comments && post.comments.length > 0 && (
          <>
            <Typography
              variant="body2"
              color="text.secondary"
              sx={{ mt: 1, cursor: 'pointer' }}
              onClick={() => setShowComments(!showComments)}
            >
              View all {post.comments.length} comments
            </Typography>

            {showComments && (
              <Box sx={{ mt: 1 }}>
                {post.comments.map((comment, index) => (
                  <Typography key={index} variant="body2" sx={{ mb: 0.5 }}>
                    <strong>{comment.username}</strong> {comment.text}
                  </Typography>
                ))}
              </Box>
            )}
          </>
        )}

        <Divider sx={{ my: 1 }} />

        <Box component="form" onSubmit={handleCommentSubmit} sx={{ display: 'flex', alignItems: 'center' }}>
          <TextField
            fullWidth
            size="small"
            placeholder="Add a comment..."
            variant="standard"
            value={commentText}
            onChange={(e) => setCommentText(e.target.value)}
            InputProps={{
              disableUnderline: true,
            }}
          />
          <IconButton type="submit" color="primary" disabled={!commentText.trim()}>
            <Send />
          </IconButton>
        </Box>
      </CardContent>
    </Card>
  );
}

export default PostCard;
