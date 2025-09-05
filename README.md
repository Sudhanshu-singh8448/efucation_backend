# Unified Education Backend - NoSQL Version

A comprehensive education platform backend built with Flask and MongoDB, providing career guidance, college finding, course suggestions, news recommendations, and scholarship services.

## 🚀 Features

### Core Services
- **Career Guidance**: RIASEC personality assessment with 24 questions and career recommendations
- **College Finder**: Search and filter colleges with advanced criteria
- **Course Suggestions**: RIASEC-based course recommendations with location preferences
- **News Recommender**: Personalized news recommendations based on career interests
- **Scholarship Service**: Smart scholarship matching using personality traits and eligibility

### Technical Features
- MongoDB Atlas cloud database integration
- RESTful API design with comprehensive endpoints
- RIASEC (Holland Code) personality assessment system
- Geographic distance calculations for location-based recommendations
- Comprehensive error handling and logging
- CORS enabled for cross-origin requests

## 📋 API Endpoints

### Health & General
- `GET /` - Root endpoint with service information
- `GET /api/health` - Global health check
- `GET /api/services` - List all available services and endpoints

### Career Guidance (`/api/career`)
- `GET /health` - Service health check
- `POST /start-assessment` - Start RIASEC assessment
- `POST /submit-answers` - Submit assessment answers
- `GET /recommendations/<session_id>` - Get career recommendations

### College Finder (`/api/college`)
- `GET /health` - Service health check
- `GET /search` - Search colleges by name or keyword
- `POST /filter` - Filter colleges by multiple criteria
- `GET /statistics` - Get college statistics

### Course Suggestions (`/api/course`)
- `GET /health` - Service health check
- `POST /recommend` - Get course recommendations based on RIASEC scores
- `GET /search` - Search courses by keyword

### News Recommender (`/api/news`)
- `GET /health` - Service health check
- `POST /recommend` - Get news recommendations
- `GET /news-by-type/<riasec_type>` - Get news by RIASEC type
- `GET /articles/search` - Search news articles
- `GET /articles` - Get all articles
- `GET /categories` - Get news categories

### Scholarship (`/api/scholarship`)
- `GET /health` - Service health check
- `POST /recommend` - Get scholarship recommendations
- `GET /search` - Search scholarships
- `GET /all` - Get all scholarships
- `GET /by-riasec/<riasec_type>` - Get scholarships by RIASEC type
- `GET /fields` - Get scholarship fields and statistics

## � Deployment

### Deploy to Render (Recommended)

1. **Quick Deploy**:
   - Push code to GitHub
   - Connect repository to Render
   - Set MongoDB URI in environment variables
   - Deploy with one click!

2. **Detailed Guide**: See [RENDER_DEPLOY.md](RENDER_DEPLOY.md) for step-by-step instructions

3. **Environment Variables**:
   ```
   MONGODB_URI = mongodb+srv://username:password@cluster.mongodb.net/
   DATABASE_NAME = education_platform
   FLASK_ENV = production
   PORT = 10000
   ```

4. **Test Deployment**:
   ```bash
   python test_deployment.py https://your-app.onrender.com
   ```

### Alternative Deployments

- **Docker**: Use included `Dockerfile`
- **Heroku**: Use `Procfile` and `runtime.txt`
- **Railway**: Compatible with existing configuration
- **DigitalOcean**: Use Docker deployment

## �🛠 Installation & Setup

### Prerequisites
- Python 3.8+
- MongoDB Atlas account
- Git

### 1. Clone and Navigate
```bash
cd nosql_backend
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file with your MongoDB connection:
```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
DATABASE_NAME=education_platform
SECRET_KEY=your-secret-key-here
FLASK_DEBUG=False
HOST=0.0.0.0
PORT=5000
```

### 4. Data Migration
Run the migration script to populate MongoDB:
```bash
python migrate_data.py
```

### 5. Start the Server
```bash
python app.py
```

The server will start on `http://localhost:5000`

