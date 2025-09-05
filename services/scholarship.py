"""
Scholarship Service - NoSQL Version
Provides scholarship recommendations based on RIASEC traits with MongoDB storage
"""

from flask import Blueprint, request, jsonify
import logging
from typing import Dict, List, Any, Optional
from database import get_collection, COLLECTIONS
import pandas as pd
import json
import os

logger = logging.getLogger(__name__)

scholarship_bp = Blueprint('scholarship', __name__)

def load_scholarship_data_to_mongodb():
    """Load scholarship data from JSON to MongoDB"""
    try:
        json_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'scholarship.json')
        if not os.path.exists(json_path):
            logger.warning(f"Scholarship JSON not found at {json_path}")
            return
        
        scholarship_collection = get_collection(COLLECTIONS['scholarships'])
        
        # Check if data already loaded
        try:
            count = scholarship_collection.count_documents({})
            if count > 0:
                logger.info("Scholarship data already loaded in MongoDB")
                return
        except Exception as e:
            logger.warning(f"Could not check existing data: {e}")
            # Continue with loading
        
        # Load JSON data
        with open(json_path, 'r') as f:
            scholarships = json.load(f)
        
        # Ensure it's a list
        if isinstance(scholarships, dict):
            scholarships = [scholarships]
        
        # Add metadata to each scholarship
        for scholarship in scholarships:
            scholarship['created_at'] = pd.Timestamp.now()
            scholarship['updated_at'] = pd.Timestamp.now()
            scholarship['views'] = 0
            scholarship['applications'] = 0
        
        if scholarships:
            scholarship_collection.insert_many(scholarships)
            logger.info(f"Loaded {len(scholarships)} scholarships into MongoDB")
        
    except Exception as e:
        logger.error(f"Error loading scholarship data: {e}")

# RIASEC type to scholarship mapping
RIASEC_SCHOLARSHIP_MAPPING = {
    'R': ['Engineering', 'Technology', 'Construction', 'Automotive', 'Manufacturing', 'Agriculture'],
    'I': ['Science', 'Research', 'Mathematics', 'Medicine', 'Laboratory', 'Environmental'],
    'A': ['Art', 'Design', 'Music', 'Creative', 'Media', 'Fashion', 'Film'],
    'S': ['Education', 'Social Work', 'Healthcare', 'Psychology', 'Community Service', 'Counseling'],
    'E': ['Business', 'Entrepreneurship', 'Management', 'Leadership', 'Marketing', 'Finance'],
    'C': ['Accounting', 'Administration', 'Data Management', 'Office', 'Clerical', 'Organization']
}

@scholarship_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        scholarship_collection = get_collection(COLLECTIONS['scholarships'])
        total_scholarships = scholarship_collection.count_documents({})
        
        return jsonify({
            'status': 'healthy',
            'service': 'Scholarship API',
            'version': '1.0.0',
            'total_scholarships': total_scholarships,
            'database': 'connected'
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'service': 'Scholarship API',
            'error': str(e)
        }), 500

@scholarship_bp.route('/recommend', methods=['POST'])
def get_scholarship_recommendations():
    """Get scholarship recommendations based on RIASEC traits"""
    try:
        data = request.get_json() or {}
        
        riasec_types = data.get('riasec_types', '')
        cgpa = data.get('cgpa', 0.0)
        income_level = data.get('income_level', '')
        location = data.get('location', '')
        field_of_study = data.get('field_of_study', '')
        
        if not riasec_types:
            return jsonify({
                'success': False,
                'error': 'RIASEC types are required'
            }), 400
        
        # Parse RIASEC types
        riasec_list = [t.upper() for t in riasec_types if t.upper() in RIASEC_SCHOLARSHIP_MAPPING]
        
        if not riasec_list:
            return jsonify({
                'success': False,
                'error': 'Valid RIASEC types are required (R, I, A, S, E, C)'
            }), 400
        
        scholarship_collection = get_collection(COLLECTIONS['scholarships'])
        
        # Build query based on RIASEC and criteria
        query = {}
        
        # Get relevant fields for RIASEC types
        relevant_fields = []
        for riasec_type in riasec_list:
            relevant_fields.extend(RIASEC_SCHOLARSHIP_MAPPING[riasec_type])
        
        # Query scholarships
        all_scholarships = list(scholarship_collection.find({}, {'_id': 0}))
        
        # Filter and score scholarships
        recommendations = []
        
        for scholarship in all_scholarships:
            score = 0
            
            # Check field relevance
            scholarship_field = scholarship.get('field', '').lower()
            for field in relevant_fields:
                if field.lower() in scholarship_field:
                    score += 30
                    break
            
            # Check CGPA eligibility
            min_cgpa = scholarship.get('min_cgpa', 0.0)
            if isinstance(min_cgpa, (int, float)) and cgpa >= min_cgpa:
                score += 25
            elif cgpa > 0:  # If no min_cgpa specified but user has CGPA
                score += 15
            
            # Check income eligibility
            income_criteria = scholarship.get('income_criteria', '').lower()
            if income_level and income_level.lower() in income_criteria:
                score += 20
            elif not income_criteria:  # No income restriction
                score += 10
            
            # Check location preference
            scholarship_location = scholarship.get('location', '').lower()
            if location and location.lower() in scholarship_location:
                score += 15
            elif 'international' in scholarship_location or 'worldwide' in scholarship_location:
                score += 10
            
            # Check field of study
            if field_of_study:
                if field_of_study.lower() in scholarship_field:
                    score += 20
            
            # Add scholarship with score if it has some relevance
            if score > 10:
                scholarship['relevance_score'] = score
                scholarship['match_reasons'] = []
                
                # Add match reasons
                if any(field.lower() in scholarship_field for field in relevant_fields):
                    scholarship['match_reasons'].append('Field matches your interests')
                
                if cgpa >= scholarship.get('min_cgpa', 0):
                    scholarship['match_reasons'].append('CGPA meets requirement')
                
                if income_level and income_level.lower() in income_criteria:
                    scholarship['match_reasons'].append('Income level eligible')
                
                recommendations.append(scholarship)
        
        # Sort by relevance score
        recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        # Limit to top 10 recommendations
        recommendations = recommendations[:10]
        
        return jsonify({
            'success': True,
            'riasec_types': riasec_types,
            'criteria': {
                'cgpa': cgpa,
                'income_level': income_level,
                'location': location,
                'field_of_study': field_of_study
            },
            'total_recommendations': len(recommendations),
            'recommendations': recommendations
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting scholarship recommendations: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get scholarship recommendations',
            'details': str(e)
        }), 500

