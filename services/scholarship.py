"""
Scholarship Service
Converted from standalone Flask app to Blueprint for unified backend
"""

from flask import Blueprint, request, jsonify
import json
import os
from datetime import datetime

# Create Blueprint
scholarship_bp = Blueprint('scholarship', __name__)

def load_scholarships():
    """Load scholarship data from JSON file"""
    try:
        # Try to load from the data directory
        json_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'scholarship.json')
        if not os.path.exists(json_path):
            # Fallback to original location
            json_path = '/Users/sudhanshukumar/project/backend/scholarship_backend/scholarship.json'
        
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Warning: scholarship.json file not found!")
        return []
    except json.JSONDecodeError:
        print("Warning: scholarship.json file is corrupted!")
        return []

def calculate_age(birth_year):
    """Calculate age from birth year"""
    current_year = datetime.now().year
    return current_year - birth_year

def match_scholarships(user_profile):
    """Match scholarships based on user profile"""
    scholarships = load_scholarships()
    matched_scholarships = []
    
    for scholarship in scholarships:
        eligibility = scholarship.get('eligibility_criteria', {})
        is_eligible = True
        match_score = 0
        reasons = []
        
        # Check domicile
        user_domicile = user_profile.get('domicile')
        eligible_domiciles = eligibility.get('domicile', [])
        if eligible_domiciles and user_domicile:
            if user_domicile not in eligible_domiciles:
                is_eligible = False
                reasons.append(f"Domicile requirement not met. Required: {', '.join(eligible_domiciles)}")
            else:
                match_score += 20
        
        # Check gender
        user_gender = user_profile.get('gender')
        eligible_gender = eligibility.get('gender')
        if eligible_gender and eligible_gender != 'All' and user_gender:
            if user_gender.lower() != eligible_gender.lower():
                is_eligible = False
                reasons.append(f"Gender requirement not met. Required: {eligible_gender}")
            else:
                match_score += 15
        elif eligible_gender == 'All':
            match_score += 10
        
        # Check age
        user_age = user_profile.get('age')
        min_age = eligibility.get('min_age')
        max_age = eligibility.get('max_age')
        if user_age:
            if min_age and user_age < min_age:
                is_eligible = False
                reasons.append(f"Age too low. Minimum age: {min_age}")
            elif max_age and user_age > max_age:
                is_eligible = False
                reasons.append(f"Age too high. Maximum age: {max_age}")
            else:
                match_score += 10
        
        # Check income
        user_income = user_profile.get('annual_income')
        income_ceiling = eligibility.get('income_ceiling_pa')
        if user_income and income_ceiling:
            if user_income > income_ceiling:
                is_eligible = False
                reasons.append(f"Income exceeds limit. Maximum income: ₹{income_ceiling:,}")
            else:
                match_score += 15
        
        # Check social category
        user_category = user_profile.get('social_category')
        eligible_categories = eligibility.get('social_category')
        if eligible_categories and user_category:
            if user_category not in eligible_categories:
                is_eligible = False
                reasons.append(f"Social category not eligible. Required: {', '.join(eligible_categories)}")
            else:
                match_score += 15
        
        # Check education level
        user_education = user_profile.get('education_level')
        eligible_education = eligibility.get('education_level')
        if eligible_education and user_education:
            if user_education not in eligible_education:
                is_eligible = False
                reasons.append(f"Education level not eligible. Required: {', '.join(eligible_education)}")
            else:
                match_score += 20
        
        # Check course stream
        user_stream = user_profile.get('course_stream')
        eligible_streams = eligibility.get('course_stream')
        if eligible_streams and user_stream:
            if user_stream not in eligible_streams:
                match_score -= 5  # Minor penalty but not disqualifying
                reasons.append(f"Course stream preference: {', '.join(eligible_streams)}")
            else:
                match_score += 10
        
        # Check academic percentage
        user_percentage = user_profile.get('percentage')
        min_percentage = eligibility.get('academic_requirements', {}).get('min_percentage')
        if user_percentage and min_percentage:
            if user_percentage < min_percentage:
                is_eligible = False
                reasons.append(f"Academic percentage too low. Minimum required: {min_percentage}%")
            else:
                match_score += 10
        
        # Add scholarship to results
        scholarship_result = {
            **scholarship,
            'is_eligible': is_eligible,
            'match_score': max(0, match_score),
            'eligibility_reasons': reasons if not is_eligible else ["All eligibility criteria met"],
            'recommendation_level': 'High' if match_score >= 70 else 'Medium' if match_score >= 40 else 'Low'
        }
        
        matched_scholarships.append(scholarship_result)
    
    # Sort by eligibility first, then by match score
    matched_scholarships.sort(key=lambda x: (x['is_eligible'], x['match_score']), reverse=True)
    
    return matched_scholarships

