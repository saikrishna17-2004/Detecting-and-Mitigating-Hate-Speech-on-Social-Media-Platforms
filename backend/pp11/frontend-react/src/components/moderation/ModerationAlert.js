import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Alert,
  Box,
  Chip
} from '@mui/material';
import { Warning, Block } from '@mui/icons-material';

function ModerationAlert({ open, onClose, alert }) {
  const isSuspension = alert.action === 'suspended';

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>
        <Box display="flex" alignItems="center" gap={1}>
          {isSuspension ? <Block color="error" /> : <Warning color="warning" />}
          <Typography variant="h6">
            {isSuspension ? 'Account Suspended' : 'Content Warning'}
          </Typography>
        </Box>
      </DialogTitle>
      
      <DialogContent>
        <Alert severity={isSuspension ? 'error' : 'warning'} sx={{ mb: 2 }}>
          {isSuspension 
            ? 'Your account has been suspended due to repeated violations.'
            : 'Your content has been flagged for review.'}
        </Alert>

        <Typography variant="body1" gutterBottom>
          <strong>Reason:</strong> Hate speech detected
        </Typography>
        
        <Typography variant="body1" gutterBottom>
          <strong>Category:</strong>{' '}
          <Chip label={alert.category} size="small" color="error" />
        </Typography>

        <Typography variant="body1" gutterBottom>
          <strong>Confidence:</strong> {(alert.score * 100).toFixed(1)}%
        </Typography>

        <Box sx={{ mt: 2, p: 2, bgcolor: 'grey.100', borderRadius: 1 }}>
          <Typography variant="body2" color="text.secondary">
            {isSuspension ? (
              <>
                Your account has been suspended after multiple violations of our community guidelines.
                Please contact support if you believe this is an error.
              </>
            ) : (
              <>
                This is a warning. Repeated violations may result in account suspension.
                Please review our community guidelines.
              </>
            )}
          </Typography>
        </Box>
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
