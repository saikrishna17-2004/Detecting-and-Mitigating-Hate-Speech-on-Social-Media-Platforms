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
  Dialog,
  DialogTitle,
  DialogContent,
  TextField,
  List,
  ListItem,
  ListItemButton,
  ListItemAvatar,
  ListItemText,
  Button,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  Home,
  AddBox,
  AccountCircle,
  AdminPanelSettings,
  ExitToApp,
  Search,
} from '@mui/icons-material';
import { translate } from '../../i18n/translations';
import { userAPI, getApiErrorMessage } from '../../services/api';

function Navbar({ user, onLogout, uiLanguage = 'english' }) {
  const [anchorEl, setAnchorEl] = React.useState(null);
  const [searchOpen, setSearchOpen] = React.useState(false);
  const [searchText, setSearchText] = React.useState('');
  const [searchResults, setSearchResults] = React.useState([]);
  const [searchLoading, setSearchLoading] = React.useState(false);
  const [searchError, setSearchError] = React.useState('');
  const [followLoadingByUser, setFollowLoadingByUser] = React.useState({});
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

  const handleOpenSearch = () => {
    setSearchOpen(true);
    setSearchText('');
    setSearchResults([]);
    setSearchError('');
    setFollowLoadingByUser({});
  };

  const handleCloseSearch = () => {
    setSearchOpen(false);
    setSearchText('');
    setSearchResults([]);
    setSearchError('');
    setFollowLoadingByUser({});
  };

  const runUserSearch = React.useCallback(async (username) => {
    const query = username.trim();

    if (!query || query.length < 2) {
      setSearchResults([]);
      setSearchError('');
      return;
    }

    setSearchLoading(true);
    setSearchError('');

    try {
      const response = await userAPI.searchUsers(query, user.id);
      const users = response.data?.users || [];
      const filtered = users.filter((searchedUser) => searchedUser.id !== user.id);
      setSearchResults(filtered);
    } catch (error) {
      setSearchError(getApiErrorMessage(error, uiLanguage, translate(uiLanguage, 'searchFailed')));
      setSearchResults([]);
    } finally {
      setSearchLoading(false);
    }
  }, [uiLanguage, user.id]);

  React.useEffect(() => {
    if (!searchOpen) {
      return;
    }

    const debounceTimer = setTimeout(() => {
      runUserSearch(searchText);
    }, 300);

    return () => clearTimeout(debounceTimer);
  }, [searchOpen, searchText, runUserSearch]);

  const handleSelectUser = (selectedUserId) => {
    handleCloseSearch();
    navigate(`/profile/${selectedUserId}`);
  };

  const handleFollowToggle = async (event, searchedUser) => {
    event.stopPropagation();

    const targetUserId = searchedUser.id;
    if (!targetUserId || targetUserId === user.id) {
      return;
    }

    try {
      setFollowLoadingByUser((prev) => ({ ...prev, [targetUserId]: true }));
      if (searchedUser.is_following) {
        await userAPI.unfollowUser(targetUserId, user.id);
      } else {
        await userAPI.followUser(targetUserId, user.id);
      }

      await runUserSearch(searchText);
    } catch (error) {
      setSearchError(getApiErrorMessage(error, uiLanguage, translate(uiLanguage, 'searchFailed')));
    } finally {
      setFollowLoadingByUser((prev) => ({ ...prev, [targetUserId]: false }));
    }
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
          {translate(uiLanguage, 'appName')}
        </Typography>

        <Box sx={{ display: 'flex', gap: 1 }}>
          <IconButton onClick={() => navigate('/')} color="inherit">
            <Home />
          </IconButton>
          <IconButton onClick={handleOpenSearch} color="inherit">
            <Search />
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
            {translate(uiLanguage, 'profile')}
          </MenuItem>
          <MenuItem onClick={handleLogout}>
            <ExitToApp sx={{ mr: 1 }} />
            {translate(uiLanguage, 'logout')}
          </MenuItem>
        </Menu>

        <Dialog open={searchOpen} onClose={handleCloseSearch} fullWidth maxWidth="sm">
          <DialogTitle>{translate(uiLanguage, 'searchUsers')}</DialogTitle>
          <DialogContent>
            <TextField
              fullWidth
              autoFocus
              margin="dense"
              value={searchText}
              onChange={(event) => setSearchText(event.target.value)}
              placeholder={translate(uiLanguage, 'searchByUsername')}
            />

            {searchLoading && (
              <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
                <CircularProgress size={24} />
              </Box>
            )}

            {searchError && (
              <Alert severity="error" sx={{ mt: 2 }}>
                {searchError}
              </Alert>
            )}

            {!searchLoading && !searchError && searchText.trim().length >= 2 && searchResults.length === 0 && (
              <Alert severity="info" sx={{ mt: 2 }}>
                {translate(uiLanguage, 'noUsersFound')}
              </Alert>
            )}

            <List sx={{ mt: 1 }}>
              {searchResults.map((searchedUser) => (
                <ListItem key={searchedUser.id} disablePadding>
                  <ListItemButton onClick={() => handleSelectUser(searchedUser.id)}>
                    <ListItemAvatar>
                      <Avatar sx={{ width: 32, height: 32, bgcolor: 'primary.main' }}>
                        {searchedUser.username?.[0]?.toUpperCase()}
                      </Avatar>
                    </ListItemAvatar>
                    <ListItemText
                      primary={searchedUser.username}
                      secondary={searchedUser.email}
                    />
                    <Button
                      size="small"
                      variant={searchedUser.is_following ? 'outlined' : 'contained'}
                      disabled={!!followLoadingByUser[searchedUser.id]}
                      onClick={(event) => handleFollowToggle(event, searchedUser)}
                    >
                      {translate(uiLanguage, searchedUser.is_following ? 'unfollow' : 'follow')}
                    </Button>
                  </ListItemButton>
                </ListItem>
              ))}
            </List>
          </DialogContent>
        </Dialog>
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;