@scholarship_bp.route('/fields', methods=['GET'])
def fields_alias():
    """Alias for compatibility (the route already exists)"""
    return get_scholarship_fields()

@scholarship_bp.route('/search', methods=['GET'])
def search_scholarships():
    """Search scholarships by various criteria"""
    try:
        field = request.args.get('field', '').strip()
        min_amount = request.args.get('min_amount', type=float)
        max_amount = request.args.get('max_amount', type=float)
        location = request.args.get('location', '').strip()
        
        scholarship_collection = get_collection(COLLECTIONS['scholarships'])
        
        query = {}
        
        if field:
            query['field'] = {'$regex': field, '$options': 'i'}
        
        if location:
            query['location'] = {'$regex': location, '$options': 'i'}
        
        # Amount filtering (if amount field exists)
        if min_amount is not None or max_amount is not None:
            amount_query = {}
            if min_amount is not None:
                amount_query['$gte'] = min_amount
            if max_amount is not None:
                amount_query['$lte'] = max_amount
            if amount_query:
                query['amount'] = amount_query
        
        scholarships = list(scholarship_collection.find(query, {'_id': 0}))
        
        return jsonify({
            'success': True,
            'search_criteria': {
                'field': field,
                'min_amount': min_amount,
                'max_amount': max_amount,
                'location': location
            },
            'total_results': len(scholarships),
            'scholarships': scholarships
        }), 200
        
    except Exception as e:
        logger.error(f"Error searching scholarships: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to search scholarships',
            'details': str(e)
        }), 500

@scholarship_bp.route('/all', methods=['GET'])
def get_all_scholarships():
    """Get all scholarships"""
    try:
        scholarship_collection = get_collection(COLLECTIONS['scholarships'])
        scholarships = list(scholarship_collection.find({}, {'_id': 0}))
        
        return jsonify({
            'success': True,
            'total_scholarships': len(scholarships),
            'scholarships': scholarships
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting scholarships: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get scholarships',
            'details': str(e)
        }), 500

@scholarship_bp.route('/fields', methods=['GET'])
def get_scholarship_fields():
    """Get all scholarship fields and statistics"""
    try:
        scholarship_collection = get_collection(COLLECTIONS['scholarships'])
        
        # Get distinct fields
        fields = scholarship_collection.distinct('field')
        locations = scholarship_collection.distinct('location')
        
        # Get RIASEC mapping info
        riasec_mapping = RIASEC_SCHOLARSHIP_MAPPING
        
        return jsonify({
            'success': True,
            'fields': fields,
            'locations': locations,
            'riasec_mapping': riasec_mapping
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting scholarship fields: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get scholarship fields',
            'details': str(e)
        }), 500

@scholarship_bp.route('/by-riasec/<riasec_type>', methods=['GET'])
def get_scholarships_by_riasec(riasec_type):
    """Get scholarships for specific RIASEC type"""
    try:
        riasec_type = riasec_type.upper()
        
        if riasec_type not in RIASEC_SCHOLARSHIP_MAPPING:
            return jsonify({
                'success': False,
                'error': f'Invalid RIASEC type. Valid types: {list(RIASEC_SCHOLARSHIP_MAPPING.keys())}'
            }), 400
        
        # Get relevant fields for this RIASEC type
        relevant_fields = RIASEC_SCHOLARSHIP_MAPPING[riasec_type]
        
        scholarship_collection = get_collection(COLLECTIONS['scholarships'])
        
        # Find scholarships that match any of the relevant fields
        scholarships = []
        all_scholarships = list(scholarship_collection.find({}, {'_id': 0}))
        
        for scholarship in all_scholarships:
            scholarship_field = scholarship.get('field', '').lower()
            for field in relevant_fields:
                if field.lower() in scholarship_field:
                    scholarships.append(scholarship)
                    break
        
        return jsonify({
            'success': True,
            'riasec_type': riasec_type,
            'relevant_fields': relevant_fields,
            'total_scholarships': len(scholarships),
            'scholarships': scholarships
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting scholarships by RIASEC: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get scholarships by RIASEC',
            'details': str(e)
        }), 500

# Data will be loaded on first request or during app initialization
