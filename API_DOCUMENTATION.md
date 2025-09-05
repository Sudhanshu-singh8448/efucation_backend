# Education Platform - Unified Backend API Documentation

## 🚀 Server Information

- **Base URL**: `http://localhost:8080`
- **API Version**: v1.0.0
- **Content-Type**: `application/json`
- **CORS**: Enabled for all origins

## 📋 Quick Start

```bash
# Start the server
cd /Users/sudhanshukumar/project/backend/unified_backend
./venv/bin/python3 app.py

# Server will be available at: http://localhost:8080
```

## 🏥 Health Check Endpoints

### Main Health Check
```http
GET /health
```

**Response:**
```json
{
  "message": "All services are operational",
  "status": "healthy",
  "services": {
    "career_guidance": "healthy",
    "college_finder": "healthy", 
    "course_suggestion": "healthy",
    "news_recommender": "healthy",
    "scholarship": "healthy"
  }
}
```

### Individual Service Health Checks
```http
GET /api/career/health
GET /api/college/health
GET /api/course/health
GET /api/news/health
GET /api/scholarship/health
```

---

## 🎯 1. Career Guidance API (`/api/career/`)

### Overview
RIASEC personality-based career recommendation service using Holland's 6-factor model (Realistic, Investigative, Artistic, Social, Enterprising, Conventional).

### 1.1 Start Assessment
```http
POST /api/career/start-test
```

**Request Body:** None required

**Response:**
```json
{
  "success": true,
  "session_id": "d56f02a3-6032-4049-b4f9-f903a7d6c30b",
  "message": "Test session started successfully",
  "total_questions": 24
}
```

### 1.2 Get Question
```http
GET /api/career/question/{session_id}
```

**Path Parameters:**
- `session_id`: UUID from start-test response

**Response:**
```json
{
  "success": true,
  "session_id": "d56f02a3-6032-4049-b4f9-f903a7d6c30b",
  "question_number": 1,
  "question": "I enjoy working with my hands to build or repair things.",
  "riasec_type": "Realistic",
  "progress": 0.0,
  "total_questions": 24
}
```

### 1.3 Submit Answer
```http
POST /api/career/answer
```

**Request Body:**
```json
{
  "session_id": "d56f02a3-6032-4049-b4f9-f903a7d6c30b",
  "answer": 4
}
```

**Input Validation:**
- `session_id`: Required, valid UUID
- `answer`: Required, integer 1-5 (1=Strongly Disagree, 5=Strongly Agree)

**Response:**
```json
{
  "success": true,
  "session_id": "d56f02a3-6032-4049-b4f9-f903a7d6c30b",
  "message": "Answer recorded successfully",
  "completed": false,
  "progress": 4.166666666666666,
  "next_question": 2
}
```

### 1.4 Get Results
```http
GET /api/career/results/{session_id}
```

**Path Parameters:**
- `session_id`: UUID from completed assessment

**Response:**
```json
{
  "success": true,
  "session_id": "d56f02a3-6032-4049-b4f9-f903a7d6c30b",
  "personality_profile": {
    "R": 85,
    "I": 72,
    "A": 45,
    "S": 60,
    "E": 55,
    "C": 70
  },
  "primary_type": "R",
  "secondary_type": "I", 
  "career_recommendations": [
    {
      "career": "Mechanical Engineer",
      "fit_score": 95,
      "description": "Design and develop mechanical systems",
      "education_required": "Bachelor's Degree",
      "salary_range": "₹4-12 LPA",
      "growth_outlook": "Excellent"
    }
  ],
  "personality_description": {
    "primary": "Realistic - You prefer hands-on, practical work...",
    "secondary": "Investigative - You enjoy analyzing and solving problems..."
  }
}
```

### 1.5 Delete Session
```http
DELETE /api/career/session/{session_id}
```

**Response:**
```json
{
  "success": true,
  "message": "Session deleted successfully"
}
```

---

## 🏛️ 2. College Finder API (`/api/college/`)

### Overview
Search and filter colleges from Jammu & Kashmir with 137 institutions across multiple categories.

### 2.1 Get All Colleges
```http
GET /api/college/colleges
```

