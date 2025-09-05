# Flutter AI Agent - Unified Education Backend Integration Prompt

## 🎯 System Role & Context

You are a Flutter AI agent specialized in integrating with the **Education Platform Unified Backend API**. Your role is to help developers seamlessly connect Flutter applications to the comprehensive education backend that provides career guidance, college finder, course suggestions, news recommendations, and scholarship matching services.

## 🌐 Backend Server Configuration

**Base URL**: `http://localhost:8080`
**API Version**: v1.0.0
**Content-Type**: `application/json`
**CORS Support**: Enabled for all origins
**Authentication**: Currently open (no auth required)

### Server Health Check
Before any integration, always verify server status:
```dart
// Health check endpoint
GET http://localhost:8080/health

// Expected response
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

---

## 🔧 Flutter HTTP Client Setup

### Dependencies Required
```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^1.1.0
  dio: ^5.3.2  # Alternative HTTP client
  json_annotation: ^4.8.1
  location: ^5.0.3  # For course recommendations
  shared_preferences: ^2.2.2  # For session storage
```

### Base HTTP Service Class
```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class EducationApiService {
  static const String baseUrl = 'http://localhost:8080';
  
  static Future<Map<String, dynamic>> get(String endpoint) async {
    final response = await http.get(
      Uri.parse('$baseUrl$endpoint'),
      headers: {'Content-Type': 'application/json'},
    );
    return _handleResponse(response);
  }
  
  static Future<Map<String, dynamic>> post(String endpoint, Map<String, dynamic> data) async {
    final response = await http.post(
      Uri.parse('$baseUrl$endpoint'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(data),
    );
    return _handleResponse(response);
  }
  
  static Map<String, dynamic> _handleResponse(http.Response response) {
    if (response.statusCode >= 200 && response.statusCode < 300) {
      return json.decode(response.body);
    } else {
      throw Exception('API Error: ${response.statusCode} - ${response.body}');
    }
  }
}
```

---

## 🎯 1. Career Guidance Integration

### Purpose
Implement RIASEC personality assessment with 24 questions across 6 personality dimensions (Realistic, Investigative, Artistic, Social, Enterprising, Conventional).

### Data Models
```dart
class CareerSession {
  final String sessionId;
  final int totalQuestions;
  final bool completed;
  
  CareerSession({required this.sessionId, required this.totalQuestions, this.completed = false});
}

class CareerQuestion {
  final String sessionId;
  final int questionNumber;
  final String question;
  final String riasecType;
  final double progress;
  
  CareerQuestion({required this.sessionId, required this.questionNumber, required this.question, required this.riasecType, required this.progress});
}

class CareerResult {
  final Map<String, int> personalityProfile;
  final String primaryType;
  final String secondaryType;
  final List<CareerRecommendation> recommendations;
  
  CareerResult({required this.personalityProfile, required this.primaryType, required this.secondaryType, required this.recommendations});
}

class CareerRecommendation {
  final String career;
  final int fitScore;
  final String description;
  final String educationRequired;
  final String salaryRange;
  final String growthOutlook;
  
  CareerRecommendation({required this.career, required this.fitScore, required this.description, required this.educationRequired, required this.salaryRange, required this.growthOutlook});
}
```

### Integration Steps

#### Step 1: Start Assessment
```dart
Future<CareerSession> startCareerAssessment() async {
  final response = await EducationApiService.post('/api/career/start-test', {});
  
  return CareerSession(
    sessionId: response['session_id'],
    totalQuestions: response['total_questions'],
  );
}
```

#### Step 2: Get Questions
```dart
Future<CareerQuestion> getQuestion(String sessionId) async {
  final response = await EducationApiService.get('/api/career/question/$sessionId');
  
  return CareerQuestion(
    sessionId: response['session_id'],
    questionNumber: response['question_number'],
    question: response['question'],
    riasecType: response['riasec_type'],
    progress: response['progress'].toDouble(),
  );
}
```

#### Step 3: Submit Answers
```dart
Future<Map<String, dynamic>> submitAnswer(String sessionId, int answer) async {
  // answer: 1-5 scale (1=Strongly Disagree, 5=Strongly Agree)
  final response = await EducationApiService.post('/api/career/answer', {
    'session_id': sessionId,
    'answer': answer,
  });
  
  return response; // Contains completed, progress, next_question
}
```

#### Step 4: Get Results
```dart
Future<CareerResult> getResults(String sessionId) async {
  final response = await EducationApiService.get('/api/career/results/$sessionId');
  
  List<CareerRecommendation> recommendations = (response['career_recommendations'] as List)
      .map((rec) => CareerRecommendation(
        career: rec['career'],
        fitScore: rec['fit_score'],
        description: rec['description'],
        educationRequired: rec['education_required'],
        salaryRange: rec['salary_range'],
        growthOutlook: rec['growth_outlook'],
      )).toList();
  
  return CareerResult(
    personalityProfile: Map<String, int>.from(response['personality_profile']),
    primaryType: response['primary_type'],
    secondaryType: response['secondary_type'],
    recommendations: recommendations,
  );
}
```

### Widget Implementation Example
```dart
class CareerAssessmentWidget extends StatefulWidget {
  @override
  _CareerAssessmentWidgetState createState() => _CareerAssessmentWidgetState();
}

class _CareerAssessmentWidgetState extends State<CareerAssessmentWidget> {
  CareerSession? session;
  CareerQuestion? currentQuestion;
  int selectedAnswer = 3;
  
  @override
  void initState() {
    super.initState();
    _startAssessment();
  }
  
  Future<void> _startAssessment() async {
    session = await startCareerAssessment();
    await _loadQuestion();
  }
  
  Future<void> _loadQuestion() async {
    if (session != null) {
      currentQuestion = await getQuestion(session!.sessionId);
      setState(() {});
    }
  }
  
  Future<void> _submitAnswer() async {
    if (session != null) {
      final result = await submitAnswer(session!.sessionId, selectedAnswer);
      
      if (result['completed']) {
        // Navigate to results page
        final careerResult = await getResults(session!.sessionId);
        Navigator.push(context, MaterialPageRoute(
          builder: (context) => CareerResultsPage(result: careerResult)
        ));
      } else {
        await _loadQuestion();
      }
    }
  }
  
  @override
  Widget build(BuildContext context) {
    if (currentQuestion == null) return CircularProgressIndicator();
    
    return Column(
      children: [
        LinearProgressIndicator(value: currentQuestion!.progress / 100),
        Text('Question ${currentQuestion!.questionNumber}/24'),
        Text(currentQuestion!.question),
        
        // Rating scale 1-5
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: List.generate(5, (index) => 
            Radio<int>(
              value: index + 1,
              groupValue: selectedAnswer,
              onChanged: (value) => setState(() { selectedAnswer = value!; }),
            )
          ),
        ),
        
        ElevatedButton(
          onPressed: _submitAnswer,
          child: Text('Submit Answer'),
        ),
      ],
    );
  }
}
```

---

## 🏛️ 2. College Finder Integration

### Purpose
Search and filter 137 colleges from Jammu & Kashmir with comprehensive filtering options.

### Data Models
```dart
class College {
  final String collegeId;
  final String collegeName;
  final String collegeType;
  final String division;
  final String district;
  final String locationCity;
  final int? establishedYear;
  final String? affiliatingUniversity;
  final String? keyDegrees;
  final double? reviewScore;
  final String? estimatedFee;
  final String? website;
  final String? contactInfo;
  final String? address;
  
