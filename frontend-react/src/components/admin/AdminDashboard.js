import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  Box,
  Tabs,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  Chip,
  Grid,
  Card,
  CardContent,
  TextField,
  Alert,
} from '@mui/material';
import { adminAPI, withApiFeedback } from '../../services/api';
import {
  translate,
  translateModerationAction,
  translateModerationCategory,
} from '../../i18n/translations';

function AdminDashboard({ uiLanguage = 'english' }) {
  const [tabValue, setTabValue] = useState(0);
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [violations, setViolations] = useState([]);
  const [lexiconInfo, setLexiconInfo] = useState(null);
  const [lexiconLoading, setLexiconLoading] = useState(false);
  const [lexiconText, setLexiconText] = useState('');
  const [lexiconMessage, setLexiconMessage] = useState('');
  const [lexiconMessageSeverity, setLexiconMessageSeverity] = useState('success');
  const [adminActionMessage, setAdminActionMessage] = useState('');
  const [adminActionSeverity, setAdminActionSeverity] = useState('success');

  useEffect(() => {
    fetchStatistics();
    fetchUsers();
    fetchViolations();
  }, []);

  const fetchStatistics = async () => {
    try {
      const response = await adminAPI.getStatistics();
      setStats(response.data.statistics);
    } catch (err) {
      console.error('Failed to fetch statistics:', err);
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await adminAPI.getUsers();
      setUsers(response.data.users || []);
    } catch (err) {
      console.error('Failed to fetch users:', err);
    }
  };

  const fetchViolations = async () => {
    try {
      const response = await adminAPI.getViolations();
      setViolations(response.data.violations || []);
    } catch (err) {
      console.error('Failed to fetch violations:', err);
    }
  };

  const setLexiconErrorMessage = (message) => {
    if (!message) {
      setLexiconMessage('');
      return;
    }
    setLexiconMessage(message);
    setLexiconMessageSeverity('error');
  };

  const setLexiconSuccessMessage = (message) => {
    setLexiconMessage(message);
    setLexiconMessageSeverity('success');
  };

  const setAdminErrorMessage = (message) => {
    if (!message) {
      return;
    }
    setAdminActionMessage(message);
    setAdminActionSeverity('error');
  };

  const setAdminSuccessMessage = (message) => {
    setAdminActionMessage(message);
    setAdminActionSeverity('success');
  };

  const handleReloadLexicon = async () => {
    setLexiconLoading(true);
    const result = await withApiFeedback({
      request: () => adminAPI.reloadLexicon(),
      uiLanguage,
      errorFallback: translate(uiLanguage, 'lexiconReloadFailed'),
      successFallback: translate(uiLanguage, 'lexiconReloaded'),
      setError: setLexiconErrorMessage,
      setSuccess: setLexiconSuccessMessage,
    });

    if (result.ok) {
      setLexiconInfo(result.response.data);
    }

    setLexiconLoading(false);
  };

  const handleGetLexiconStats = async () => {
    try {
      const response = await adminAPI.getLexiconStats();
      setLexiconInfo(response.data);
    } catch (err) {
      console.error('Failed to get lexicon stats:', err);
    }
  };

  const handleUpdateLexicon = async (mode) => {
    setLexiconLoading(true);
    const result = await withApiFeedback({
      request: () => adminAPI.updateLexicon(lexiconText, mode),
      uiLanguage,
      errorFallback: translate(uiLanguage, 'lexiconUpdateFailed'),
      successFallback: mode === 'append' ? translate(uiLanguage, 'lexiconAppended') : translate(uiLanguage, 'lexiconReplaced'),
      setError: setLexiconErrorMessage,
      setSuccess: setLexiconSuccessMessage,
    });

    if (result.ok) {
      setLexiconInfo(result.response.data);
      setLexiconText('');
    }

    setLexiconLoading(false);
  };

  const handleWarnUser = async (userId) => {
    const result = await withApiFeedback({
      request: () => adminAPI.warnUser(userId),
      uiLanguage,
      errorFallback: translate(uiLanguage, 'adminActionFailed'),
      setError: setAdminErrorMessage,
      setSuccess: setAdminSuccessMessage,
    });

    if (result.ok) {
      fetchUsers();
      fetchStatistics();
    }
  };

  const handleSuspendUser = async (userId) => {
    const result = await withApiFeedback({
      request: () => adminAPI.suspendUser(userId),
      uiLanguage,
      errorFallback: translate(uiLanguage, 'adminActionFailed'),
      setError: setAdminErrorMessage,
      setSuccess: setAdminSuccessMessage,
    });

    if (result.ok) {
      fetchUsers();
      fetchStatistics();
    }
  };

  const handleUnsuspendUser = async (userId) => {
    const result = await withApiFeedback({
      request: () => adminAPI.unsuspendUser(userId),
      uiLanguage,
      errorFallback: translate(uiLanguage, 'adminActionFailed'),
      setError: setAdminErrorMessage,
      setSuccess: setAdminSuccessMessage,
    });

    if (result.ok) {
      fetchUsers();
      fetchStatistics();
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        {translate(uiLanguage, 'adminDashboard')}
      </Typography>

      {adminActionMessage && (
        <Alert severity={adminActionSeverity} sx={{ mb: 2 }}>
          {adminActionMessage}
        </Alert>
      )}

      {/* Statistics Cards */}
      {stats && (
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>
                  {translate(uiLanguage, 'totalUsers')}
                </Typography>
                <Typography variant="h4">{stats.total_users}</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>
                  {translate(uiLanguage, 'suspendedUsers')}
                </Typography>
                <Typography variant="h4" color="error">
                  {stats.suspended_users}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>
                  {translate(uiLanguage, 'totalViolations')}
                </Typography>
                <Typography variant="h4">{stats.total_violations}</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>
                  {translate(uiLanguage, 'hateSpeechPercent')}
                </Typography>
                <Typography variant="h4" color="warning.main">
                  {stats.hate_speech_percentage}%
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Lexicon Controls */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
        <Button variant="contained" onClick={handleReloadLexicon} disabled={lexiconLoading}>
          {lexiconLoading ? translate(uiLanguage, 'reloadingLexicon') : translate(uiLanguage, 'reloadLexicon')}
        </Button>
        {lexiconInfo && lexiconInfo.success && (
          <Typography variant="body2" color="text.secondary">
            {translate(uiLanguage, 'loadedLexiconInfo')} {lexiconInfo.words_count} {translate(uiLanguage, 'words')} {translate(uiLanguage, 'and')} {lexiconInfo.phrases_count} {translate(uiLanguage, 'phrases')} {translate(uiLanguage, 'from')} {lexiconInfo.path}
          </Typography>
        )}
        <Button variant="outlined" onClick={handleGetLexiconStats}>
          {translate(uiLanguage, 'getLexiconStats')}
        </Button>
      </Box>

      {/* Lexicon Management */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          {translate(uiLanguage, 'lexiconManagement')}
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
          {translate(uiLanguage, 'lexiconManagementHelp')}
        </Typography>
        <TextField
          value={lexiconText}
          onChange={(e) => setLexiconText(e.target.value)}
          placeholder={translate(uiLanguage, 'lexiconPlaceholder')}
          fullWidth
          multiline
          minRows={4}
          sx={{ mb: 2 }}
        />
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button variant="outlined" disabled={!lexiconText.trim() || lexiconLoading} onClick={() => handleUpdateLexicon('append')}>
            {translate(uiLanguage, 'append')}
          </Button>
          <Button variant="contained" color="warning" disabled={!lexiconText.trim() || lexiconLoading} onClick={() => handleUpdateLexicon('replace')}>
            {translate(uiLanguage, 'replace')}
          </Button>
        </Box>
        {lexiconMessage && (
          <Alert severity={lexiconMessageSeverity} sx={{ mt: 2 }}>
            {lexiconMessage}
          </Alert>
        )}
      </Paper>

      <Paper>
        <Tabs value={tabValue} onChange={(e, v) => setTabValue(v)}>
          <Tab label={translate(uiLanguage, 'users')} />
          <Tab label={translate(uiLanguage, 'violations')} />
        </Tabs>

        <Box sx={{ p: 3 }}>
          {/* Users Tab */}
          {tabValue === 0 && (
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>{translate(uiLanguage, 'username')}</TableCell>
                    <TableCell>{translate(uiLanguage, 'email')}</TableCell>
                    <TableCell>{translate(uiLanguage, 'warnings')}</TableCell>
                    <TableCell>{translate(uiLanguage, 'status')}</TableCell>
                    <TableCell>{translate(uiLanguage, 'actions')}</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {users.map((user) => (
                    <TableRow key={user.id}>
                      <TableCell>{user.username}</TableCell>
                      <TableCell>{user.email}</TableCell>
                      <TableCell>
                        <Chip
                          label={`${user.warning_count}/3`}
                          color={user.warning_count >= 2 ? 'error' : 'default'}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>
                        {user.is_suspended ? (
                          <Chip label={translate(uiLanguage, 'suspended')} color="error" size="small" />
                        ) : (
                          <Chip label={translate(uiLanguage, 'active')} color="success" size="small" />
                        )}
                      </TableCell>
                      <TableCell>
                        <Box sx={{ display: 'flex', gap: 1 }}>
                          {!user.is_suspended ? (
                            <>
                              <Button
                                size="small"
                                variant="outlined"
                                color="warning"
                                onClick={() => handleWarnUser(user.id)}
                              >
                                {translate(uiLanguage, 'warn')}
                              </Button>
                              <Button
                                size="small"
                                variant="outlined"
                                color="error"
                                onClick={() => handleSuspendUser(user.id)}
                              >
                                {translate(uiLanguage, 'suspend')}
                              </Button>
                            </>
                          ) : (
                            <Button
                              size="small"
                              variant="outlined"
                              color="success"
                              onClick={() => handleUnsuspendUser(user.id)}
                            >
                              {translate(uiLanguage, 'unsuspend')}
                            </Button>
                          )}
                        </Box>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}

          {/* Violations Tab */}
          {tabValue === 1 && (
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>{translate(uiLanguage, 'user')}</TableCell>
                    <TableCell>{translate(uiLanguage, 'content')}</TableCell>
                    <TableCell>{translate(uiLanguage, 'category')}</TableCell>
                    <TableCell>{translate(uiLanguage, 'confidence')}</TableCell>
                    <TableCell>{translate(uiLanguage, 'action')}</TableCell>
                    <TableCell>{translate(uiLanguage, 'date')}</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {violations.map((violation) => (
                    <TableRow key={violation.id}>
                      <TableCell>{violation.username}</TableCell>
                      <TableCell>
                        <Typography variant="body2" noWrap sx={{ maxWidth: 200 }}>
                          {violation.content}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Chip label={translateModerationCategory(uiLanguage, violation.category)} size="small" />
                      </TableCell>
                      <TableCell>{(violation.confidence_score * 100).toFixed(0)}%</TableCell>
                      <TableCell>
                        <Chip
                          label={translateModerationAction(uiLanguage, violation.action_taken)}
                          color={violation.action_taken === 'suspension' ? 'error' : 'warning'}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>
                        {new Date(violation.timestamp).toLocaleDateString()}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </Box>
      </Paper>
    </Container>
  );
}

export default AdminDashboard;
