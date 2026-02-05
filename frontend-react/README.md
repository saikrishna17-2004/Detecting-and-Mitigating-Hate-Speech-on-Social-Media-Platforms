# React Frontend for Hate Speech Detection

Instagram-like social media interface with real-time hate speech detection.

## Features

- User authentication (login/register)
- Instagram-style post feed
- Image and text posts
- Comments and likes
- User profiles
- Moderation alerts (warnings/suspensions)
- Admin dashboard

## Getting Started

### Install Dependencies

```bash
cd frontend-react
npm install
```

### Start Development Server

```bash
npm start
```

The app will run on http://localhost:3000

### Backend Requirement

Make sure the Flask backend is running on http://localhost:5000

## Project Structure

```
frontend-react/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── auth/
│   │   ├── posts/
│   │   ├── profile/
│   │   ├── moderation/
│   │   └── admin/
│   ├── services/
│   ├── App.js
│   └── index.js
└── package.json
```

## Technologies

- React 18
- Material-UI
- React Router
- Axios