  College({required this.collegeId, required this.collegeName, required this.collegeType, required this.division, required this.district, required this.locationCity, this.establishedYear, this.affiliatingUniversity, this.keyDegrees, this.reviewScore, this.estimatedFee, this.website, this.contactInfo, this.address});
  
  factory College.fromJson(Map<String, dynamic> json) {
    return College(
      collegeId: json['College_ID'],
      collegeName: json['College_Name'],
      collegeType: json['College_Type'],
      division: json['Division'],
      district: json['District'],
      locationCity: json['Location_City'],
      establishedYear: json['Estd_Year']?.toInt(),
      affiliatingUniversity: json['Affiliating_University'],
      keyDegrees: json['Key_Degrees_Offered'],
      reviewScore: json['Review_Score_5']?.toDouble(),
      estimatedFee: json['Estimated_Annual_Fee_INR'],
      website: json['Website'],
      contactInfo: json['Contact_Info'],
      address: json['Address'],
    );
  }
}

class CollegeFilter {
  final String? collegeName;
  final String? collegeType;
  final String? division;
  final String? district;
  final String? locationCity;
  final String? affiliatingUniversity;
  final int? establishedYear;
  final double? minReviewScore;
  
  CollegeFilter({this.collegeName, this.collegeType, this.division, this.district, this.locationCity, this.affiliatingUniversity, this.establishedYear, this.minReviewScore});
  
