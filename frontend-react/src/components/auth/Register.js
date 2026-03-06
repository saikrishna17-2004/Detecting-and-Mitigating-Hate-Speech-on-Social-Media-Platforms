import React, { useState } from 'react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  TextField,
  Button,
  Typography,
  Paper,
  Link,
  Alert,
} from '@mui/material';
import { authAPI, withApiFeedback } from '../../services/api';
import { translate } from '../../i18n/translations';

function Register({ onRegister, uiLanguage = 'english' }) {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // Validate passwords match
    if (formData.password !== formData.confirmPassword) {
      setError(translate(uiLanguage, 'passwordsDoNotMatch'));
      return;
    }

    setLoading(true);

    const { confirmPassword, ...registrationData } = formData;
    const result = await withApiFeedback({
      request: () => authAPI.register(registrationData),
      uiLanguage,
      errorFallback: translate(uiLanguage, 'registrationFailed'),
      setError,
    });

    if (result.ok) {
      const userData = result.response.data.user;
      onRegister(userData);
      navigate('/');
    }

    setLoading(false);
  };

  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Paper
          elevation={0}
          sx={{
            padding: 4,
            width: '100%',
            border: '1px solid #dbdbdb',
          }}
        >
          <Typography
            component="h1"
            variant="h4"
            align="center"
            sx={{
              fontFamily: "'Pacifico', cursive",
              marginBottom: 1,
            }}
          >
            {translate(uiLanguage, 'appName')}
          </Typography>
          <Typography
            variant="body2"
            align="center"
            color="text.secondary"
            sx={{ mb: 3 }}
          >
            {translate(uiLanguage, 'signupTagline')}
          </Typography>

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          <Box component="form" onSubmit={handleSubmit}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label={translate(uiLanguage, 'email')}
              name="email"
              autoComplete="email"
              autoFocus
              value={formData.email}
              onChange={handleChange}
              size="small"
            />
            <TextField
              margin="normal"
              required
              fullWidth
              id="username"
              label={translate(uiLanguage, 'username')}
              name="username"
              autoComplete="username"
              value={formData.username}
              onChange={handleChange}
              size="small"
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label={translate(uiLanguage, 'password')}
              type="password"
              id="password"
              autoComplete="new-password"
              value={formData.password}
              onChange={handleChange}
              size="small"
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="confirmPassword"
              label={translate(uiLanguage, 'confirmPassword')}
              type="password"
              id="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              size="small"
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
              disabled={loading}
            >
              {loading ? translate(uiLanguage, 'signingUp') : translate(uiLanguage, 'signUpAction')}
            </Button>
          </Box>
        </Paper>

        <Paper
          elevation={0}
          sx={{
            marginTop: 2,
            padding: 2,
            width: '100%',
            border: '1px solid #dbdbdb',
            textAlign: 'center',
          }}
        >
          <Typography variant="body2">
            {translate(uiLanguage, 'haveAccount')}{' '}
            <Link component={RouterLink} to="/login" underline="none">
              {translate(uiLanguage, 'logIn')}
            </Link>
          </Typography>
        </Paper>
      </Box>
    </Container>
  );
}

export default Register;