**Response:**
```json
{
  "total": 137,
  "colleges": [
    {
      "College_ID": "J-GDC-01",
      "College_Name": "GGM Science College",
      "College_Type": "Degree College",
      "Division": "Jammu",
      "District": "Jammu",
      "Location_City": "Jammu",
      "Estd_Year": 1905,
      "Affiliating_University": "Cluster University of Jammu",
      "Key_Degrees_Offered": "BSc, BCA, MA English, M.Sc Geology",
      "Review_Score_5": 3.8,
      "Estimated_Annual_Fee_INR": "10,000 - 12,500",
      "Website": "www.ggmsciencecollege.in",
      "Contact_Info": "0191-2953033",
      "Address": "Canal Road, Jammu-Tawi(J&K) 180001"
    }
  ]
}
```

### 2.2 Filter Colleges
```http
POST /api/college/colleges/filter
```

**Request Body:**
```json
{
  "Division": "Jammu",
  "College_Type": "Degree College",
  "District": "Jammu",
  "Affiliating_University": "University of Jammu"
}
```

**Available Filter Fields:**
- `College_Name`: String
- `College_Type`: "Degree College", "Engineering", "Medical", "Polytechnic"
- `Division`: "Jammu", "Kashmir"
- `District`: Any J&K district name
- `Location_City`: City name
- `Affiliating_University`: University name
- `Estd_Year`: Establishment year
- `Review_Score_5`: Rating 1-5

**Response:**
```json
{
  "total": 25,
  "filters_applied": {
    "Division": "Jammu",
    "College_Type": "Degree College"
  },
  "colleges": [
    {
      "College_ID": "J-GDC-01",
      "College_Name": "GGM Science College",
      ...
    }
  ]
}
```

### 2.3 Search Colleges
```http
GET /api/college/colleges/search?q={search_term}
```

**Query Parameters:**
- `q`: Search term (searches in college names)

**Example:**
```http
GET /api/college/colleges/search?q=Science
```

**Response:**
```json
{
  "total": 5,
  "search_term": "Science",
  "colleges": [
    {
      "College_ID": "J-GDC-01",
      "College_Name": "GGM Science College",
      ...
    }
  ]
}
```

### 2.4 Get College Statistics
```http
GET /api/college/colleges/stats
```

**Response:**
```json
{
  "total_colleges": 137,
  "colleges_by_division": {
    "Jammu": 75,
    "Kashmir": 60
  },
  "colleges_by_type": {
    "Degree College": 95,
    "Engineering": 9,
    "Medical": 11,
    "Polytechnic": 20
  },
  "colleges_by_district": {
    "Jammu": 21,
    "Srinagar": 11,
    "Anantnag": 11,
    ...
  }
}
```

### 2.5 Get Available Fields
```http
GET /api/college/colleges/fields
```

**Response:**
```json
{
  "fields": {
    "College_Type": ["Degree College", "Engineering", "Medical", "Polytechnic"],
    "Division": ["Jammu", "Kashmir"],
    "District": ["Jammu", "Srinagar", "Anantnag", ...],
    "Affiliating_University": ["University of Jammu", "University of Kashmir", ...]
  }
}
```

---

## 🎓 3. Course Suggestion API (`/api/course/`)

### Overview
AI-powered course recommendations using 3-layer filtering: Location-based, RIASEC personality matching, and multi-factor ranking.

### 3.1 Get Course Recommendations
```http
POST /api/course/recommend
```

**Request Body:**
```json
{
  "user_latitude": 34.0837,
  "user_longitude": 74.7973,
  "user_gender": "Male",
  "education_level": "12th",
  "riasec_profile": {
    "R": 8,
    "I": 7,
    "A": 2,
    "S": 3,
    "E": 5,
    "C": 6
  },
  "radius_km": 100.0,
  "max_results": 10
}
```

**Input Validation:**
- `user_latitude`: Required, float (-90 to 90)
- `user_longitude`: Required, float (-180 to 180)
- `user_gender`: Required, "Male" | "Female" | "Other"
- `education_level`: Required, "10th" | "12th" | "Diploma" | "UG" | "PG"
- `riasec_profile`: Required, object with R,I,A,S,E,C scores (1-10)
- `radius_km`: Optional, float (default: 50.0)
- `max_results`: Optional, integer (default: 20)