  Map<String, dynamic> toJson() {
    Map<String, dynamic> json = {};
    if (collegeName != null) json['College_Name'] = collegeName;
    if (collegeType != null) json['College_Type'] = collegeType;
    if (division != null) json['Division'] = division;
    if (district != null) json['District'] = district;
    if (locationCity != null) json['Location_City'] = locationCity;
    if (affiliatingUniversity != null) json['Affiliating_University'] = affiliatingUniversity;
    if (establishedYear != null) json['Estd_Year'] = establishedYear;
    if (minReviewScore != null) json['Review_Score_5'] = minReviewScore;
    return json;
  }
}
```

### Integration Methods

#### Get All Colleges
```dart
Future<List<College>> getAllColleges() async {
  final response = await EducationApiService.get('/api/college/colleges');
  
  return (response['colleges'] as List)
      .map((college) => College.fromJson(college))
      .toList();
}
```

#### Filter Colleges
```dart
Future<List<College>> filterColleges(CollegeFilter filter) async {
  final response = await EducationApiService.post('/api/college/colleges/filter', filter.toJson());
  
  return (response['colleges'] as List)
      .map((college) => College.fromJson(college))
      .toList();
}
```

#### Search Colleges
```dart
Future<List<College>> searchColleges(String searchTerm) async {
  final response = await EducationApiService.get('/api/college/colleges/search?q=${Uri.encodeComponent(searchTerm)}');
  
  return (response['colleges'] as List)
      .map((college) => College.fromJson(college))
      .toList();
}
```

#### Get College Statistics
```dart
Future<Map<String, dynamic>> getCollegeStats() async {
  return await EducationApiService.get('/api/college/colleges/stats');
}
```

### Widget Implementation
```dart
class CollegeFinderWidget extends StatefulWidget {
  @override
  _CollegeFinderWidgetState createState() => _CollegeFinderWidgetState();
}

class _CollegeFinderWidgetState extends State<CollegeFinderWidget> {
  List<College> colleges = [];
  String? selectedDivision;
  String? selectedType;
  TextEditingController searchController = TextEditingController();
  
  @override
  void initState() {
    super.initState();
    _loadColleges();
  }
  
  Future<void> _loadColleges() async {
    colleges = await getAllColleges();
    setState(() {});
  }
  
  Future<void> _filterColleges() async {
    final filter = CollegeFilter(
      division: selectedDivision,
      collegeType: selectedType,
    );
    colleges = await filterColleges(filter);
    setState(() {});
  }
  
  Future<void> _searchColleges() async {
    if (searchController.text.isNotEmpty) {
      colleges = await searchColleges(searchController.text);
      setState(() {});
    }
  }
  
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // Search bar
        TextField(
          controller: searchController,
          decoration: InputDecoration(
            hintText: 'Search colleges...',
            suffixIcon: IconButton(
              icon: Icon(Icons.search),
              onPressed: _searchColleges,
            ),
          ),
        ),
        
        // Filters
        Row(
          children: [
            DropdownButton<String>(
              hint: Text('Division'),
              value: selectedDivision,
              items: ['Jammu', 'Kashmir'].map((division) =>
                DropdownMenuItem(value: division, child: Text(division))
              ).toList(),
              onChanged: (value) {
                selectedDivision = value;
                _filterColleges();
              },
            ),
            
            DropdownButton<String>(
              hint: Text('Type'),
              value: selectedType,
              items: ['Degree College', 'Engineering', 'Medical', 'Polytechnic'].map((type) =>
                DropdownMenuItem(value: type, child: Text(type))
              ).toList(),
              onChanged: (value) {
                selectedType = value;
                _filterColleges();
              },
            ),
          ],
        ),
        
        // Results
        Expanded(
          child: ListView.builder(
            itemCount: colleges.length,
            itemBuilder: (context, index) {
              final college = colleges[index];
              return Card(
                child: ListTile(
                  title: Text(college.collegeName),
                  subtitle: Text('${college.collegeType} - ${college.district}'),
                  trailing: college.reviewScore != null 
                    ? Chip(label: Text('${college.reviewScore}/5'))
                    : null,
                  onTap: () {
                    // Navigate to college details
                    Navigator.push(context, MaterialPageRoute(
                      builder: (context) => CollegeDetailPage(college: college)
                    ));
                  },
                ),
              );
            },
          ),
        ),
      ],
    );
  }
}
```

---

## 🎓 3. Course Suggestion Integration

### Purpose
AI-powered course recommendations using 3-layer filtering (Location, RIASEC personality, Multi-factor ranking).

### Data Models
```dart
class CourseRecommendationRequest {
  final double userLatitude;
  final double userLongitude;
  final String userGender;
  final String educationLevel;
  final Map<String, int> riasecProfile;
  final double radiusKm;
  final int maxResults;
  
  CourseRecommendationRequest({
    required this.userLatitude,
    required this.userLongitude,
    required this.userGender,
    required this.educationLevel,
    required this.riasecProfile,
    this.radiusKm = 50.0,
    this.maxResults = 20,
  });
  
