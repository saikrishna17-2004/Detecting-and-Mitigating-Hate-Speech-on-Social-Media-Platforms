import React, { useState, useEffect } from 'react';
import {
  Container,
  Box,
  Paper,
  Typography,
  Grid,
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  Tabs,
  Tab,
  Chip,
  CircularProgress
} from '@mui/material';
import { People, Block, Warning, TrendingUp } from '@mui/icons-material';
import { adminAPI } from '../../services/api';

function AdminDashboard() {
  const [tabValue, setTabValue] = useState(0);
  const [statistics, setStatistics] = useState(null);
  const [users, setUsers] = useState([]);
  const [violations, setViolations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [stats, usersData, violationsData] = await Promise.all([
        adminAPI.getStatistics(),
        adminAPI.getAllUsers(),
        adminAPI.getViolations()
      ]);
      setStatistics(stats);
      setUsers(usersData.users || []);
      setViolations(violationsData.violations || []);
    } catch (error) {
      console.error('Error loading dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleWarn = async (userId) => {
    try {
      await adminAPI.warnUser(userId);
      loadDashboardData();
    } catch (error) {
      console.error('Error warning user:', error);
    }
  };

  const handleSuspend = async (userId) => {
    try {
      await adminAPI.suspendUser(userId);
      loadDashboardData();
    } catch (error) {
      console.error('Error suspending user:', error);
    }
  };

  const handleUnsuspend = async (userId) => {
    try {
      await adminAPI.unsuspendUser(userId);
      loadDashboardData();
    } catch (error) {
      console.error('Error unsuspending user:', error);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        Admin Dashboard
      </Typography>

      {/* Statistics Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Total Users
                  </Typography>
                  <Typography variant="h4">
                    {statistics?.total_users || 0}
                  </Typography>
                </Box>
                <People sx={{ fontSize: 40, color: 'primary.main' }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Suspended
                  </Typography>
                  <Typography variant="h4">
                    {statistics?.suspended_users || 0}
                  </Typography>
                </Box>
                <Block sx={{ fontSize: 40, color: 'error.main' }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Violations
                  </Typography>
                  <Typography variant="h4">
                    {statistics?.total_violations || 0}
                  </Typography>
                </Box>
                <Warning sx={{ fontSize: 40, color: 'warning.main' }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Hate Rate
                  </Typography>
                  <Typography variant="h4">
                    {statistics?.hate_speech_rate?.toFixed(1) || 0}%
                  </Typography>
                </Box>
                <TrendingUp sx={{ fontSize: 40, color: 'secondary.main' }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Tabs */}
      <Paper sx={{ mb: 3 }}>
        <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)}>
          <Tab label="Users" />
          <Tab label="Violations" />
        </Tabs>
      </Paper>

      {/* Users Table */}
      {tabValue === 0 && (
        <TableContainer component={Paper}>
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
                  <TableCell>{user.warnings}</TableCell>
                  <TableCell>
                    {user.is_suspended ? (
                      <Chip label="Suspended" color="error" size="small" />
                    ) : (
                      <Chip label="Active" color="success" size="small" />
                    )}
                  </TableCell>
                  <TableCell>
                    {user.is_suspended ? (
                      <Button
                        size="small"
                        variant="outlined"
                        onClick={() => handleUnsuspend(user.id)}
                      >
                        Unsuspend
                      </Button>
                    ) : (
                      <>
                        <Button
                          size="small"
                          variant="outlined"
                          color="warning"
                          onClick={() => handleWarn(user.id)}
                          sx={{ mr: 1 }}
                        >
                          Warn
                        </Button>
                        <Button
                          size="small"
                          variant="outlined"
                          color="error"
                          onClick={() => handleSuspend(user.id)}
                        >
                          Suspend
                        </Button>
                      </>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {/* Violations Table */}
      {tabValue === 1 && (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>User</TableCell>
                <TableCell>Content</TableCell>
                <TableCell>Category</TableCell>
                <TableCell>Date</TableCell>
                <TableCell>Action</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {violations.map((violation) => (
                <TableRow key={violation.id}>
                  <TableCell>{violation.user.username}</TableCell>
                  <TableCell>{violation.content.substring(0, 50)}...</TableCell>
                  <TableCell>
                    <Chip label={violation.category} size="small" color="error" />
                  </TableCell>
                  <TableCell>{new Date(violation.created_at).toLocaleDateString()}</TableCell>
                  <TableCell>
                    <Chip label={violation.action_taken} size="small" />
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Container>
  );
}

export default AdminDashboard;
