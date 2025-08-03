# AI Social Media Manager Backend

A comprehensive backend system for an AI agent that creates and manages Facebook content for businesses. The agent simulates the capabilities of a smart social media manager: understands businesses, stays updated on industry trends, and generates lead-oriented posts that can be reviewed, edited, and published automatically.

## 🚀 Features

### Core APIs
1. **Business Understanding API** - Analyzes business websites and extracts structured profiles
2. **Industry News Analyzer API** - Fetches current industry news and insights
3. **Content Generator API** - Creates ready-to-publish Facebook posts
4. **Weekly Planner API** - Schedules posts across the week
5. **Preview & Edit API** - Manages post content before publishing
6. **Facebook Page Connection** - Integrates with Facebook Graph API
7. **Post Publishing** - Publishes content to Facebook pages

### Key Capabilities
- ✅ Website scraping and business profile extraction
- ✅ Industry news analysis and trend identification
- ✅ AI-powered content generation with multiple tones
- ✅ Flexible weekly scheduling system
- ✅ Facebook Graph API integration (with mock mode)
- ✅ Post editing and management
- ✅ Analytics and insights
- ✅ Data persistence and backup

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager
- Facebook Developer Account (for real Facebook integration)

### Quick Start

1. **Clone the repository**
```bash
git clone <repository-url>
cd ai-social-media-manager-backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables (optional)**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Run the application**
```bash
python app.py
```

The server will start at `http://localhost:5000`

### Environment Variables

Create a `.env` file in the root directory:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
FLASK_ENV=development

# Facebook API (for real integration)
FACEBOOK_APP_ID=your-facebook-app-id
FACEBOOK_APP_SECRET=your-facebook-app-secret
FACEBOOK_MOCK_MODE=True

# Data Storage
DATA_DIRECTORY=data

# Rate Limiting
RATELIMIT_ENABLED=False
RATELIMIT_DEFAULT=100 per hour

# Content Settings
DEFAULT_POST_FREQUENCY=3
MAX_POST_FREQUENCY=7

# Website Analysis
WEBSITE_TIMEOUT=10
MAX_WEBSITE_SIZE=5242880

# News Analysis
NEWS_CACHE_HOURS=6
MAX_NEWS_ITEMS=10
```

## 📊 API Documentation

### Base URL
```
http://localhost:5000/api
```

### 1. Business Understanding API

#### Analyze Business Website
```http
POST /api/business/analyze
Content-Type: application/json

{
  "website_url": "https://example-gym.com"
}
```

**Response:**
```json
{
  "success": true,
  "business_id": "uuid-here",
  "profile": {
    "business_name": "FitZone Gym",
    "industry": "fitness",
    "description": "Modern fitness center...",
    "services": ["Personal Training", "Group Classes"],
    "tone_of_voice": "friendly",
    "contact_info": {
      "phone": "555-0123",
      "email": "info@fitzone.com"
    }
  }
}
```

#### Get Business Profile
```http
GET /api/business/{business_id}
```

### 2. Industry News Analyzer API

#### Get Industry News
```http
POST /api/news/analyze
Content-Type: application/json

{
  "industry": "fitness",
  "keywords": ["gym", "workout", "training"]
}
```

**Response:**
```json
{
  "success": true,
  "industry": "fitness",
  "insights": [
    {
      "headline": "HIIT workouts gain popularity...",
      "summary": "Industry analysis shows...",
      "source": "Fitness Magazine",
      "business_insights": ["Consider adding HIIT classes"],
      "content_ideas": ["Post workout video", "Share tips"]
    }
  ]
}
```

### 3. Content Generator API

#### Generate Posts
```http
POST /api/content/generate
Content-Type: application/json

{
  "business_id": "uuid-here",
  "post_preferences": {
    "tone": "friendly",
    "post_type": "promo",
    "frequency": 3
  },
  "industry_news": []
}
```

**Response:**
```json
{
  "success": true,
  "posts": [
    {
      "id": "post-uuid",
      "content": "Hey everyone! 🎉 We've got something special...",
      "hashtags": ["#fitness", "#gym", "#deal"],
      "post_type": "promo",
      "tone": "friendly",
      "call_to_action": "Book now!",
      "best_time_to_post": "6:00 PM"
    }
  ]
}
```

### 4. Weekly Planner API

#### Create Schedule
```http
POST /api/planner/schedule
Content-Type: application/json