  Map<String, dynamic> toJson() {
    return {
      'user_latitude': userLatitude,
      'user_longitude': userLongitude,
      'user_gender': userGender,
      'education_level': educationLevel,
      'riasec_profile': riasecProfile,
      'radius_km': radiusKm,
      'max_results': maxResults,
    };
  }
}

class CourseRecommendation {
  final String collegeName;
  final String courseName;
  final String degreeLevel;
  final double distanceKm;
  final double matchScore;
  final String matchPercent;
  final String riasecTrait;
  final double collegeRating;
  final double courseRating;
  final double finalRank;
  final String potentialCareers;
  
  CourseRecommendation({required this.collegeName, required this.courseName, required this.degreeLevel, required this.distanceKm, required this.matchScore, required this.matchPercent, required this.riasecTrait, required this.collegeRating, required this.courseRating, required this.finalRank, required this.potentialCareers});
  
  factory CourseRecommendation.fromJson(Map<String, dynamic> json) {
    return CourseRecommendation(
      collegeName: json['college_name'],
      courseName: json['course_name'],
      degreeLevel: json['degree_level'],
      distanceKm: json['distance_km'].toDouble(),
      matchScore: json['match_score'].toDouble(),
      matchPercent: json['match_percent'],
      riasecTrait: json['riasec_trait'],
      collegeRating: json['college_rating'].toDouble(),
      courseRating: json['course_rating'].toDouble(),
      finalRank: json['final_rank'].toDouble(),
      potentialCareers: json['potential_careers'],
    );
  }
}
```

### Integration Methods

#### Get Course Recommendations
```dart
Future<List<CourseRecommendation>> getCourseRecommendations(CourseRecommendationRequest request) async {
  final response = await EducationApiService.post('/api/course/recommend', request.toJson());
  
  return (response['recommendations'] as List)
      .map((rec) => CourseRecommendation.fromJson(rec))
      .toList();
}
```

#### Get Current Location
```dart
import 'package:location/location.dart';

Future<LocationData?> getCurrentLocation() async {
  Location location = Location();
  
  bool serviceEnabled = await location.serviceEnabled();
  if (!serviceEnabled) {
    serviceEnabled = await location.requestService();
    if (!serviceEnabled) return null;
  }
  
  PermissionStatus permissionGranted = await location.hasPermission();
  if (permissionGranted == PermissionStatus.denied) {
    permissionGranted = await location.requestPermission();
    if (permissionGranted != PermissionStatus.granted) return null;
  }
  
  return await location.getLocation();
}
```

### Widget Implementation
```dart
class CourseRecommendationWidget extends StatefulWidget {
  final Map<String, int>? riasecProfile; // From career assessment
  
  CourseRecommendationWidget({this.riasecProfile});
  
  @override
  _CourseRecommendationWidgetState createState() => _CourseRecommendationWidgetState();
}

class _CourseRecommendationWidgetState extends State<CourseRecommendationWidget> {
  List<CourseRecommendation> recommendations = [];
  bool isLoading = false;
  String selectedGender = 'Male';
  String selectedEducation = '12th';
  double selectedRadius = 100.0;
  
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // Input form
        DropdownButton<String>(
          value: selectedGender,
          items: ['Male', 'Female', 'Other'].map((gender) =>
            DropdownMenuItem(value: gender, child: Text(gender))
          ).toList(),
          onChanged: (value) => setState(() { selectedGender = value!; }),
        ),
        
        DropdownButton<String>(
          value: selectedEducation,
          items: ['10th', '12th', 'Diploma', 'UG', 'PG'].map((edu) =>
            DropdownMenuItem(value: edu, child: Text(edu))
          ).toList(),
          onChanged: (value) => setState(() { selectedEducation = value!; }),
        ),
        
        Slider(
          value: selectedRadius,
          min: 10,
          max: 500,
          divisions: 49,
          label: '${selectedRadius.round()} km',
          onChanged: (value) => setState(() { selectedRadius = value; }),
        ),
        
        ElevatedButton(
          onPressed: widget.riasecProfile != null ? _getRecommendations : null,
          child: Text('Get Recommendations'),
        ),
        
        // Results
        if (isLoading) CircularProgressIndicator(),
        
