import React, { useState } from 'react';
import {
  Card,
  CardContent,
  TextField,
  Button,
  Box,
  Alert
} from '@mui/material';
import { PhotoCamera } from '@mui/icons-material';
import { postAPI } from '../../services/api';

function CreatePost({ user, onPostCreated }) {
  const [content, setContent] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    if (!content.trim()) return;

    setLoading(true);
    setError('');

    try {
      const response = await postAPI.createPost(content, imageUrl || null);
      
      // Check if post was flagged
      if (response.hate_detected) {
        onPostCreated(null, {
          action: response.action,
          category: response.category,
          score: response.hate_score
        });
      } else {
        onPostCreated(response.post, null);
      }

      setContent('');
      setImageUrl('');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create post');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card sx={{ mb: 3 }}>
      <CardContent>
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        
        <TextField
          fullWidth
          multiline
          rows={3}
          placeholder="What's on your mind?"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          sx={{ mb: 2 }}
        />

        <TextField
          fullWidth
          placeholder="Image URL (optional)"
          value={imageUrl}
          onChange={(e) => setImageUrl(e.target.value)}
          sx={{ mb: 2 }}
          InputProps={{
            startAdornment: <PhotoCamera sx={{ mr: 1, color: 'action.active' }} />
          }}
        />

        <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
          <Button
            variant="contained"
            onClick={handleSubmit}
            disabled={loading || !content.trim()}
          >
            {loading ? 'Posting...' : 'Post'}
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
}

export default CreatePost;
