import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Avatar,
  Box,
  Menu,
  MenuItem,
} from '@mui/material';
import {
  Home,
  AddBox,
  AccountCircle,
  AdminPanelSettings,
  ExitToApp,
} from '@mui/icons-material';

function Navbar({ user, onLogout }) {
  const [anchorEl, setAnchorEl] = React.useState(null);
  const navigate = useNavigate();

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    handleMenuClose();
    onLogout();
    navigate('/login');
  };

  return (
    <AppBar position="sticky" color="inherit" elevation={1}>
      <Toolbar>
        <Typography
          variant="h6"
          sx={{
            fontFamily: "'Pacifico', cursive",
            flexGrow: 1,
            cursor: 'pointer',
          }}
          onClick={() => navigate('/')}
        >
          Social Feed
        </Typography>

        <Box sx={{ display: 'flex', gap: 1 }}>
          <IconButton onClick={() => navigate('/')} color="inherit">
            <Home />
          </IconButton>
          <IconButton onClick={() => navigate('/create')} color="inherit">
            <AddBox />
          </IconButton>
          {user.isAdmin && (
            <IconButton onClick={() => navigate('/admin')} color="inherit">
              <AdminPanelSettings />
            </IconButton>
          )}
          <IconButton onClick={handleMenuOpen}>
            <Avatar
              sx={{ width: 32, height: 32, bgcolor: 'primary.main' }}
            >
              {user.username?.[0]?.toUpperCase()}
            </Avatar>
          </IconButton>
        </Box>

        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleMenuClose}
        >
          <MenuItem onClick={() => { handleMenuClose(); navigate(`/profile/${user.id}`); }}>
            <AccountCircle sx={{ mr: 1 }} />
            Profile
          </MenuItem>
          <MenuItem onClick={handleLogout}>
            <ExitToApp sx={{ mr: 1 }} />
            Logout
          </MenuItem>
        </Menu>
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;