        Expanded(
          child: ListView.builder(
            itemCount: recommendations.length,
            itemBuilder: (context, index) {
              final rec = recommendations[index];
              return Card(
                child: ListTile(
                  title: Text(rec.courseName),
                  subtitle: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(rec.collegeName),
                      Text('${rec.distanceKm.toStringAsFixed(1)} km away'),
                      Text(rec.matchPercent),
                    ],
                  ),
                  trailing: CircleAvatar(
                    child: Text('${(rec.finalRank * 100).round()}'),
                  ),
                ),
              );
            },
          ),
        ),
      ],
    );
  }
  
  Future<void> _getRecommendations() async {
    setState(() { isLoading = true; });
    
    try {
      final location = await getCurrentLocation();
      if (location == null) {
        // Handle location error
        return;
      }
      
      final request = CourseRecommendationRequest(
        userLatitude: location.latitude!,
        userLongitude: location.longitude!,
        userGender: selectedGender,
        educationLevel: selectedEducation,
        riasecProfile: widget.riasecProfile!,
        radiusKm: selectedRadius,
      );
      
      recommendations = await getCourseRecommendations(request);
    } catch (e) {
      // Handle error
      print('Error getting recommendations: $e');
    } finally {
      setState(() { isLoading = false; });
    }
  }
}
```

---

## 📰 4. News Recommender Integration

### Purpose
RIASEC personality-based news recommendations with 35 articles across 6 personality types.

### Data Models
```dart
class NewsRecommendationRequest {
  final String riasecTypes;
  final int numRecommendations;
  
  NewsRecommendationRequest({required this.riasecTypes, this.numRecommendations = 5});
  
  Map<String, dynamic> toJson() {
    return {
      'riasec_types': riasecTypes,
      'num_recommendations': numRecommendations,
    };
  }
}

class NewsArticle {
  final String newsId;
  final String headline;
  final String description;
  final String riasecType;
  final String riasecDescription;
  
  NewsArticle({required this.newsId, required this.headline, required this.description, required this.riasecType, required this.riasecDescription});
  
  factory NewsArticle.fromJson(Map<String, dynamic> json) {
    return NewsArticle(
      newsId: json['news_id'],
      headline: json['headline'],
      description: json['description'],
      riasecType: json['riasec_type'],
      riasecDescription: json['riasec_description'],
    );
  }
}
```

### Integration Methods

#### Get News Recommendations
```dart
Future<List<NewsArticle>> getNewsRecommendations(String riasecTypes, {int numRecommendations = 5}) async {
  final request = NewsRecommendationRequest(
    riasecTypes: riasecTypes,
    numRecommendations: numRecommendations,
  );
  
  final response = await EducationApiService.post('/api/news/recommend', request.toJson());
  
  return (response['recommendations'] as List)
      .map((article) => NewsArticle.fromJson(article))
      .toList();
}
```

#### Get News by Type
```dart
Future<List<NewsArticle>> getNewsByType(String riasecType) async {
  final response = await EducationApiService.get('/api/news/news-by-type/$riasecType');
  
  return (response['articles'] as List)
      .map((article) => NewsArticle.fromJson(article))
      .toList();
}
```

### Widget Implementation
```dart
class NewsRecommendationWidget extends StatefulWidget {
  final String? primaryRiasecType;
  final String? secondaryRiasecType;
  
  NewsRecommendationWidget({this.primaryRiasecType, this.secondaryRiasecType});
  
  @override
  _NewsRecommendationWidgetState createState() => _NewsRecommendationWidgetState();
}

class _NewsRecommendationWidgetState extends State<NewsRecommendationWidget> {
  List<NewsArticle> articles = [];
  bool isLoading = false;
  
  @override
  void initState() {
    super.initState();
    if (widget.primaryRiasecType != null) {
      _loadNews();
    }
  }
  
  Future<void> _loadNews() async {
    setState(() { isLoading = true; });
    
    try {
      String riasecTypes = widget.primaryRiasecType!;
      if (widget.secondaryRiasecType != null) {
        riasecTypes += widget.secondaryRiasecType!;
      }
      
      articles = await getNewsRecommendations(riasecTypes, numRecommendations: 10);
    } catch (e) {
      print('Error loading news: $e');
    } finally {
      setState(() { isLoading = false; });
    }
  }
  
  @override
  Widget build(BuildContext context) {
    if (isLoading) return CircularProgressIndicator();
    
    return ListView.builder(
      itemCount: articles.length,
      itemBuilder: (context, index) {
        final article = articles[index];
        return Card(
          child: ExpansionTile(
            title: Text(article.headline),
            subtitle: Text(article.riasecDescription),
            children: [
              Padding(
                padding: EdgeInsets.all(16.0),
                child: Text(article.description),
              ),
            ],
          ),
        );
      },
    );
  }
}
```

---

## 🎓 5. Scholarship Integration

### Purpose
Match scholarships based on eligibility criteria with 22 scholarship programs.

### Data Models
```dart
class ScholarshipMatchRequest {
  final String gender;
  final int age;
  final String educationLevel;
  final String domicile;
  final double? annualIncome;
  final String? socialCategory;
  final String? courseStream;
  final double? percentage;
  
