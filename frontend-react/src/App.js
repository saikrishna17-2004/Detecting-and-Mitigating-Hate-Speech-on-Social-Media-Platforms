import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Box } from '@mui/material';

// Components
import Navbar from './components/layout/Navbar';
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import Feed from './components/posts/Feed';
import Profile from './components/profile/Profile';
import CreatePost from './components/posts/CreatePost';
import AdminDashboard from './components/admin/AdminDashboard';
import ModerationAlert from './components/moderation/ModerationAlert';

function App() {
  const [user, setUser] = useState(null);
  const [moderationAlert, setModerationAlert] = useState(null);

  useEffect(() => {
    // Check if user is logged in (from localStorage)
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
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

  const showModerationAlert = (alert) => {
    setModerationAlert(alert);
  };

  const closeModerationAlert = () => {
    setModerationAlert(null);
  };

  return (
    <Box sx={{ minHeight: '100vh', backgroundColor: '#fafafa' }}>
      {user && <Navbar user={user} onLogout={handleLogout} />}
      
      {moderationAlert && (
        <ModerationAlert 
          alert={moderationAlert} 
          onClose={closeModerationAlert} 
        />
      )}

      <Routes>
        <Route 
          path="/login" 
          element={user ? <Navigate to="/" /> : <Login onLogin={handleLogin} />} 
        />
        <Route 
          path="/register" 
          element={user ? <Navigate to="/" /> : <Register onRegister={handleLogin} />} 
        />
        <Route 
          path="/" 
          element={user ? <Feed user={user} onModerationAlert={showModerationAlert} /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/create" 
          element={user ? <CreatePost user={user} onModerationAlert={showModerationAlert} /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/profile/:userId" 
          element={user ? <Profile user={user} /> : <Navigate to="/login" />} 
        />
        <Route 
          path="/admin" 
          element={user && user.isAdmin ? <AdminDashboard user={user} /> : <Navigate to="/" />} 
        />
      </Routes>
    </Box>
  );
}

export default App;
