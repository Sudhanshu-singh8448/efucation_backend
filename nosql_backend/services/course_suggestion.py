"""
Course Suggestion Service - NoSQL Version
Provides course recommendations based on RIASEC traits with MongoDB storage
"""

from flask import Blueprint, request, jsonify
import logging
from typing import Dict, List, Any, Optional
from database import get_collection, COLLECTIONS
import pandas as pd
import os
from geopy.distance import geodesic

logger = logging.getLogger(__name__)

course_suggestion_bp = Blueprint('course_suggestion', __name__)

def load_course_data_to_mongodb():
    """Load course data from CSV to MongoDB"""
    try:
        csv_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'courseAndCollegedata.csv')
        if not os.path.exists(csv_path):
            logger.warning(f"Course CSV not found at {csv_path}")
            return
        
        courses_collection = get_collection(COLLECTIONS['courses'])
        
        # Check if data already loaded
        try:
            count = courses_collection.count_documents({})
            if count > 0:
                logger.info("Course data already loaded in MongoDB")
                return
        except Exception as e:
            logger.warning(f"Could not check existing data: {e}")
            # Continue with loading
        
        # Load CSV data
        data = []
        with open(csv_path, 'r') as file:
            lines = file.readlines()
            lines = [line for line in lines if line.strip()]
            
            import csv
            reader = csv.DictReader(lines)
            for row in reader:
                try:
                    row['Latitude'] = float(row['Latitude'])
                    row['Longitude'] = float(row['Longitude'])
                    row['College_Rating_Placeholder'] = float(row['College_Rating_Placeholder'])
                    row['Course_Rating_Placeholder'] = float(row['Course_Rating_Placeholder'])
                    row['created_at'] = pd.Timestamp.now()
                    row['updated_at'] = pd.Timestamp.now()
                    data.append(row)
                except (ValueError, KeyError) as e:
                    logger.warning(f"Skipping row due to error: {e}")
                    continue
        
        if data:
            courses_collection.insert_many(data)
            logger.info(f"Loaded {len(data)} courses into MongoDB")
        
    except Exception as e:
        logger.error(f"Error loading course data: {e}")

# RIASEC to course field mapping
RIASEC_COURSE_MAPPING = {
    'realistic': [
        'Engineering', 'Architecture', 'Agriculture', 'Aviation', 'Automotive',
        'Construction', 'Manufacturing', 'Technology', 'Mechanical', 'Civil',
        'Computer Science', 'Information Technology'
    ],
    'investigative': [
        'Medicine', 'Science', 'Research', 'Biology', 'Chemistry', 'Physics',
        'Mathematics', 'Psychology', 'Pharmacy', 'Biotechnology', 'Medical',
        'Health Sciences', 'Laboratory', 'Computer Science'
    ],
    'artistic': [
        'Arts', 'Design', 'Media', 'Communication', 'Journalism', 'Fine Arts',
        'Graphic Design', 'Fashion', 'Photography', 'Music', 'Literature',
        'Creative Writing', 'Film', 'Animation'
    ],
    'social': [
        'Education', 'Social Work', 'Psychology', 'Teaching', 'Counseling',
        'Human Resources', 'Social Sciences', 'Community Development',
        'Public Administration', 'Sociology', 'Anthropology'
    ],
    'enterprising': [
        'Business', 'Management', 'Marketing', 'Finance', 'Economics',
        'Commerce', 'Entrepreneurship', 'Sales', 'Leadership', 'MBA',
        'Banking', 'Insurance', 'International Business'
    ],
    'conventional': [
        'Accounting', 'Administration', 'Office Management', 'Data Entry',
        'Statistics', 'Bookkeeping', 'Clerical', 'Finance', 'Banking',
        'Insurance', 'Government', 'Public Service'
    ]
}

@course_suggestion_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        courses_collection = get_collection(COLLECTIONS['courses'])
        total_courses = courses_collection.count_documents({})
        
        return jsonify({
            'status': 'healthy',
            'service': 'Course Suggestion API',
            'version': '1.0.0',
            'total_courses': total_courses,
            'database': 'connected'
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'service': 'Course Suggestion API',
            'error': str(e)
        }), 500

