# Multi-Language & API-as-a-Service Features

## 🌍 Multi-Language Support

### Overview
The system now automatically detects and processes text in 55+ languages.

### Supported Languages
- **Major Languages:** English, Spanish, French, German, Italian, Portuguese
- **Asian Languages:** Chinese, Japanese, Korean, Hindi, Arabic, Thai
- **European Languages:** Russian, Polish, Dutch, Swedish, Turkish
- **And 40+ more...**

### How It Works

1. **Language Detection**
```python
from backend.models.detector import detector

# Automatically detects language
result = detector.analyze("¡Esto es un mensaje de odio!")

# Returns:
{
    "is_hate_speech": true,
    "confidence": 0.87,
    "language": "es",  # Spanish detected
    "translated": true,
    "original_text": "¡Esto es un mensaje de odio!"
}
```

2. **Translation Pipeline**
- Non-English text is automatically translated to English
- Analyzed using our trained model
- Results include original language metadata

### API Usage

**Endpoint:** `POST /api/analyze`

**Request:**
```json
{
    "text": "Das ist Hassrede",
    "user_id": "user123"
}
```

**Response:**
```json
{
    "success": true,
    "result": {
        "is_hate_speech": true,
        "confidence": 0.92,
        "category": "hate_speech",
        "language": "de",
        "translated": true,
        "original_text": "Das ist Hassrede"
    },
    "action_taken": "block"
}
```

---

## 🔑 API-as-a-Service (SaaS)

### API Key System

The platform now supports API key-based access for external developers.

### Subscription Tiers

| Tier | Monthly Calls | Price | Features |
|------|--------------|-------|----------|
| **Free** | 1,000 | $0 | Basic hate speech detection |
| **Pro** | 50,000 | $29 | Multi-language + Analytics |
| **Enterprise** | Unlimited | Custom | Dedicated support + SLA |

### Getting Started

#### 1. Generate API Key

**Endpoint:** `POST /api/api-keys/generate`

```bash
curl -X POST http://localhost:5000/api/api-keys/generate \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "tier": "free"
  }'
```

**Response:**
```json
{
    "success": true,
    "api_key": "xyz123abc456...",
    "tier": "free",
    "calls_limit": 1000,
    "message": "⚠️ Save this API key! It will not be shown again."
}
```

#### 2. Use API Key

Include the API key in the `X-API-Key` header:

```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{
    "text": "Text to analyze"
  }'
```

#### 3. Check Usage

**Endpoint:** `GET /api/api-keys/usage`

```bash
curl http://localhost:5000/api/api-keys/usage \
  -H "X-API-Key: YOUR_API_KEY"
```

**Response:**
```json
{
    "success": true,
    "tier": "free",
    "calls_used": 247,
    "calls_limit": 1000,
    "calls_remaining": 753,
    "created_at": "2026-02-01T10:00:00",
    "last_used": "2026-02-13T14:30:00"
}
```

---

## 🔗 Social Media Integration

### Webhook Support

The platform provides webhook endpoints for real-time integration with social media platforms.

### Integration Methods

#### Method 1: Direct API Integration

```javascript
// Example: Pre-posting validation
async function validatePost(content) {
    const response = await fetch('https://your-api.com/api/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-API-Key': 'YOUR_API_KEY'
        },
        body: JSON.stringify({ text: content })
    });
    
    const result = await response.json();
    
    if (result.result.is_hate_speech) {
        alert('Content blocked: Contains hate speech');
        return false;
    }
    
    return true;
}
```

#### Method 2: Webhook Integration

**Endpoint:** `POST /api/webhook/analyze`

```bash
curl -X POST http://localhost:5000/api/webhook/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "X-Callback-URL: https://your-platform.com/callback" \
  -d '{
    "text": "Post content",
    "platform": "twitter",
    "post_id": "123456",
    "user_id": "user789"
  }'
```

**Response:**
```json
{
    "success": true,
    "result": {
        "is_hate_speech": false,
        "confidence": 0.95,
        "language": "en"
    },
    "should_block": false,
    "platform": "twitter",
    "post_id": "123456",
    "timestamp": "2026-02-13T15:00:00"
}
```

### Platform-Specific Examples

#### Twitter/X Integration

```python
import tweepy
import requests

# Twitter API setup
client = tweepy.Client(bearer_token="YOUR_TWITTER_TOKEN")

# Stream tweets and analyze
class HateSpeechStream(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        # Analyze tweet
        response = requests.post(
            'http://your-api.com/api/analyze',
            headers={'X-API-Key': 'YOUR_API_KEY'},
            json={'text': tweet.text, 'user_id': str(tweet.author_id)}
        )
        
        result = response.json()
        if result['result']['is_hate_speech']:
            # Report tweet
            client.report_spam(tweet_id=tweet.id)

stream = HateSpeechStream("YOUR_BEARER_TOKEN")
stream.filter(tweet_fields=["author_id"])
```

