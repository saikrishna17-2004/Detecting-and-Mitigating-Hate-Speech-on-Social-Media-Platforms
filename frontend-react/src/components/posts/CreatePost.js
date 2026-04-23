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
import { postAPI, analysisAPI, withApiFeedback } from '../../services/api';
import IndianLanguageKeyboard from '../keyboard/IndianLanguageKeyboard';
import { translate } from '../../i18n/translations';

function CreatePost({ user, onModerationAlert, uiLanguage = 'english', onLanguageChange }) {
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
      if (!user || user.id === undefined || user.id === null) {
        setError(translate(uiLanguage, 'sessionExpired'));
        setLoading(false);
        return;
      }

      // First, analyze caption for hate speech
      if (caption.trim()) {
        const analysisResponse = await analysisAPI.analyzeText(
          caption,
          user.id,
          user.username
        );

        const accountSuspended =
          analysisResponse.data?.account_suspended ||
          analysisResponse.data?.message_key === 'account_suspended_after_warnings';

        // Enforce moderation for all detected harmful content so users get immediate feedback.
        if (analysisResponse.data?.result?.is_hate_speech) {
          onModerationAlert({
            type: accountSuspended
              ? 'suspended'
              : (analysisResponse.data.action_taken === 'block' ? 'block' : 'warn'),
            message: analysisResponse.data.message,
            messageKey: analysisResponse.data.message_key,
            messageParams: analysisResponse.data.message_params,
            category: analysisResponse.data.result.category,
          });
          setLoading(false);
          return;
        }
      }

      // Create post with image URL (for now, use placeholder or base64)
      const postData = {
        content: caption,
        user_id: user.id,
        image_url: imagePreview || null, // Use base64 preview as image URL
      };

      const createResult = await withApiFeedback({
        request: () => postAPI.createPost(postData),
        uiLanguage,
        errorFallback: translate(uiLanguage, 'failedCreatePost'),
        setError,
      });

      if (!createResult.ok) {
        const blockedAnalysis = createResult.error?.response?.data?.analysis;
        const blockedByModeration =
          createResult.error?.response?.data?.error_key === 'post_blocked_high_confidence_hate_speech';

        if (blockedByModeration && blockedAnalysis) {
          onModerationAlert({
            type: 'block',
            message:
              createResult.error?.response?.data?.error ||
              translate(uiLanguage, 'hateSpeechDetected'),
            messageKey: createResult.error?.response?.data?.error_key,
            messageParams: {},
            category: blockedAnalysis.category,
          });
        }
        return;
      }

      navigate('/');
    } catch (err) {
      setError(err?.message || translate(uiLanguage, 'failedCreatePost'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm">
      <Paper sx={{ mt: 4, p: 3 }}>
        <Typography variant="h5" gutterBottom>
          {translate(uiLanguage, 'createNewPost')}
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
              {translate(uiLanguage, 'uploadPhoto')}
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
            placeholder={translate(uiLanguage, 'writeCaption')}
            value={caption}
            onChange={(e) => setCaption(e.target.value)}
            sx={{ mb: 0 }}
          />

          <IndianLanguageKeyboard
            value={caption}
            onChange={setCaption}
            selectedLanguage={uiLanguage}
            onLanguageChange={onLanguageChange}
          />

          <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
            <Button
              variant="outlined"
              fullWidth
              onClick={() => navigate('/')}
            >
              {translate(uiLanguage, 'cancel')}
            </Button>
            <Button
              type="submit"
              variant="contained"
              fullWidth
              disabled={loading || (!caption.trim() && !imageFile)}
            >
              {loading ? translate(uiLanguage, 'sharing') : translate(uiLanguage, 'share')}
            </Button>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
}

export default CreatePost;
