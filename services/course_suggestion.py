"""
Course Suggestion Service
Converted from FastAPI to Flask Blueprint for unified backend
"""

from flask import Blueprint, request, jsonify
import csv
import os
from typing import List, Dict, Optional
from geopy.distance import geodesic

# Create Blueprint
course_suggestion_bp = Blueprint('course_suggestion', __name__)

# Load the dataset
def load_course_data():
    """Load course data from CSV file"""
    try:
        # Try to load from the data directory
        csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'courseAndCollegedata.csv')
        if not os.path.exists(csv_path):
            # Fallback to original location
            csv_path = '/Users/sudhanshukumar/project/backend/course_Suggestion_backend/courseAndCollegedata.csv'
        
        data = []
        with open(csv_path, 'r') as file:
            # Skip the first empty line
            lines = file.readlines()
            lines = [line for line in lines if line.strip()]  # Remove empty lines
            
            reader = csv.DictReader(lines)
            for row in reader:
                # Convert numeric fields
                try:
                    row['Latitude'] = float(row['Latitude'])
                    row['Longitude'] = float(row['Longitude'])
                    row['College_Rating_Placeholder'] = float(row['College_Rating_Placeholder'])
                    row['Course_Rating_Placeholder'] = float(row['Course_Rating_Placeholder'])
                    data.append(row)
                except (ValueError, KeyError) as e:
                    print(f"Skipping row due to error: {e}")
                    continue  # Skip rows with invalid data
        
        print(f"Loaded {len(data)} courses from dataset")
        return data
    except FileNotFoundError:
        print("Warning: courseAndCollegedata.csv not found. Using empty dataset.")
        return []

# Load data on startup
course_data = load_course_data()

class RecommendationEngine:
    def __init__(self, dataset):
        self.data = dataset
        
    def layer1_initial_filtering(self, user_lat, user_lon, education_level, radius_km):
        """
        Layer 1: Initial Filtering (Knowledge-Based)
        - Filter by location (within radius)
        - Filter by education level eligibility
        """
        if not self.data:
            return []
            
        filtered_data = []
        
        for row in self.data:
            try:
                # Rule 1: Location filtering
                college_coords = (row['Latitude'], row['Longitude'])
                user_coords = (user_lat, user_lon)
                distance = geodesic(user_coords, college_coords).kilometers
                
                if distance > radius_km:
                    continue
                
                # Rule 2: Education level eligibility
                if education_level == '12th':
                    # Show UG and PG courses for 12th pass students
                    if row['Degree_Level'] not in ['UG', 'PG']:
                        continue
                elif education_level == '10th':
                    # Show diploma and certificate courses for 10th pass students
                    # For now, we'll include UG as well since the dataset mainly has UG courses
                    if row['Degree_Level'] not in ['UG', 'Diploma', 'Certificate']:
                        continue
                
                # Add distance to the row
                row_copy = row.copy()
                row_copy['Distance_km'] = distance
                filtered_data.append(row_copy)
                
            except (ValueError, KeyError):
                continue
        
        return filtered_data
    
    def layer2_personalized_scoring(self, filtered_data, riasec_profile):
        """
        Layer 2: Personalized Scoring (Content-Based)
        Calculate match score based on RIASEC profile
        """
        if not filtered_data:
            return filtered_data
            
        for row in filtered_data:
            # Get the primary trait for the course
            primary_trait = row['RIASEC_Trait']
            
            # For simplicity, we'll use the primary trait with higher weight
            primary_score = riasec_profile.get(primary_trait, 0) * 1.5
            
            # Calculate secondary score based on course type patterns
            secondary_score = 0
            course_name = row['Course_Name'].lower()
            
            # Define secondary trait mappings based on course patterns
            secondary_traits = {
                'engineering': 'I',
                'management': 'E',
                'arts': 'A',
                'science': 'I',
                'commerce': 'C',
                'education': 'S',
                'medical': 'I',
                'nursing': 'S',
                'journalism': 'A'
            }
            
            for pattern, trait in secondary_traits.items():
                if pattern in course_name and trait != primary_trait:
                    secondary_score = riasec_profile.get(trait, 0) * 1.0
                    break
            
            row['Match_Score'] = primary_score + secondary_score
            
            # Calculate match percentage
            max_possible_score = max(riasec_profile.values()) * 1.5 + max(riasec_profile.values()) * 1.0
            row['Match_Percent'] = (row['Match_Score'] / max_possible_score * 100) if max_possible_score > 0 else 0
        
        return filtered_data
    
    def layer3_final_ranking(self, scored_data):
        """
        Layer 3: Final Ranking (Learning-to-Rank)
        Combine multiple factors for final ranking
        """
        if not scored_data:
            return scored_data
            
        # Weights for different factors
        w1 = 0.6  # Match score weight (highest priority)
        w2 = 0.25  # Course rating weight
        w3 = 0.15  # College rating weight
        
        # Get min/max for normalization
        match_scores = [row['Match_Score'] for row in scored_data]
        course_ratings = [row['Course_Rating_Placeholder'] for row in scored_data]
        college_ratings = [row['College_Rating_Placeholder'] for row in scored_data]
        
        def normalize(value, min_val, max_val):
            if max_val == min_val:
                return 0
            return (value - min_val) / (max_val - min_val)
        
        min_match, max_match = min(match_scores), max(match_scores)
        min_course, max_course = min(course_ratings), max(course_ratings)
        min_college, max_college = min(college_ratings), max(college_ratings)
        
        for row in scored_data:
            # Normalize each component
            norm_match = normalize(row['Match_Score'], min_match, max_match)
            norm_course_rating = normalize(row['Course_Rating_Placeholder'], min_course, max_course)
            norm_college_rating = normalize(row['College_Rating_Placeholder'], min_college, max_college)
            
            # Calculate final rank
            row['Final_Rank'] = (
                w1 * norm_match +
                w2 * norm_course_rating +
                w3 * norm_college_rating
            )
        
        # Sort by final rank (descending)
        scored_data.sort(key=lambda x: x['Final_Rank'], reverse=True)
        
        return scored_data
    
    def get_recommendations(self, request_data):
        """
        Main recommendation function that applies all three layers
        """
        # Layer 1: Initial Filtering
        layer1_results = self.layer1_initial_filtering(
            request_data['user_latitude'],
            request_data['user_longitude'],
            request_data['education_level'],
            request_data.get('radius_km', 100.0)
        )
        
        # Layer 2: Personalized Scoring
        layer2_results = self.layer2_personalized_scoring(
            layer1_results,
            request_data['riasec_profile']
        )
        
        # Layer 3: Final Ranking
        final_results = self.layer3_final_ranking(layer2_results)
        
        # Limit results
        max_results = request_data.get('max_results', 20)
        final_results = final_results[:max_results]
        
        return final_results

