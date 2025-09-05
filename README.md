# Education Platform - Unified Backend API

A consolidated backend service that combines five educational microservices into a single deployable application for easy deployment on platforms like Render.

## Services Included

### 1. Career Guidance API (`/api/career`)
- **Purpose**: RIASEC personality-based career recommendation
- **Key Endpoints**:
  - `POST /api/career/start-test` - Start career assessment
  - `GET /api/career/question/<session_id>` - Get next question
  - `POST /api/career/answer` - Submit answer
  - `GET /api/career/results/<session_id>` - Get career recommendations

### 2. College Finder API (`/api/college`)
- **Purpose**: Filter and search colleges based on criteria
- **Key Endpoints**:
  - `GET /api/college/colleges` - Get all colleges
  - `POST /api/college/colleges/filter` - Filter colleges
  - `GET /api/college/colleges/search` - Search colleges by name
  - `GET /api/college/colleges/stats` - Get college statistics

### 3. Course Suggestion API (`/api/course`)
- **Purpose**: AI-powered course recommendations using 3-layer filtering
- **Key Endpoints**:
  - `POST /api/course/recommend` - Get personalized course recommendations
  - `GET /api/course/dataset-info` - Get dataset information

### 4. News Recommender API (`/api/news`)
- **Purpose**: RIASEC-based news recommendations
- **Key Endpoints**:
  - `POST /api/news/recommend` - Get news recommendations
  - `GET /api/news/riasec-types` - Get RIASEC type descriptions
  - `GET /api/news/stats` - Get news dataset statistics

### 5. Scholarship API (`/api/scholarship`)
- **Purpose**: Match scholarships based on user eligibility
- **Key Endpoints**:
  - `POST /api/scholarship/match` - Match scholarships for user
  - `GET /api/scholarship/scholarships` - Get all scholarships
  - `GET /api/scholarship/scholarships/<id>` - Get specific scholarship

## Quick Start

### Local Development

1. **Clone and Setup**:
   ```bash
   cd unified_backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python app.py
   ```

3. **Access the API**:
   - Main API: http://localhost:5000
   - Health Check: http://localhost:5000/health
   - API Documentation: http://localhost:5000

### Production Deployment

#### Deploy to Render

1. **Create a new Web Service on Render**
2. **Connect your GitHub repository**
3. **Use these settings**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 app:app`
   - **Environment**: Python 3

#### Deploy with Docker

1. **Build the image**:
   ```bash
   docker build -t education-platform-api .
   ```

2. **Run the container**:
   ```bash
   docker run -p 5000:5000 education-platform-api
   ```

## API Usage Examples

### Career Guidance Example
```bash
# Start a test session
curl -X POST http://localhost:5000/api/career/start-test

# Get a question
curl http://localhost:5000/api/career/question/<session_id>

# Submit an answer
curl -X POST http://localhost:5000/api/career/answer \
  -H "Content-Type: application/json" \
  -d '{"session_id": "<session_id>", "answer": 4}'
```

### College Filter Example
```bash
# Filter colleges
curl -X POST http://localhost:5000/api/college/colleges/filter \
  -H "Content-Type: application/json" \
  -d '{"Division": "Jammu", "College_Type": "Government"}'
```

### Course Recommendation Example
```bash
# Get course recommendations
curl -X POST http://localhost:5000/api/course/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "user_latitude": 32.7266,
    "user_longitude": 74.8570,
    "education_level": "12th",
    "riasec_profile": {"R": 6, "I": 8, "A": 4, "S": 5, "E": 7, "C": 3},
    "radius_km": 100
  }'
```

### News Recommendation Example
```bash
# Get news recommendations
curl -X POST http://localhost:5000/api/news/recommend \
  -H "Content-Type: application/json" \
  -d '{"riasec_types": "IE", "num_recommendations": 5}'
```

### Scholarship Matching Example
```bash
# Match scholarships
curl -X POST http://localhost:5000/api/scholarship/match \
  -H "Content-Type: application/json" \
  -d '{
    "gender": "Male",
    "age": 20,
    "education_level": "Undergraduate",
    "domicile": "Jammu & Kashmir",
    "annual_income": 400000,
    "social_category": "General",
    "percentage": 85.5
  }'
```

## Project Structure

```
unified_backend/
├── app.py                 # Main Flask application
├── services/             # Service modules (blueprints)
│   ├── career_guidance.py
│   ├── college_finder.py
│   ├── course_suggestion.py
│   ├── news_recommender.py
│   └── scholarship.py
├── data/                 # Data files
│   ├── college_list.csv
│   ├── courseAndCollegedata.csv
│   ├── news_data.csv
│   └── scholarship.json
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
├── render.yaml         # Render deployment config
└── README.md           # This file
```

## Dependencies

- **Flask 3.0.0**: Web framework
- **Flask-CORS**: Cross-origin resource sharing
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **scikit-learn**: Machine learning
- **geopy**: Geographic calculations
- **requests**: HTTP library
- **gunicorn**: Production WSGI server

## Key Features

### ✅ Production Ready
- Gunicorn WSGI server for production
- Health check endpoints
- Error handling and validation
- CORS enabled for frontend integration

### ✅ Deployment Ready
- Docker containerization
- Render.com configuration
- Environment variable support
- Consolidated requirements

### ✅ API Gateway Pattern
- Single entry point for all services
- Consistent API structure
- Centralized error handling
- Service isolation through blueprints

### ✅ Data Management
- All datasets included in project
- Fallback data loading mechanisms
- CSV and JSON data support

## Environment Variables

- `PORT`: Server port (default: 5000)
- `FLASK_ENV`: Environment mode (development/production)
- `PYTHONUNBUFFERED`: Python output buffering

## Health Monitoring

- **Global Health Check**: `GET /health`
- **Individual Service Health**: `GET /api/<service>/health`
- **Service Status**: All endpoints return consistent status information

## Migration from Individual Services

This unified backend maintains **100% API compatibility** with the original individual services. The only change required is updating the base URL and adding the service prefix:

**Original**: `http://localhost:3002/api/start-test`
**Unified**: `http://localhost:5000/api/career/start-test`

## Support

For issues or questions:
1. Check the API documentation at the root endpoint
2. Verify health check endpoints
3. Review logs for detailed error information

## License

This project consolidates multiple educational APIs into a unified deployment-ready backend service.