{
  "business_id": "uuid-here",
  "frequency": 3,
  "preferred_days": ["monday", "wednesday", "friday"],
  "start_date": "2025-08-04"
}
```

### 5. Preview & Edit API

#### Get Scheduled Posts
```http
GET /api/posts/scheduled/{business_id}
```

#### Update Post
```http
PUT /api/posts/{post_id}
Content-Type: application/json

{
  "content": "Updated post content...",
  "hashtags": ["#updated", "#hashtags"]
}
```

#### Delete Post
```http
DELETE /api/posts/{post_id}
```

### 6. Facebook Integration

#### Connect Facebook Page
```http
POST /api/facebook/connect
Content-Type: application/json

{
  "access_token": "facebook-user-token",
  "page_id": "optional-specific-page-id"
}
```

#### Publish Post
```http
POST /api/posts/{post_id}/publish
Content-Type: application/json

{
  "page_id": "facebook-page-id",
  "access_token": "page-access-token"
}
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python test_complete_system.py


### Manual Testing
```bash
# Test individual components
python business_analyzer.py
python news_analyzer.py
python content_generator.py
python facebook_integration.py
python data_storage.py
```

### API Testing with cURL

#### Test Business Analysis
```bash
curl -X POST http://localhost:5000/api/business/analyze \
  -H "Content-Type: application/json" \
  -d '{"website_url": "https://example.com"}'
```

#### Test Content Generation
```bash
curl -X POST http://localhost:5000/api/content/generate \
  -H "Content-Type: application/json" \
  -d '{
    "business_id": "your-business-id",
    "post_preferences": {
      "tone": "friendly",
      "frequency": 3
    }
  }'
```

## 📁 Project Structure

```
ai-social-media-manager/
├── app.py                      # Main Flask application
├── business_analyzer.py        # Website analysis module
├── news_analyzer.py           # Industry news analysis
├── content_generator.py       # AI content generation
├── facebook_integration.py    # Facebook API integration
├── data_storage.py           # Data persistence layer
├── config.py                 # Configuration management
├── requirements.txt          # Python dependencies
├── README.md                # Project documentation
├── .env.example             # Environment variables template
├── data/                    # Data storage directory
│   ├── business_profiles.json
│   ├── posts.json
│   ├── schedules.json
│   └── facebook_connections.json
├── tests/                   # Test files
├── docs/                    # Additional documentation
└── logs/                    # Application logs
```

## 🔧 Configuration

### Mock Mode vs Real Facebook Integration

**Mock Mode (Default - Safe for testing):**
- Set `FACEBOOK_MOCK_MODE=True`
- No real Facebook API calls
- Simulated responses for testing

**Real Facebook Mode:**
- Set `FACEBOOK_MOCK_MODE=False`
- Requires Facebook App ID and Secret
- Makes actual Facebook API calls

### Facebook App Setup (for real integration)

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app
3. Add Facebook Login and Pages API products
4. Get App ID and App Secret
5. Set up proper permissions: `pages_manage_posts`, `pages_show_list`

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production with Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📈 Features Overview

### Supported Industries
- Fitness (gyms, personal training)
- Beauty (salons, spas)
- Food (restaurants, cafes)
- Retail (shops, boutiques)
- Healthcare (clinics, wellness)
- General business

### Post Types
- **Promotional**: Special offers, deals, discounts
- **Tips**: Industry advice, how-to content
- **Updates**: Business news, announcements
- **Insights**: Industry trends, market analysis

### Tone Options
- **Professional**: Formal, expert-focused
- **Friendly**: Warm, community-oriented
- **Casual**: Relaxed, conversational
- **Premium**: Luxury, sophisticated

## 🔐 Security Features

- CORS protection
- Rate limiting
- Input validation
- Secure token handling
- Data encryption options

## 📊 Analytics & Monitoring

### Built-in Analytics
- Post performance tracking
- Engagement estimates
- Business metrics
- Content type analysis

### Health Check
```http
GET /api/health
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For questions or issues:
1. Check the documentation
2. Review common issues in GitHub Issues
3. Contact: [info@growthzi.com]