@scholarship_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Scholarship API',
        'version': '1.0.0',
        'total_scholarships': len(load_scholarships()),
        'timestamp': datetime.now().isoformat()
    }), 200

@scholarship_bp.route('/', methods=['GET'])
def home():
    """Home endpoint with API documentation"""
    return jsonify({
        'message': 'Scholarship Recommender API',
        'version': '1.0.0',
        'endpoints': {
            '/': 'GET - API information',
            '/match': 'POST - Match scholarships based on user profile',
            '/scholarships': 'GET - Get all scholarships',
            '/scholarships/<id>': 'GET - Get scholarship by ID'
        },
        'sample_request': {
            'url': 'POST /match',
            'body': {
                'gender': 'Male',
                'age': 20,
                'education_level': 'Undergraduate',
                'domicile': 'Jammu & Kashmir',
                'annual_income': 400000,
                'social_category': 'General',
                'course_stream': 'Engineering',
                'percentage': 85.5
            }
        }
    })

@scholarship_bp.route('/match', methods=['POST'])
def match_user_scholarships():
    """API endpoint to match scholarships based on user profile"""
    try:
        user_profile = request.get_json()
        
        if not user_profile:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        # Validate required fields
        required_fields = ['gender', 'age', 'education_level', 'domicile']
        missing_fields = [field for field in required_fields if not user_profile.get(field)]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}',
                'required_fields': {
                    'gender': 'Male/Female/Other',
                    'age': 'Age in years (integer)',
                    'education_level': 'e.g., Undergraduate, Postgraduate, Pre-Matric (Class 1-10)',
                    'domicile': 'e.g., Jammu & Kashmir',
                    'annual_income': 'Annual family income (optional)',
                    'social_category': 'e.g., General, OBC, SC, ST, Minority (optional)',
                    'course_stream': 'e.g., Engineering, Medical, General (optional)',
                    'percentage': 'Academic percentage (optional)'
                }
            }), 400
        
        # Calculate age if birth_year is provided instead of age
        if 'birth_year' in user_profile and 'age' not in user_profile:
            user_profile['age'] = calculate_age(user_profile['birth_year'])
        
        matched_scholarships = match_scholarships(user_profile)
        
        # Separate eligible and non-eligible scholarships
        eligible_scholarships = [s for s in matched_scholarships if s['is_eligible']]
        ineligible_scholarships = [s for s in matched_scholarships if not s['is_eligible']]
        
        return jsonify({
            'success': True,
            'user_profile': user_profile,
            'total_scholarships': len(matched_scholarships),
            'eligible_count': len(eligible_scholarships),
            'ineligible_count': len(ineligible_scholarships),
            'eligible_scholarships': eligible_scholarships,
            'ineligible_scholarships': ineligible_scholarships[:5],  # Limit to first 5 ineligible
            'recommendations': {
                'high_match': [s for s in eligible_scholarships if s['recommendation_level'] == 'High'],
                'medium_match': [s for s in eligible_scholarships if s['recommendation_level'] == 'Medium'],
                'low_match': [s for s in eligible_scholarships if s['recommendation_level'] == 'Low']
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

@scholarship_bp.route('/scholarships', methods=['GET'])
def get_all_scholarships():
    """API endpoint to get all scholarships"""
    try:
        scholarships = load_scholarships()
        return jsonify({
            'success': True,
            'total_scholarships': len(scholarships),
            'scholarships': scholarships
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500

@scholarship_bp.route('/scholarships/<scholarship_id>', methods=['GET'])
def get_scholarship_by_id(scholarship_id):
    """API endpoint to get a specific scholarship by ID"""
    try:
        scholarships = load_scholarships()
        scholarship = next((s for s in scholarships if s.get('scholarship_id') == scholarship_id), None)
        
        if scholarship:
            return jsonify({
                'success': True,
                'scholarship': scholarship
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Scholarship not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500