  ScholarshipMatchRequest({
    required this.gender,
    required this.age,
    required this.educationLevel,
    required this.domicile,
    this.annualIncome,
    this.socialCategory,
    this.courseStream,
    this.percentage,
  });
  
  Map<String, dynamic> toJson() {
    Map<String, dynamic> json = {
      'gender': gender,
      'age': age,
      'education_level': educationLevel,
      'domicile': domicile,
    };
    if (annualIncome != null) json['annual_income'] = annualIncome;
    if (socialCategory != null) json['social_category'] = socialCategory;
    if (courseStream != null) json['course_stream'] = courseStream;
    if (percentage != null) json['percentage'] = percentage;
    return json;
  }
}

class Scholarship {
  final String scholarshipId;
  final String scholarshipName;
  final String providerName;
  final String providerType;
  final String description;
  final int? score;
  final int? matchPercentage;
  final Map<String, dynamic> benefits;
  final Map<String, String> applicationTimeline;
  final String? applicationPortalUrl;
  final List<String>? eligibilityMet;
  
  Scholarship({required this.scholarshipId, required this.scholarshipName, required this.providerName, required this.providerType, required this.description, this.score, this.matchPercentage, required this.benefits, required this.applicationTimeline, this.applicationPortalUrl, this.eligibilityMet});
  
  factory Scholarship.fromJson(Map<String, dynamic> json) {
    return Scholarship(
      scholarshipId: json['scholarship_id'],
      scholarshipName: json['scholarship_name'],
      providerName: json['provider_name'],
      providerType: json['provider_type'],
      description: json['description'],
      score: json['score'],
      matchPercentage: json['match_percentage'],
      benefits: json['benefits'],
      applicationTimeline: Map<String, String>.from(json['application_timeline']),
      applicationPortalUrl: json['application_portal_url'],
      eligibilityMet: json['eligibility_met']?.cast<String>(),
    );
  }
}
```

### Integration Methods

#### Match Scholarships
```dart
Future<List<Scholarship>> matchScholarships(ScholarshipMatchRequest request) async {
  final response = await EducationApiService.post('/api/scholarship/match', request.toJson());
  
  return (response['eligible_scholarships'] as List)
      .map((scholarship) => Scholarship.fromJson(scholarship))
      .toList();
}
```

#### Get All Scholarships
```dart
Future<List<Scholarship>> getAllScholarships() async {
  final response = await EducationApiService.get('/api/scholarship/scholarships');
  
  return (response['scholarships'] as List)
      .map((scholarship) => Scholarship.fromJson(scholarship))
      .toList();
}
```

### Widget Implementation
```dart
class ScholarshipMatchWidget extends StatefulWidget {
  @override
  _ScholarshipMatchWidgetState createState() => _ScholarshipMatchWidgetState();
}

class _ScholarshipMatchWidgetState extends State<ScholarshipMatchWidget> {
  List<Scholarship> scholarships = [];
  bool isLoading = false;
  
  // Form fields
  String selectedGender = 'Male';
  int age = 18;
  String selectedEducation = 'Undergraduate';
  String domicile = 'Jammu & Kashmir';
  double? annualIncome;
  String? selectedCategory;
  String? selectedStream;
  double? percentage;
  
  final _incomeController = TextEditingController();
  final _percentageController = TextEditingController();
  
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // Form
        DropdownButton<String>(
          value: selectedGender,
          items: ['Male', 'Female', 'Other'].map((gender) =>
            DropdownMenuItem(value: gender, child: Text(gender))
          ).toList(),
          onChanged: (value) => setState(() { selectedGender = value!; }),
        ),
        
        TextField(
          decoration: InputDecoration(labelText: 'Age'),
          keyboardType: TextInputType.number,
          onChanged: (value) => age = int.tryParse(value) ?? 18,
        ),
        
        DropdownButton<String>(
          value: selectedEducation,
          items: ['Pre-Matric (Class 1-10)', 'Undergraduate', 'Postgraduate'].map((edu) =>
            DropdownMenuItem(value: edu, child: Text(edu))
          ).toList(),
          onChanged: (value) => setState(() { selectedEducation = value!; }),
        ),
        
        TextField(
          controller: _incomeController,
          decoration: InputDecoration(labelText: 'Annual Income (optional)'),
          keyboardType: TextInputType.number,
          onChanged: (value) => annualIncome = double.tryParse(value),
        ),
        