@course_suggestion_bp.route('/recommend', methods=['POST'])
def get_course_recommendations():
    """Get course recommendations based on RIASEC traits and preferences"""
    try:
        data = request.get_json() or {}
        
        # Extract request parameters
        riasec_scores = data.get('riasec_scores', {})
        location = data.get('location', {})
        preferences = data.get('preferences', {})
        
        courses_collection = get_collection(COLLECTIONS['courses'])
        
        # Build query based on RIASEC scores
        query = {}
        course_fields = []
        
        # Get relevant course fields based on top RIASEC traits
        if riasec_scores:
            sorted_traits = sorted(riasec_scores.items(), key=lambda x: x[1], reverse=True)
            top_traits = [trait for trait, score in sorted_traits[:3] if score > 0]
            
            for trait in top_traits:
                if trait in RIASEC_COURSE_MAPPING:
                    course_fields.extend(RIASEC_COURSE_MAPPING[trait])
        
        # Build course field query
        if course_fields:
            field_patterns = [{'Course': {'$regex': field, '$options': 'i'}} for field in course_fields]
            query['$or'] = field_patterns
        
        # Location preferences
        if location:
            if 'state' in location and location['state']:
                query['State'] = {'$regex': location['state'], '$options': 'i'}
            if 'city' in location and location['city']:
                query['City'] = {'$regex': location['city'], '$options': 'i'}
        
        # Other preferences
        if preferences:
            if 'college_type' in preferences and preferences['college_type']:
                query['College_Type'] = {'$regex': preferences['college_type'], '$options': 'i'}
            
            if 'min_rating' in preferences:
                query['Course_Rating_Placeholder'] = {'$gte': preferences['min_rating']}
        
        # Execute query with sorting
        courses = list(courses_collection.find(query, {'_id': 0}).sort([
            ('Course_Rating_Placeholder', -1),
            ('College_Rating_Placeholder', -1)
        ]).limit(50))
        
        # Calculate match scores
        for course in courses:
            course['match_score'] = calculate_match_score(course, riasec_scores, preferences)
        
        # Sort by match score
        courses.sort(key=lambda x: x['match_score'], reverse=True)
        
        return jsonify({
            'success': True,
            'total_recommendations': len(courses),
            'riasec_scores': riasec_scores,
            'recommendations': courses[:20]  # Return top 20
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting course recommendations: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get course recommendations',
            'details': str(e)
        }), 500

@course_suggestion_bp.route('/search', methods=['GET'])
def search_alias():
    """Alias for /courses/search to maintain compatibility"""
    return search_courses()

def calculate_match_score(course, riasec_scores, preferences):
    """Calculate match score for a course based on RIASEC and preferences"""
    score = 0
    
    # RIASEC matching (60% weight)
    if riasec_scores:
        course_name = course.get('Course', '').lower()
        for trait, trait_score in riasec_scores.items():
            if trait in RIASEC_COURSE_MAPPING:
                for field in RIASEC_COURSE_MAPPING[trait]:
                    if field.lower() in course_name:
                        score += trait_score * 0.6
                        break
    
    # Course rating (25% weight)
    course_rating = course.get('Course_Rating_Placeholder', 0)
    score += course_rating * 25
    
    # College rating (15% weight)
    college_rating = course.get('College_Rating_Placeholder', 0)
    score += college_rating * 15
    
    return round(score, 2)

@course_suggestion_bp.route('/courses', methods=['GET'])
def get_all_courses():
    """Get all available courses"""
    try:
        courses_collection = get_collection(COLLECTIONS['courses'])
        courses = list(courses_collection.find({}, {'_id': 0}))
        
        return jsonify({
            'success': True,
            'total_courses': len(courses),
            'courses': courses
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting courses: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get courses',
            'details': str(e)
        }), 500

@course_suggestion_bp.route('/courses/search', methods=['GET'])
def search_courses():
    """Search courses by name or field"""
    try:
        search_term = request.args.get('q', '').strip()
        
        if not search_term:
            return jsonify({
                'success': False,
                'error': 'Search term is required'
            }), 400
        
        courses_collection = get_collection(COLLECTIONS['courses'])
        
        query = {
            '$or': [
                {'Course': {'$regex': search_term, '$options': 'i'}},
                {'College_Name': {'$regex': search_term, '$options': 'i'}},
                {'Specialization': {'$regex': search_term, '$options': 'i'}}
            ]
        }
        
        courses = list(courses_collection.find(query, {'_id': 0}))
        
        return jsonify({
            'success': True,
            'search_term': search_term,
            'total_results': len(courses),
            'courses': courses
        }), 200
        
    except Exception as e:
        logger.error(f"Error searching courses: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to search courses',
            'details': str(e)
        }), 500

# Data will be loaded on first request or during app initialization