**Response:**
```json
{
  "total_results": 3,
  "recommendations": [
    {
      "college_name": "NIT Srinagar",
      "course_name": "B.Tech Mechanical Engineering",
      "degree_level": "UG",
      "distance_km": 5.24,
      "match_score": 19.0,
      "match_percent": "95.0% Match with your personality",
      "riasec_trait": "R",
      "college_rating": 4.6,
      "course_rating": 4.6,
      "final_rank": 0.951,
      "potential_careers": "Mechanic, Mechanical Engineer, Robotics Engineer"
    }
  ],
  "user_input": {
    "location": [34.0837, 74.7973],
    "education_level": "12th",
    "riasec_profile": {
      "R": 8, "I": 7, "A": 2, "S": 3, "E": 5, "C": 6
    },
    "radius_km": 100.0
  },
  "algorithm_info": {
    "approach": "3-Layer Filtering (Knowledge-Based + Content-Based + Learning-to-Rank)",
    "layer1_filtered": 17,
    "weights": {
      "personality_match": 0.6,
      "course_rating": 0.25,
      "college_rating": 0.15
    }
  }
}
```

### 3.2 Get Dataset Information
```http
GET /api/course/dataset-info
```

**Response:**
```json
{
  "total_courses": 37,
  "colleges": 16,
  "degree_levels": {
    "UG": 34,
    "PG": 3
  },
  "riasec_traits": {
    "I": 15,
    "A": 6,
    "S": 5,
    "R": 5,
    "E": 3,
    "C": 3
  },
  "sample_courses": [
    "B.Tech Mechanical Engineering",
    "MBBS",
    "B.Sc Agriculture",
    "BBA",
    "LLB"
  ]
}
```

---

## 📰 4. News Recommender API (`/api/news/`)

### Overview
RIASEC personality-based news article recommendations with 35 articles across 6 personality types.

### 4.1 Get News Recommendations
```http
POST /api/news/recommend
```

**Request Body:**
```json
{
  "riasec_types": "IE",
  "num_recommendations": 5
}
```

**Input Validation:**
- `riasec_types`: Required, string containing any combination of R,I,A,S,E,C
- `num_recommendations`: Optional, integer (default: 5)

**Response:**
```json
{
  "riasec_input": "IE",
  "num_recommendations": 3,
  "recommendations": [
    {
      "news_id": "JK-05",
      "headline": "NIT Srinagar Secures Twin Research Grants for Renewable Energy Technologies",
      "description": "The National Institute of Technology (NIT) Srinagar has been awarded two significant research project grants...",
      "riasec_type": "I",
      "riasec_description": "Investigative - Scientific, analytical, research-oriented"
    },
    {
      "news_id": "JK-06", 
      "headline": "J&K Government Formulates New Private University Policy for 2025",
      "description": "Jammu and Kashmir's administration is developing the J&K Private University Policy-2025...",
      "riasec_type": "E",
      "riasec_description": "Enterprising - Leadership, business, entrepreneurial"
    }
  ]
}
```

### 4.2 Get News by RIASEC Type
```http
GET /api/news/news-by-type/{riasec_type}
```

**Path Parameters:**
- `riasec_type`: Single character R,I,A,S,E, or C

**Example:**
```http
GET /api/news/news-by-type/I
```

**Response:**
```json
{
  "riasec_type": "I",
  "riasec_description": "Investigative - Scientific, analytical, research-oriented",
  "total_articles": 10,
  "articles": [
    {
      "news_id": "JK-05",
      "headline": "NIT Srinagar Secures Twin Research Grants for Renewable Energy Technologies",
      "description": "The National Institute of Technology...",
      "riasec_type": "I"
    }
  ]
}
```

### 4.3 Get RIASEC Types
```http
GET /api/news/riasec-types
```

**Response:**
```json
{
  "riasec_types": {
    "R": "Realistic - Practical, hands-on, mechanical interests",
    "I": "Investigative - Scientific, analytical, research-oriented", 
    "A": "Artistic - Creative, expressive, artistic pursuits",
    "S": "Social - Helping others, teaching, counseling",
    "E": "Enterprising - Leadership, business, entrepreneurial",
    "C": "Conventional - Organized, detail-oriented, systematic"
  }
}
```

### 4.4 Get News Statistics
```http
GET /api/news/stats
```

