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
  Button,
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
import { translate } from '../../i18n/translations';
import IndianLanguageKeyboard from '../keyboard/IndianLanguageKeyboard';

function PostCard({
  post,
  currentUser,
  onLike,
  onUnlike,
  onComment,
  onDelete,
  onFollowToggle,
  followLoading = false,
  onLanguageChange,
  uiLanguage = 'english'
}) {
  const [commentText, setCommentText] = useState('');
  const [showComments, setShowComments] = useState(false);
  const [menuAnchor, setMenuAnchor] = useState(null);
  const [commentSuccess, setCommentSuccess] = useState('');
  const navigate = useNavigate();

  const isOwner = !!(currentUser && currentUser.id === post.user_id);
  const canFollow = !!(!isOwner && currentUser && onFollowToggle);

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
      setShowComments(true);
      setCommentSuccess(translate(uiLanguage, 'commentAdded'));
      setTimeout(() => setCommentSuccess(''), 2000);
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

  const handleFollowClick = () => {
    if (!canFollow) {
      return;
    }
    onFollowToggle(post.user_id, !!post.is_following);
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
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            {canFollow && (
              <Button
                size="small"
                variant={post.is_following ? 'outlined' : 'contained'}
                onClick={handleFollowClick}
                disabled={followLoading}
              >
                {translate(uiLanguage, post.is_following ? 'unfollow' : 'follow')}
              </Button>
            )}
            <IconButton aria-label="more" onClick={handleMenuOpen}>
              <MoreVert />
            </IconButton>
          </Box>
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
          {translate(uiLanguage, 'viewProfile')}
        </MenuItem>

        {isOwner && onDelete && (
          <MenuItem
            onClick={async () => {
              handleMenuClose();
              const ok = window.confirm(translate(uiLanguage, 'deletePostConfirm'));
              if (ok) {
                await onDelete(post.id);
              }
            }}
          >
            {translate(uiLanguage, 'deletePost')}
          </MenuItem>
        )}
      </Menu>

      {post.image_url && (
        <CardMedia
          component="img"
          height="400"
          image={post.image_url}
          alt={post.content || translate(uiLanguage, 'postImage')}
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
          {post.likes_count || 0} {translate(uiLanguage, 'likes')}
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
              {translate(uiLanguage, 'viewAll')} {post.comments.length} {translate(uiLanguage, 'comments')}
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
            placeholder={translate(uiLanguage, 'addComment')}
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
        <IndianLanguageKeyboard
          value={commentText}
          onChange={setCommentText}
          selectedLanguage={uiLanguage}
          onLanguageChange={onLanguageChange}
        />
        {commentSuccess && (
          <Typography variant="caption" color="success.main" sx={{ display: 'block', mt: 0.5 }}>
            {commentSuccess}
          </Typography>
        )}
      </CardContent>
    </Card>
  );
}

export default PostCard;
