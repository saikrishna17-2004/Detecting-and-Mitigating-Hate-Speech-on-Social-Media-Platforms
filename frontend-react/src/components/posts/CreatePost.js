import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  IconButton,
  Alert,
} from '@mui/material';
import { PhotoCamera, Close } from '@mui/icons-material';
import { postAPI, analysisAPI } from '../../services/api';

function CreatePost({ user, onModerationAlert }) {
  const [caption, setCaption] = useState('');
  const [imagePreview, setImagePreview] = useState(null);
  const [imageFile, setImageFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImageFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleRemoveImage = () => {
    setImageFile(null);
    setImagePreview(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // First, analyze caption for hate speech
      if (caption.trim()) {
        const analysisResponse = await analysisAPI.analyzeText(
          caption,
          user.id,
          user.username
        );

        if (analysisResponse.data.result.is_hate_speech) {
          onModerationAlert({
            type: analysisResponse.data.action_taken,
            message: analysisResponse.data.message,
            category: analysisResponse.data.result.category,
          });

          // If suspended, don't create post
          if (analysisResponse.data.action_taken === 'suspended') {
            setLoading(false);
            return;
          }
        }
      }

      // Create post with image URL (for now, use placeholder or base64)
      const postData = {
        content: caption,
        user_id: user.id,
        image_url: imagePreview || null, // Use base64 preview as image URL
      };

      await postAPI.createPost(postData);
      navigate('/');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create post');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm">
      <Paper sx={{ mt: 4, p: 3 }}>
        <Typography variant="h5" gutterBottom>
          Create New Post
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Box component="form" onSubmit={handleSubmit}>
          {imagePreview ? (
            <Box sx={{ position: 'relative', mb: 2 }}>
              <img
                src={imagePreview}
                alt="Preview"
                style={{
                  width: '100%',
                  maxHeight: 400,
                  objectFit: 'contain',
                  borderRadius: 8,
                }}
              />
              <IconButton
                onClick={handleRemoveImage}
                sx={{
                  position: 'absolute',
                  top: 8,
                  right: 8,
                  backgroundColor: 'rgba(0, 0, 0, 0.5)',
                  color: 'white',
                  '&:hover': {
                    backgroundColor: 'rgba(0, 0, 0, 0.7)',
                  },
                }}
              >
                <Close />
              </IconButton>
            </Box>
          ) : (
            <Button
              component="label"
              variant="outlined"
              fullWidth
              startIcon={<PhotoCamera />}
              sx={{ mb: 2, py: 2 }}
            >
              Upload Photo
              <input
                type="file"
                hidden
                accept="image/*"
                onChange={handleImageChange}
              />
            </Button>
          )}

          <TextField
            fullWidth
            multiline
            rows={4}
            placeholder="Write a caption..."
            value={caption}
            onChange={(e) => setCaption(e.target.value)}
            sx={{ mb: 2 }}
          />

          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button
              variant="outlined"
              fullWidth
              onClick={() => navigate('/')}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="contained"
              fullWidth
              disabled={loading || (!caption.trim() && !imageFile)}
            >
              {loading ? 'Sharing...' : 'Share'}
            </Button>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
}

export default CreatePost;