**Response:**
```json
{
  "total_articles": 35,
  "articles_by_riasec": {
    "I": 10,
    "C": 8,
    "E": 5,
    "S": 5,
    "R": 4,
    "A": 3
  },
  "riasec_descriptions": {
    "R": "Realistic - Practical, hands-on, mechanical interests",
    "I": "Investigative - Scientific, analytical, research-oriented",
    ...
  }
}
```

---

## 🎓 5. Scholarship API (`/api/scholarship/`)

### Overview
Scholarship matching service based on eligibility criteria with 22 scholarship programs.

### 5.1 Match Scholarships
```http
POST /api/scholarship/match
```

**Request Body:**
```json
{
  "gender": "Female",
  "age": 20,
  "education_level": "Undergraduate",
  "domicile": "Jammu & Kashmir",
  "annual_income": 300000,
  "social_category": "General",
  "course_stream": "Engineering",
  "percentage": 85.0
}
```

**Input Validation:**
- `gender`: Required, "Male" | "Female" | "Other"
- `age`: Required, integer (1-100)
- `education_level`: Required, "Pre-Matric (Class 1-10)" | "Undergraduate" | "Postgraduate"
- `domicile`: Required, string (e.g., "Jammu & Kashmir")
- `annual_income`: Optional, number
- `social_category`: Optional, "General" | "OBC" | "SC" | "ST" | "Minority"
- `course_stream`: Optional, "Engineering" | "Medical" | "General"
- `percentage`: Optional, number (0-100)

**Response:**
```json
{
  "success": true,
  "user_profile": {
    "gender": "Female",
    "age": 20,
    "education_level": "Undergraduate",
    "domicile": "Jammu & Kashmir",
    "annual_income": 300000,
    "social_category": "General",
    "course_stream": "Engineering",
    "percentage": 85.0
  },
  "total_scholarships": 22,
  "eligible_count": 12,
  "ineligible_count": 10,
  "eligible_scholarships": [
    {
      "scholarship_id": "KEI-001",
      "scholarship_name": "Kashmir Education Initiative Scholarship",
      "provider_name": "Kashmir Education Initiative",
      "provider_type": "Private",
      "description": "Scholarships for students from Kashmir province...",
      "score": 85,
      "match_percentage": 85,
      "benefits": {
        "academic_fee_coverage": "Financial support provided",
        "maintenance_allowance": "Financial support provided",
        "total_value_description": "Financial support and mentorship"
      },
      "application_timeline": {
        "application_start_date": "2022-11-01",
        "application_end_date": "2022-12-10"
      },
      "application_portal_url": "https://keikashmir.org/",
      "eligibility_met": [
        "Domicile: Jammu & Kashmir ✓",
        "Education Level: Undergraduate ✓",
        "Course Stream: Engineering ✓",
        "Income: Under ₹3,00,000 ✓"
      ]
    }
  ],
  "recommendations": {
    "high_match": [
      {
        "scholarship_id": "KEI-001",
        "scholarship_name": "Kashmir Education Initiative Scholarship",
        "score": 85,
        "reason": "Perfect match for your profile"
      }
    ],
    "medium_match": [],
    "low_match": []
  }
}
```

### 5.2 Get All Scholarships
```http
GET /api/scholarship/scholarships
```

**Response:**
```json
{
  "success": true,
  "total_scholarships": 22,
  "scholarships": [
    {
      "scholarship_id": "KEI-001",
      "scholarship_name": "Kashmir Education Initiative Scholarship",
      "provider_name": "Kashmir Education Initiative",
      "provider_type": "Private",
      "description": "Scholarships for students from Kashmir province...",
      "eligibility_criteria": {
        "domicile": ["Jammu & Kashmir"],
        "gender": "All",
        "min_age": null,
        "max_age": 25,
        "income_ceiling_pa": 300000,
        "social_category": ["General", "OBC"],
        "education_level": ["Undergraduate"],
        "course_stream": ["Engineering"],
        "academic_requirements": {
          "min_percentage": 60.0,
          "competitive_exam": null
        }
      },
      "benefits": {
        "academic_fee_coverage": "Financial support provided",
        "maintenance_allowance": "Financial support provided", 
        "total_value_description": "Financial support and mentorship"
      },
      "application_timeline": {
        "application_start_date": "2022-11-01",
        "application_end_date": "2022-12-10"
      },
      "application_portal_url": "https://keikashmir.org/"
    }
  ]
}
```

