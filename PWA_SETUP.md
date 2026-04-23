# PWA Setup Guide - Mobile App Installation

Your React app is now configured as a Progressive Web App (PWA). Users can install it on iOS, Android, desktop, and tablets directly from the browser—no app store needed!

## ✅ What's Configured

- **Service Worker** - Offline functionality and caching
- **Manifest** - App name, icons, and launch settings
- **Meta Tags** - iOS support and mobile optimization
- **App Shell Caching** - Fast load times

## 🚀 Build & Deploy

### Step 1: Build the App
```powershell
cd c:\Users\nakka\Desktop\pp1\frontend-react
npm run build
```

### Step 2: Serve Securely
PWA requires **HTTPS** or localhost. Deploy to:
- **Render** (free, built-in HTTPS) ✓
- **Vercel** (free, built-in HTTPS) ✓
- **Netlify** (free, built-in HTTPS) ✓
- **Local testing**: `npm start` works fine

## 📱 Install on Mobile (After Deploy)

### iOS (iPhone/iPad)
1. Open your app URL in Safari
2. Tap **Share** (bottom menu)
3. Scroll down → Tap **"Add to Home Screen"**
4. Name it & tap **"Add"**

### Android (Chrome/Firefox)
1. Open your app URL in Chrome
2. Tap **⋮** (menu) → **"Install app"**
   OR
3. You'll see **"Install"** banner at bottom → Tap it
4. Confirm installation

### Desktop (Windows/Mac)
1. Open in Chrome/Edge
2. Click **⬇️ Install** icon in address bar
3. Select where to install
4. Opens as standalone app

## 🔧 Test Locally

### Option 1: HTTPS Testing (Recommended)
```powershell
# Install http-server with SSL support
npm install -g http-server

# Generate self-signed cert (Windows)
# Or use mkcert (https://github.com/FiloSottile/mkcert)

# Serve with SSL
http-server -p 443 -S -C cert.pem -K key.pem ./build
```

### Option 2: Localhost Testing
```powershell
cd frontend-react
npm start  # http://localhost:3000 (no PWA install prompt)
```

## 📦 Deployment Steps

### Deploy to Render (Recommended - Free)

1. **Build the React app**:
```powershell
cd frontend-react
npm run build
```

2. **Create render.yaml**:
```yaml
services:
  - type: web
    name: hate-speech-pwa
    buildCommand: npm install && npm run build
    startCommand: npx serve -s build -l 3000
    envVars:
      - key: REACT_APP_API_URL
        value: https://your-backend.onrender.com
```

3. **Push to GitHub & connect Render**

4. **Your PWA will be live at**: `https://hate-speech-pwa.onrender.com`

### Deploy to Vercel (Alternative)
```powershell
npm install -g vercel
cd frontend-react
vercel
```

### Deploy to Netlify
```powershell
npm install -g netlify-cli
cd frontend-react
netlify deploy --prod --dir build
```

## 🎯 Features Enabled

✅ Install as app on mobile/desktop
✅ Offline mode (cached pages work without internet)
✅ Push notifications (requires additional setup)
✅ App shortcuts (create/feed)
✅ Splash screen on launch
✅ Full-screen mode
✅ Custom theme color

## 🔍 Verify PWA Setup

After deploying, visit your URL and check:

```javascript
// In browser console
navigator.serviceWorker.getRegistrations()
  .then(registrations => {
    console.log('Service Workers:', registrations);
  });
```

Should show 1 active service worker.

## 📋 Checklist Before Deploy

- [ ] Backend API (Flask) deployed & running
- [ ] `REACT_APP_API_URL` env variable set
- [ ] `npm run build` succeeds
- [ ] `manifest.json` has correct app name & description
- [ ] Service worker registered in DevTools
- [ ] HTTPS enabled (required for PWA)

## 🚨 Troubleshooting

### "Install button not showing"
- Ensure HTTPS is enabled
- Check browser console for errors
- Service worker must be registered (DevTools → Application → Service Workers)
- Manifest must be valid JSON

### "App shows offline page"
- Check service worker scope in DevTools
- Verify API calls go to `/api/` path (cached differently)
- Clear browser cache: `DevTools → Application → Clear storage`

### "App not launching standalone"
- Check `display: "standalone"` in manifest.json
- Ensure icons are valid URLs or data URIs

## 📚 Next Steps

1. **Enable offline sync** - Save posts locally, sync when online
2. **Add push notifications** - Notify users of comments/likes
3. **Background sync** - Upload images when connection returns
4. **App shortcuts** - Quick-access dashboard
5. **Photo sharing** - Use device camera with `<input type="file" capture>`

## 🎨 Customize App

Edit these files:

- **App name/colors**: `frontend-react/public/manifest.json`
- **Icons/splash**: Generate at [PWA Builder](https://www.pwabuilder.com/)
- **Caching strategy**: `frontend-react/public/service-worker.js`
- **Theme**: `frontend-react/src/index.js` (theme colors)

---

**Ready to launch?** 
1. Run `npm run build`
2. Deploy to Render/Vercel
3. Share your PWA URL with users
4. Users install from browser → full app experience!
