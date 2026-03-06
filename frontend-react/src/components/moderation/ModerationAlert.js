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
import { translate, translateModerationCategory, translateModerationMessage } from '../../i18n/translations';

function ModerationAlert({ alert, onClose, uiLanguage = 'english' }) {
  const isSuspension = alert.type === 'suspended';
  const resolvedMessage = translateModerationMessage(
    uiLanguage,
    alert.messageKey,
    alert.messageParams,
    alert.message
  );

  return (
    <Dialog open={true} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>
        {isSuspension ? (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Block color="error" />
            {translate(uiLanguage, 'accountSuspended')}
          </Box>
        ) : (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Warning color="warning" />
            {translate(uiLanguage, 'contentWarning')}
          </Box>
        )}
      </DialogTitle>
      
      <DialogContent>
        <Alert severity={isSuspension ? 'error' : 'warning'}>
          <AlertTitle>
            {isSuspension ? translate(uiLanguage, 'yourAccountSuspended') : translate(uiLanguage, 'hateSpeechDetected')}
          </AlertTitle>
          {resolvedMessage}
        </Alert>

        {alert.category && (
          <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
            {translate(uiLanguage, 'category')}: <strong>{translateModerationCategory(uiLanguage, alert.category)}</strong>
          </Typography>
        )}

        <Typography variant="body2" sx={{ mt: 2 }}>
          {isSuspension ? (
            translate(uiLanguage, 'suspensionNote')
          ) : (
            translate(uiLanguage, 'warningNote')
          )}
        </Typography>
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose} variant="contained">
          {translate(uiLanguage, 'understand')}
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default ModerationAlert;

