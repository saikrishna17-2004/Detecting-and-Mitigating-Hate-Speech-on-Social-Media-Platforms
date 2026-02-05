import React from 'react';
import {
  Box,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Alert,
  AlertTitle,
  Typography,
} from '@mui/material';
import { Warning, Block } from '@mui/icons-material';

function ModerationAlert({ alert, onClose }) {
  const isSuspension = alert.type === 'suspended';

  return (
    <Dialog open={true} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>
        {isSuspension ? (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Block color="error" />
            Account Suspended
          </Box>
        ) : (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Warning color="warning" />
            Content Warning
          </Box>
        )}
      </DialogTitle>
      
      <DialogContent>
        <Alert severity={isSuspension ? 'error' : 'warning'}>
          <AlertTitle>
            {isSuspension ? 'Your account has been suspended' : 'Hate Speech Detected'}
          </AlertTitle>
          {alert.message}
        </Alert>

        {alert.category && (
          <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
            Category: <strong>{alert.category}</strong>
          </Typography>
        )}

        <Typography variant="body2" sx={{ mt: 2 }}>
          {isSuspension ? (
            'Your account has been suspended due to repeated violations of our community guidelines. Please contact support for more information.'
          ) : (
            'Please review our community guidelines and ensure your content follows our policies. Continued violations may result in account suspension.'
          )}
        </Typography>
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose} variant="contained">
          I Understand
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default ModerationAlert;

