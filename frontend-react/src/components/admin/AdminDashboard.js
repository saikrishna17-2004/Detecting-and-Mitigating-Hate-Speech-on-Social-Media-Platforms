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
import { adminAPI } from '../../services/api';

function AdminDashboard() {
  const [tabValue, setTabValue] = useState(0);
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [violations, setViolations] = useState([]);
  const [lexiconInfo, setLexiconInfo] = useState(null);
  const [lexiconLoading, setLexiconLoading] = useState(false);
  const [lexiconText, setLexiconText] = useState('');
  const [lexiconMessage, setLexiconMessage] = useState('');

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

  const handleReloadLexicon = async () => {
    try {
      setLexiconLoading(true);
      const response = await adminAPI.reloadLexicon();
      setLexiconInfo(response.data);
      setLexiconMessage('Lexicon reloaded successfully');
    } catch (err) {
      console.error('Failed to reload lexicon:', err);
      setLexiconMessage('Failed to reload lexicon');
    } finally {
      setLexiconLoading(false);
    }
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
    try {
      setLexiconLoading(true);
      const response = await adminAPI.updateLexicon(lexiconText, mode);
      setLexiconInfo(response.data);
      setLexiconMessage(mode === 'append' ? 'Words appended and reloaded' : 'Lexicon replaced and reloaded');
      setLexiconText('');
    } catch (err) {
      console.error('Failed to update lexicon:', err);
      setLexiconMessage('Failed to update lexicon');
    } finally {
      setLexiconLoading(false);
    }
  };

  const handleWarnUser = async (userId) => {
    try {
      await adminAPI.warnUser(userId);
      fetchUsers();
      fetchStatistics();
    } catch (err) {
      console.error('Failed to warn user:', err);
    }
  };

  const handleSuspendUser = async (userId) => {
    try {
      await adminAPI.suspendUser(userId);
      fetchUsers();
      fetchStatistics();
    } catch (err) {
      console.error('Failed to suspend user:', err);
    }
  };

  const handleUnsuspendUser = async (userId) => {
    try {
      await adminAPI.unsuspendUser(userId);
      fetchUsers();
      fetchStatistics();
    } catch (err) {
      console.error('Failed to unsuspend user:', err);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Admin Dashboard
      </Typography>

      {/* Statistics Cards */}
      {stats && (
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>
                  Total Users
                </Typography>
                <Typography variant="h4">{stats.total_users}</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>
                  Suspended Users
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
                  Total Violations
                </Typography>
                <Typography variant="h4">{stats.total_violations}</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent>
                <Typography color="text.secondary" gutterBottom>
                  Hate Speech %
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
          {lexiconLoading ? 'Reloading lexicon...' : 'Reload Lexicon'}
        </Button>
        {lexiconInfo && lexiconInfo.success && (
          <Typography variant="body2" color="text.secondary">
            Loaded {lexiconInfo.words_count} words and {lexiconInfo.phrases_count} phrases from {lexiconInfo.path}
          </Typography>
        )}
        <Button variant="outlined" onClick={handleGetLexiconStats}>
          Get Lexicon Stats
        </Button>
      </Box>

      {/* Lexicon Management */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Lexicon Management
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
          Paste words or phrases below (one per line), then choose Append or Replace.
        </Typography>
        <TextField
          value={lexiconText}
          onChange={(e) => setLexiconText(e.target.value)}
          placeholder={"e.g.\nfoo\nbar baz\n..."}
          fullWidth
          multiline
          minRows={4}
          sx={{ mb: 2 }}
        />
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button variant="outlined" disabled={!lexiconText.trim() || lexiconLoading} onClick={() => handleUpdateLexicon('append')}>
            Append
          </Button>
          <Button variant="contained" color="warning" disabled={!lexiconText.trim() || lexiconLoading} onClick={() => handleUpdateLexicon('replace')}>
            Replace
          </Button>
        </Box>
        {lexiconMessage && (
          <Alert severity={lexiconMessage.startsWith('Failed') ? 'error' : 'success'} sx={{ mt: 2 }}>
            {lexiconMessage}
          </Alert>
        )}
      </Paper>

      <Paper>
        <Tabs value={tabValue} onChange={(e, v) => setTabValue(v)}>
          <Tab label="Users" />
          <Tab label="Violations" />
        </Tabs>

        <Box sx={{ p: 3 }}>
          {/* Users Tab */}
          {tabValue === 0 && (
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Username</TableCell>
                    <TableCell>Email</TableCell>
                    <TableCell>Warnings</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Actions</TableCell>
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
                          <Chip label="Suspended" color="error" size="small" />
                        ) : (
                          <Chip label="Active" color="success" size="small" />
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
                                Warn
                              </Button>
                              <Button
                                size="small"
                                variant="outlined"
                                color="error"
                                onClick={() => handleSuspendUser(user.id)}
                              >
                                Suspend
                              </Button>
                            </>
                          ) : (
                            <Button
                              size="small"
                              variant="outlined"
                              color="success"
                              onClick={() => handleUnsuspendUser(user.id)}
                            >
                              Unsuspend
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
                    <TableCell>User</TableCell>
                    <TableCell>Content</TableCell>
                    <TableCell>Category</TableCell>
                    <TableCell>Confidence</TableCell>
                    <TableCell>Action</TableCell>
                    <TableCell>Date</TableCell>
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
                        <Chip label={violation.category} size="small" />
                      </TableCell>
                      <TableCell>{(violation.confidence_score * 100).toFixed(0)}%</TableCell>
                      <TableCell>
                        <Chip
                          label={violation.action_taken}
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
