# Education Platform Unified Backend

## Project Overview
A unified backend server for an Education Platform that consolidates multiple microservices into a single deployable application. The platform provides career guidance, college finder, course suggestions, news recommendations, and scholarship services.

## 🏗️ Architecture
- **Framework**: Flask with Blueprints
- **Database**: PostgreSQL (Neon Cloud)
- **Deployment**: Render.com
- **Environment**: Python 3.13+ with virtual environment
- **Security**: Environment variables for sensitive data

## 📋 Services

### 1. Career Guidance API (`/api/career`)
- **RIASEC Personality Assessment**: 24-question career assessment
- **Database Integration**: PostgreSQL for persistent session storage
- **Features**:
  - Start test sessions with unique session IDs
  - Retrieve questions sequentially
  - Submit answers with 1-5 scale scoring
  - Calculate RIASEC personality type scores
  - Generate career recommendations

### 2. College Finder API (`/api/college`)
- College search and recommendation system
- Filter by location, course, fees, etc.

### 3. Course Suggestion API (`/api/course`)
- Course recommendations based on user preferences
- Academic pathway suggestions

### 4. News Recommender API (`/api/news`)
- Educational news and updates
- Personalized content delivery

### 5. Scholarship API (`/api/scholarship`)
- Scholarship search and matching
- Eligibility criteria checking

## 🗄️ Database Schema

### Career Sessions Table (`career_sessions`)
```sql
- id: VARCHAR (Primary Key) - Session UUID
- created_at: TIMESTAMP - Session creation time
- completed: INTEGER - 0=incomplete, 1=complete
- current_question: INTEGER - Current question number
- realistic_score: INTEGER - Realistic personality score
- investigative_score: INTEGER - Investigative personality score
- artistic_score: INTEGER - Artistic personality score
- social_score: INTEGER - Social personality score
- enterprising_score: INTEGER - Enterprising personality score
- conventional_score: INTEGER - Conventional personality score
```

### Career Answers Table (`career_answers`)
```sql
- id: INTEGER (Primary Key) - Auto-increment ID
- session_id: VARCHAR - Foreign key to career_sessions
- question_number: INTEGER - Question sequence number
- question_text: TEXT - Full question text
- riasec_type: VARCHAR - Personality type category
- answer_value: INTEGER - User's answer (1-5 scale)
- created_at: TIMESTAMP - Answer submission time
```

## 🚀 Setup Instructions

### 1. Environment Setup
```bash
# Clone and navigate to project
cd /Users/sudhanshukumar/project/backend/unified_backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Configuration
Create a `.env` file with your Neon PostgreSQL connection:
```bash
DATABASE_URL=postgresql://username:password@hostname/database?sslmode=require
```

### 3. Database Setup
```bash
# Load environment variables
export $(grep -v '^#' .env | xargs)

# Create database tables
python3 -c "from database import create_tables; create_tables()"
```

### 4. Run the Server
```bash
# Development mode
export $(grep -v '^#' .env | xargs)
python3 app.py

# Or use the startup script
chmod +x start_server.sh
./start_server.sh
```

## 📡 API Endpoints

### Global Endpoints
- `GET /` - API information and service list
- `GET /health` - Global health check

### Career Guidance Endpoints
- `GET /api/career/health` - Service health check
- `POST /api/career/start-test` - Start new assessment session
- `GET /api/career/question/<session_id>` - Get current question
- `POST /api/career/answer` - Submit answer for current question
- `GET /api/career/results/<session_id>` - Get final results

### Example API Usage
```bash
# Start a test session
curl -X POST "http://localhost:8080/api/career/start-test" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user_123"}'

# Get first question
curl "http://localhost:8080/api/career/question/<session_id>"

# Submit answer
curl -X POST "http://localhost:8080/api/career/answer" \
  -H "Content-Type: application/json" \
  -d '{"session_id": "<session_id>", "answer": 4}'
```

## 🔧 Project Structure
```
unified_backend/
├── app.py                  # Main Flask application
├── database.py             # Database models and connection
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (not in git)
├── .env.example           # Environment template
├── start_server.sh        # Server startup script
├── render.yaml            # Render deployment config
├── services/              # Service modules
│   ├── career_guidance.py # Career assessment service
│   ├── college_finder.py  # College search service
│   ├── course_suggestion.py
│   ├── news_recommender.py
│   └── scholarship.py
├── data/                  # Data files
│   ├── college_list.csv
│   ├── courseAndCollegedata.csv
│   ├── news_data.csv
│   └── scholarship.json
└── venv/                  # Virtual environment
```

## 🛡️ Security Features
- ✅ Environment variables for sensitive data
- ✅ Database credentials not hardcoded
- ✅ `.gitignore` excludes sensitive files
- ✅ Secure SSL connections to database
- ✅ Input validation for API requests

## 🚀 Deployment (Render.com)
The application is configured for deployment on Render.com:

1. **Environment Variables**: Set `DATABASE_URL` in Render dashboard
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `python app.py`
4. **Port**: Automatically detected from `PORT` environment variable

## 🔍 Testing
- `quick_test.py` - Simple API testing script
- `test_career_apis.py` - Comprehensive career API tests
- `test_database_integration.py` - Database functionality tests

## 📊 RIASEC Assessment
The career guidance system uses the RIASEC model:
- **R**ealistic - Hands-on, practical work
- **I**nvestigative - Research, analysis, problem-solving
- **A**rtistic - Creative, expressive activities
- **S**ocial - Helping, teaching, working with people
- **E**nterprising - Leading, persuading, business
- **C**onventional - Organized, detail-oriented work

## 🤝 Contributing
1. Follow Python PEP 8 style guidelines
2. Add environment variables to `.env.example`
3. Update this README for new features
4. Test all endpoints before deployment

## 📝 Notes
- Uses Flask development server (switch to Gunicorn for production)
- Database tables are created automatically on first run
- Session IDs are UUID4 format for uniqueness
- All timestamps are in UTC
- CORS enabled for frontend integration