#### Instagram/Facebook Integration

```python
from facebook import GraphAPI

graph = GraphAPI(access_token="YOUR_FB_TOKEN")

def moderate_comments(post_id):
    comments = graph.get_object(f"{post_id}/comments")
    
    for comment in comments['data']:
        # Analyze comment
        response = requests.post(
            'http://your-api.com/api/analyze',
            headers={'X-API-Key': 'YOUR_API_KEY'},
            json={'text': comment['message']}
        )
        
        if response.json()['result']['is_hate_speech']:
            # Hide comment
            graph.delete_object(comment['id'])
```

#### Reddit Integration

```python
import praw

reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_SECRET",
    user_agent="HateSpeechBot"
)

subreddit = reddit.subreddit("your_subreddit")

for comment in subreddit.stream.comments():
    # Analyze
    response = requests.post(
        'http://your-api.com/api/analyze',
        headers={'X-API-Key': 'YOUR_API_KEY'},
        json={'text': comment.body}
    )
    
    if response.json()['result']['is_hate_speech']:
        comment.mod.remove()
```

---

## 📊 API Documentation

### All Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/analyze` | POST | Optional | Analyze text for hate speech |
| `/api/webhook/analyze` | POST | Required | Webhook for platforms |
| `/api/api-keys/generate` | POST | None | Generate API key |
| `/api/api-keys/usage` | GET | Required | Check usage stats |
| `/api/api-keys/list/<user_id>` | GET | None | List user's keys |

### Response Codes

- `200` - Success
- `201` - Created (API key)
- `400` - Bad request
- `401` - Unauthorized (invalid/missing API key)
- `429` - Rate limit exceeded
- `500` - Server error

### Rate Limits

- **Free Tier:** 1,000 calls/month
- **Pro Tier:** 50,000 calls/month
- **Enterprise:** No limit

---

## 🚀 Deployment

The API is production-ready and can be deployed as a SaaS service:

**Live API:**
- Development: `http://localhost:5000/api`
- Production: `https://your-domain.onrender.com/api`

**Security:**
- API keys are hashed (SHA-256)
- HTTPS required in production
- CORS enabled
- Rate limiting per tier

---

## 💡 Use Cases

1. **Content Moderation Platform**
   - Real-time comment filtering
   - Pre-posting validation
   - Automated reporting

2. **Social Media Tools**
   - Browser extensions
   - Moderation bots
   - Safety dashboards

3. **Enterprise Solutions**
   - Internal communication tools
   - Customer service platforms
   - Community forums

---

## 📚 SDK Examples

### Python SDK

```python
class HateSpeechAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://your-api.com/api"
    
    def analyze(self, text):
        response = requests.post(
            f"{self.base_url}/analyze",
            headers={'X-API-Key': self.api_key},
            json={'text': text}
        )
        return response.json()

# Usage
api = HateSpeechAPI('your_api_key')
result = api.analyze('Text to check')
print(result['result']['is_hate_speech'])
```

### JavaScript SDK

```javascript
class HateSpeechAPI {
    constructor(apiKey) {
        this.apiKey = apiKey;
        this.baseUrl = 'https://your-api.com/api';
    }
    
    async analyze(text) {
        const response = await fetch(`${this.baseUrl}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-API-Key': this.apiKey
            },
            body: JSON.stringify({ text })
        });
        return await response.json();
    }
}

// Usage
const api = new HateSpeechAPI('your_api_key');
const result = await api.analyze('Text to check');
console.log(result.result.is_hate_speech);
```

---

## 🔧 Configuration

Add to `.env`:

```bash
# Multi-language (optional - auto-fallback if not available)
ENABLE_TRANSLATION=true

# API Keys
API_RATE_LIMIT_FREE=1000
API_RATE_LIMIT_PRO=50000
```

---

## ✅ Testing

Test the new features:

```bash
# Test multi-language
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "C'\''est de la haine"}'

# Test API key
curl -X POST http://localhost:5000/api/api-keys/generate \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "tier": "free"}'

# Test with API key
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_KEY" \
  -d '{"text": "Test message"}'
```

---

**Ready to use!** See [PROJECT_LOGBOOK_ANSWERS.md](PROJECT_LOGBOOK_ANSWERS.md) for detailed implementation notes.