# Initialize recommendation engine
recommender = RecommendationEngine(course_data)

@course_suggestion_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Course Suggestion API',
        'version': '1.0.0',
        'dataset_loaded': len(course_data) > 0,
        'total_courses': len(course_data)
    }), 200

@course_suggestion_bp.route('/', methods=['GET'])
def root():
    """Root endpoint with API information"""
    return jsonify({
        "message": "Course Recommendation System API",
        "version": "1.0.0",
        "endpoints": {
            "/": "GET - API information",
            "/recommend": "POST - Get course recommendations",
            "/dataset-info": "GET - Dataset information"
        }
    })

@course_suggestion_bp.route('/dataset-info', methods=['GET'])
def dataset_info():
    """Get information about the loaded dataset"""
    if not course_data:
        return jsonify({"error": "No dataset loaded"}), 404
    
    # Count unique colleges
    colleges = set(row['College_Name'] for row in course_data)
    
    # Count degree levels
    degree_levels = {}
    for row in course_data:
        level = row['Degree_Level']
        degree_levels[level] = degree_levels.get(level, 0) + 1
    
    # Count RIASEC traits
    riasec_traits = {}
    for row in course_data:
        trait = row['RIASEC_Trait']
        riasec_traits[trait] = riasec_traits.get(trait, 0) + 1
    
    # Sample courses
    sample_courses = [row['Course_Name'] for row in course_data[:10]]
    
    return jsonify({
        "total_courses": len(course_data),
        "colleges": len(colleges),
        "degree_levels": degree_levels,
        "riasec_traits": riasec_traits,
        "sample_courses": sample_courses
    })

@course_suggestion_bp.route('/recommend', methods=['POST'])
def recommend_courses():
    """
    Get personalized course recommendations using 3-layer filtering approach
    
    Expected JSON payload:
    {
        "user_latitude": float,
        "user_longitude": float,
        "user_gender": "Male" or "Female",
        "education_level": "10th" or "12th",
        "riasec_profile": {
            "R": int (1-10),
            "I": int (1-10),
            "A": int (1-10),
            "S": int (1-10),
            "E": int (1-10),
            "C": int (1-10)
        },
        "radius_km": float (optional, default 100.0),
        "max_results": int (optional, default 20)
    }
    """
    try:
        if not course_data:
            return jsonify({"error": "Dataset not loaded"}), 404
        
        request_data = request.get_json()
        if not request_data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Validate required fields
        required_fields = ['user_latitude', 'user_longitude', 'education_level', 'riasec_profile']
        for field in required_fields:
            if field not in request_data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Validate RIASEC scores (should be between 1-10)
        riasec_profile = request_data['riasec_profile']
        for trait, score in riasec_profile.items():
            if not isinstance(score, (int, float)) or not (1 <= score <= 10):
                return jsonify({
                    "error": f"RIASEC score for trait '{trait}' should be between 1 and 10"
                }), 400
        
        # Get recommendations
        results = recommender.get_recommendations(request_data)
        
        # Format response
        recommendations = []
        for row in results:
            recommendations.append({
                "college_name": row['College_Name'],
                "course_name": row['Course_Name'],
                "distance_km": round(row['Distance_km'], 2),
                "match_score": round(row['Match_Score'], 2),
                "match_percent": f"{row['Match_Percent']:.1f}% Match with your personality",
                "potential_careers": row['Potential_Professions'],
                "course_rating": row['Course_Rating_Placeholder'],
                "college_rating": row['College_Rating_Placeholder'],
                "final_rank": round(row['Final_Rank'], 3),
                "degree_level": row['Degree_Level'],
                "riasec_trait": row['RIASEC_Trait']
            })
        
        # Calculate layer1 filtered count for algorithm info
        layer1_count = len(recommender.layer1_initial_filtering(
            request_data['user_latitude'], request_data['user_longitude'], 
            request_data['education_level'], request_data.get('radius_km', 100.0)
        ))
        
        return jsonify({
            "total_results": len(recommendations),
            "recommendations": recommendations,
            "user_input": {
                "location": [request_data['user_latitude'], request_data['user_longitude']],
                "education_level": request_data['education_level'],
                "gender": request_data.get('user_gender', 'Not specified'),
                "riasec_profile": riasec_profile,
                "radius_km": request_data.get('radius_km', 100.0)
            },
            "algorithm_info": {
                "approach": "3-Layer Filtering (Knowledge-Based + Content-Based + Learning-to-Rank)",
                "layer1_filtered": layer1_count,
                "weights": {"personality_match": 0.6, "course_rating": 0.25, "college_rating": 0.15}
            }
        })
        
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500