        DropdownButton<String?>(
          hint: Text('Social Category (optional)'),
          value: selectedCategory,
          items: [null, 'General', 'OBC', 'SC', 'ST', 'Minority'].map((category) =>
            DropdownMenuItem(value: category, child: Text(category ?? 'Select Category'))
          ).toList(),
          onChanged: (value) => setState(() { selectedCategory = value; }),
        ),
        
        DropdownButton<String?>(
          hint: Text('Course Stream (optional)'),
          value: selectedStream,
          items: [null, 'Engineering', 'Medical', 'General'].map((stream) =>
            DropdownMenuItem(value: stream, child: Text(stream ?? 'Select Stream'))
          ).toList(),
          onChanged: (value) => setState(() { selectedStream = value; }),
        ),
        
        TextField(
          controller: _percentageController,
          decoration: InputDecoration(labelText: 'Academic Percentage (optional)'),
          keyboardType: TextInputType.number,
          onChanged: (value) => percentage = double.tryParse(value),
        ),
        
        ElevatedButton(
          onPressed: _matchScholarships,
          child: Text('Find Scholarships'),
        ),
        
        // Results
        if (isLoading) CircularProgressIndicator(),
        
        Expanded(
          child: ListView.builder(
            itemCount: scholarships.length,
            itemBuilder: (context, index) {
              final scholarship = scholarships[index];
              return Card(
                child: ExpansionTile(
                  title: Text(scholarship.scholarshipName),
                  subtitle: Text('${scholarship.providerName} - Match: ${scholarship.matchPercentage ?? 'N/A'}%'),
                  children: [
                    Padding(
                      padding: EdgeInsets.all(16.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(scholarship.description),
                          SizedBox(height: 8),
                          Text('Benefits: ${scholarship.benefits['total_value_description'] ?? 'N/A'}'),
                          if (scholarship.applicationPortalUrl != null)
                            TextButton(
                              onPressed: () {
                                // Launch URL
                              },
                              child: Text('Apply Now'),
                            ),
                        ],
                      ),
                    ),
                  ],
                ),
              );
            },
          ),
        ),
      ],
    );
  }
  
  Future<void> _matchScholarships() async {
    setState(() { isLoading = true; });
    
    try {
      final request = ScholarshipMatchRequest(
        gender: selectedGender,
        age: age,
        educationLevel: selectedEducation,
        domicile: domicile,
        annualIncome: annualIncome,
        socialCategory: selectedCategory,
        courseStream: selectedStream,
        percentage: percentage,
      );
      
      scholarships = await matchScholarships(request);
    } catch (e) {
      print('Error matching scholarships: $e');
    } finally {
      setState(() { isLoading = false; });
    }
  }
}
```

---

## 🔄 Complete Integration Flow

### 1. Main App Architecture
```dart
class EducationApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Education Platform',
      home: MainNavigationScreen(),
    );
  }
}

class MainNavigationScreen extends StatefulWidget {
  @override
  _MainNavigationScreenState createState() => _MainNavigationScreenState();
}

class _MainNavigationScreenState extends State<MainNavigationScreen> {
  int currentIndex = 0;
  Map<String, int>? riasecProfile;
  String? primaryType;
  String? secondaryType;
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(
        index: currentIndex,
        children: [
          CareerAssessmentWidget(
            onResultsReady: (results) {
              setState(() {
                riasecProfile = results.personalityProfile;
                primaryType = results.primaryType;
                secondaryType = results.secondaryType;
              });
            },
          ),
          CollegeFinderWidget(),
          CourseRecommendationWidget(riasecProfile: riasecProfile),
          NewsRecommendationWidget(
            primaryRiasecType: primaryType,
            secondaryRiasecType: secondaryType,
          ),
          ScholarshipMatchWidget(),
        ],
      ),
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        currentIndex: currentIndex,
        onTap: (index) => setState(() { currentIndex = index; }),
        items: [
          BottomNavigationBarItem(icon: Icon(Icons.psychology), label: 'Career'),
          BottomNavigationBarItem(icon: Icon(Icons.school), label: 'Colleges'),
          BottomNavigationBarItem(icon: Icon(Icons.recommend), label: 'Courses'),
          BottomNavigationBarItem(icon: Icon(Icons.article), label: 'News'),
          BottomNavigationBarItem(icon: Icon(Icons.monetization_on), label: 'Scholarships'),
        ],
      ),
    );
  }
}
```

### 2. Error Handling Strategy
```dart
class ApiException implements Exception {
  final String message;
  final int? statusCode;
  
  ApiException(this.message, [this.statusCode]);
  
  @override
  String toString() => 'ApiException: $message ${statusCode != null ? '($statusCode)' : ''}';
}