## 🧪 Testing

Run the comprehensive test suite:
```bash
python test_api.py
```

This will test all endpoints and provide a detailed report.

## 📊 Database Schema

### Collections
- `career_sessions` - RIASEC assessment sessions
- `colleges` - College information and details
- `courses` - Course data with college associations
- `news_articles` - News articles with RIASEC categorization
- `scholarships` - Scholarship information and criteria

### Sample Documents

#### Career Session
```json
{
    "session_id": "uuid",
    "user_id": "user123",
    "questions": [...],
    "answers": [1, 5, 3, ...],
    "riasec_scores": {"R": 4.2, "I": 3.8, ...},
    "career_recommendations": [...],
    "created_at": "datetime",
    "completed": true
}
```

#### College
```json
{
    "college_name": "IIT Bombay",
    "state": "Maharashtra",
    "course_type": "Engineering",
    "fees": 200000,
    "rating": 4.5,
    "location": "Mumbai",
    "created_at": "datetime"
}
```

## 🎯 RIASEC Assessment System

The system uses the Holland Code (RIASEC) personality assessment:

- **R** (Realistic) - Practical, hands-on, mechanical
- **I** (Investigative) - Scientific, analytical, research
- **A** (Artistic) - Creative, expressive, artistic
- **S** (Social) - Helping others, teaching, counseling
- **E** (Enterprising) - Leadership, business, entrepreneurial
- **C** (Conventional) - Organized, detail-oriented, systematic

### Assessment Flow
1. User starts assessment → receives 24 questions
2. Submits answers (1-5 scale) → calculates RIASEC scores
3. Gets personalized recommendations based on dominant types

## 🔧 Architecture

```
nosql_backend/
├── app.py                 # Main Flask application
├── database.py           # MongoDB connection and utilities
├── migrate_data.py       # Data migration script
├── test_api.py          # Comprehensive API tests
├── requirements.txt     # Python dependencies
├── .env                 # Environment configuration
└── services/
    ├── career_guidance.py    # RIASEC assessment service
    ├── college_finder.py     # College search and filter
    ├── course_suggestion.py  # Course recommendations
    ├── news_recommender.py   # News recommendation engine
    └── scholarship.py        # Scholarship matching service
```

## 🚦 Error Handling

The API provides consistent error responses:

```json
{
    "success": false,
    "error": "Error type",
    "message": "Detailed error message",
    "details": "Additional context (in development)"
}
```

## 📝 Logging

All services include comprehensive logging:
- Request/response logging
- Error tracking
- Performance monitoring
- Database operation logs

Logs are written to both console and `app.log` file.

## 🔒 Security Features

- Environment-based configuration
- Input validation and sanitization
- MongoDB injection prevention
- CORS configuration
- Error message sanitization

## 📈 Performance Optimization

- Database indexing on frequently queried fields
- Efficient MongoDB aggregation pipelines
- Pagination support for large datasets
- Connection pooling for database operations

## 🤝 Contributing

1. Follow PEP 8 style guidelines
2. Add comprehensive tests for new features
3. Update documentation for API changes
4. Ensure all tests pass before submitting

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For issues and questions:
1. Check the comprehensive test results
2. Review the API documentation above
3. Check database connection and data migration
4. Verify environment configuration

## 🎉 Quick Start Example

```python
import requests

# Start a career assessment
response = requests.post('http://localhost:5000/api/career/start-assessment', 
                        json={'user_id': 'test_user'})
session_data = response.json()

# Submit answers (24 questions, 1-5 scale)
answers = [3, 4, 2, 5, 1, ...] # 24 answers
requests.post('http://localhost:5000/api/career/submit-answers',
              json={'session_id': session_data['session_id'], 'answers': answers})

# Get recommendations
recommendations = requests.get(f"http://localhost:5000/api/career/recommendations/{session_data['session_id']}")
print(recommendations.json())
```

---

**Ready to revolutionize education with personalized recommendations! 🎓✨**