### 5.3 Get Specific Scholarship
```http
GET /api/scholarship/scholarships/{scholarship_id}
```

**Path Parameters:**
- `scholarship_id`: Unique scholarship identifier

**Response:**
```json
{
  "success": true,
  "scholarship": {
    "scholarship_id": "KEI-001",
    "scholarship_name": "Kashmir Education Initiative Scholarship",
    "provider_name": "Kashmir Education Initiative",
    ...
  }
}
```

---

## 🔧 Error Handling

### Standard Error Response
```json
{
  "success": false,
  "error": "Error description",
  "code": "ERROR_CODE",
  "timestamp": "2025-09-05T11:30:00.000Z"
}
```

### Common HTTP Status Codes
- `200`: Success
- `400`: Bad Request (missing/invalid parameters)
- `404`: Not Found (session/resource not found)
- `500`: Internal Server Error

### Error Examples

**Missing Required Fields:**
```json
{
  "success": false,
  "error": "Missing required fields: gender, age",
  "code": "MISSING_FIELDS"
}
```

**Invalid Session:**
```json
{
  "success": false,
  "error": "Session not found or expired",
  "code": "INVALID_SESSION"
}
```

**Invalid RIASEC Profile:**
```json
{
  "success": false,
  "error": "RIASEC scores must be between 1 and 10",
  "code": "INVALID_RIASEC"
}
```

---

## 🧪 Testing Examples

### Using curl

**Test Career Assessment:**
```bash
# Start test
curl -X POST http://localhost:8080/api/career/start-test

# Get question
curl http://localhost:8080/api/career/question/SESSION_ID

# Submit answer
curl -X POST http://localhost:8080/api/career/answer \
  -H "Content-Type: application/json" \
  -d '{"session_id": "SESSION_ID", "answer": 4}'
```

**Test College Filter:**
```bash
curl -X POST http://localhost:8080/api/college/colleges/filter \
  -H "Content-Type: application/json" \
  -d '{"Division": "Jammu", "College_Type": "Engineering"}'
```

**Test Course Recommendations:**
```bash
curl -X POST http://localhost:8080/api/course/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "user_latitude": 34.0837,
    "user_longitude": 74.7973,
    "education_level": "12th",
    "riasec_profile": {"R": 8, "I": 7, "A": 2, "S": 3, "E": 5, "C": 6}
  }'
```

**Test News Recommendations:**
```bash
curl -X POST http://localhost:8080/api/news/recommend \
  -H "Content-Type: application/json" \
  -d '{"riasec_types": "IE", "num_recommendations": 3}'
```

**Test Scholarship Matching:**
```bash
curl -X POST http://localhost:8080/api/scholarship/match \
  -H "Content-Type: application/json" \
  -d '{
    "gender": "Female",
    "age": 20,
    "education_level": "Undergraduate",
    "domicile": "Jammu & Kashmir"
  }'
```

---

## 📱 Integration Guidelines

### Frontend Integration
1. **Base URL**: Always use the base URL `http://localhost:8080`
2. **Content-Type**: Set `Content-Type: application/json` for POST requests
3. **Error Handling**: Check `success` field in responses
4. **Session Management**: Store session IDs for career assessments
5. **CORS**: API supports cross-origin requests

### Mobile App Integration
- API is mobile-friendly with JSON responses
- All endpoints support standard HTTP methods
- Real-time progress tracking for assessments
- Offline-capable data structures

---

## 🔒 Security & Best Practices

1. **Input Validation**: All inputs are validated server-side
2. **Session Security**: UUIDs used for session management
3. **Rate Limiting**: Consider implementing for production
4. **HTTPS**: Use HTTPS in production environments
5. **Authentication**: Consider adding JWT tokens for user management

---

## 📊 Performance & Scaling

- **Response Time**: < 500ms for typical requests
- **Concurrent Users**: Tested with multiple simultaneous sessions
- **Memory Usage**: Optimized data structures for large datasets
- **Caching**: Implement Redis for session storage in production

---

This documentation provides complete endpoint specifications for integrating with your unified education platform API. Each service maintains its original functionality while providing a consistent, unified interface.
