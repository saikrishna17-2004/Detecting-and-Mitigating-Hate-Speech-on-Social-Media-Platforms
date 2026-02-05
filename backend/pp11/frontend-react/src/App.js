import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Box } from '@mui/material';
import Navbar from './components/layout/Navbar';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import Feed from './components/posts/Feed';
import Profile from './components/profile/Profile';
import AdminDashboard from './components/admin/AdminDashboard';
import ModerationAlert from './components/moderation/ModerationAlert';

function App() {
  const [user, setUser] = useState(null);
  const [moderationAlert, setModerationAlert] = useState(null);

  useEffect(() => {
    // Check for stored user session
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('user');
  };

  const handleModerationAlert = (alertData) => {
    setModerationAlert(alertData);
  };

  return (
    <Box>
      {user && <Navbar user={user} onLogout={handleLogout} />}
      
      <Routes>
        <Route 
          path="/login" 
          element={!user ? <Login onLogin={handleLogin} /> : <Navigate to="/" />} 
        />
        <Route 
          path="/register" 
          element={!user ? <Register onLogin={handleLogin} /> : <Navigate to="/" />} 
        />
        <Route 
          path="/" 
          element={user ? <Feed user={user} onModerationAlert={handleModerationAlert} /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/profile/:userId" 
          element={user ? <Profile currentUser={user} /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/admin" 
          element={user && user.is_admin ? <AdminDashboard /> : <Navigate to="/" />} 
        />
      </Routes>

      {moderationAlert && (
        <ModerationAlert
          open={true}
          onClose={() => setModerationAlert(null)}
          alert={moderationAlert}
        />
      )}
    </Box>
  );
}

export default App;
