import React, { useState } from 'react';
import { Routes, Route, Navigate, useLocation } from 'react-router-dom';
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

function RegisterRoute({ user, onRegister }) {
  const location = useLocation();
  const canAccessRegister = location.state?.fromLogin === true;

  if (user) {
    return <Navigate to="/" replace />;
  }

  if (!canAccessRegister) {
    return <Navigate to="/login" replace />;
  }

  return <Register onRegister={onRegister} />;
}

function App() {
  const [user, setUser] = useState(null);
  const [moderationAlert, setModerationAlert] = useState(null);

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    setUser(null);
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
          element={<RegisterRoute user={user} onRegister={handleLogin} />} 
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