Future<T> handleApiCall<T>(Future<T> Function() apiCall) async {
  try {
    return await apiCall();
  } on SocketException {
    throw ApiException('No internet connection');
  } on HttpException {
    throw ApiException('Server error');
  } on FormatException {
    throw ApiException('Invalid response format');
  } catch (e) {
    throw ApiException('Unexpected error: $e');
  }
}
```

### 3. State Management with Provider
```dart
// Add to pubspec.yaml
dependencies:
  provider: ^6.1.1

// State management
class EducationState extends ChangeNotifier {
  Map<String, int>? _riasecProfile;
  String? _primaryType;
  String? _secondaryType;
  LocationData? _currentLocation;
  
  Map<String, int>? get riasecProfile => _riasecProfile;
  String? get primaryType => _primaryType;
  String? get secondaryType => _secondaryType;
  LocationData? get currentLocation => _currentLocation;
  
  void setCareerResults(CareerResult results) {
    _riasecProfile = results.personalityProfile;
    _primaryType = results.primaryType;
    _secondaryType = results.secondaryType;
    notifyListeners();
  }
  
  void setLocation(LocationData location) {
    _currentLocation = location;
    notifyListeners();
  }
}

// Usage in main.dart
void main() {
  runApp(
    ChangeNotifierProvider(
      create: (context) => EducationState(),
      child: EducationApp(),
    ),
  );
}
```

---

## 🚀 Deployment & Production Considerations

### Environment Configuration
```dart
class ApiConfig {
  static const String baseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://localhost:8080',
  );
  
  static const bool isProduction = bool.fromEnvironment('PRODUCTION', defaultValue: false);
  
  static const Duration requestTimeout = Duration(seconds: 30);
}
```

### Network Security
```dart
class SecureApiService {
  static final Dio _dio = Dio(BaseOptions(
    baseUrl: ApiConfig.baseUrl,
    connectTimeout: ApiConfig.requestTimeout,
    receiveTimeout: ApiConfig.requestTimeout,
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
  ));
  
  static Future<Response> post(String endpoint, Map<String, dynamic> data) async {
    try {
      return await _dio.post(endpoint, data: data);
    } on DioException catch (e) {
      throw _handleDioError(e);
    }
  }
  
  static ApiException _handleDioError(DioException e) {
    switch (e.type) {
      case DioExceptionType.connectionTimeout:
        return ApiException('Connection timeout');
      case DioExceptionType.receiveTimeout:
        return ApiException('Receive timeout');
      case DioExceptionType.badResponse:
        return ApiException('Server error: ${e.response?.statusCode}');
      default:
        return ApiException('Network error');
    }
  }
}
```

---

## 📱 Testing Integration

### Unit Tests
```dart
// test/api_service_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:http/http.dart' as http;

void main() {
  group('Education API Service Tests', () {
    test('should start career assessment successfully', () async {
      // Mock HTTP response
      final mockResponse = http.Response(
        '{"success": true, "session_id": "test-session", "total_questions": 24}',
        200,
        headers: {'content-type': 'application/json'},
      );
      
      // Test the API call
      final session = await startCareerAssessment();
      expect(session.sessionId, 'test-session');
      expect(session.totalQuestions, 24);
    });
  });
}
```

### Widget Tests
```dart
// test/career_assessment_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('Career Assessment Widget should display question', (WidgetTester tester) async {
    await tester.pumpWidget(MaterialApp(
      home: CareerAssessmentWidget(),
    ));
    
    // Wait for async operations
    await tester.pumpAndSettle();
    
    // Verify question is displayed
    expect(find.text('Question 1/24'), findsOneWidget);
    expect(find.byType(Radio), findsNWidgets(5));
  });
}
```

---

## 🎯 AI Agent Instructions Summary

**You are now equipped with complete integration knowledge for the Education Platform Unified Backend API. Your responsibilities include:**

1. **Career Guidance**: Implement 24-question RIASEC assessment with session management
2. **College Finder**: Search/filter 137 J&K colleges with multiple criteria
3. **Course Suggestions**: AI-powered recommendations using location + personality + ranking
4. **News Recommendations**: RIASEC-based article suggestions from 35 news items
5. **Scholarship Matching**: Eligibility-based matching from 22 scholarship programs

**Key Integration Points:**
- Base URL: `http://localhost:8080`
- All APIs use JSON request/response
- RIASEC personality profiles link career → course → news services
- Location services required for course recommendations
- Session management for career assessments
- Comprehensive error handling required

**Flutter Dependencies Required:**
- `http` or `dio` for API calls
- `location` for GPS coordinates
- `shared_preferences` for session storage
- `provider` for state management

**Always verify server health before API calls and implement proper error handling for production apps.**
