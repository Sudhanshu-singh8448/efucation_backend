"""
College Finder Service - NoSQL Version
Manages college data and filtering with MongoDB storage
"""

from flask import Blueprint, request, jsonify
import logging
from typing import Dict, List, Any, Optional
from database import get_collection, COLLECTIONS
import pandas as pd
import os

logger = logging.getLogger(__name__)

college_finder_bp = Blueprint('college_finder', __name__)

def load_college_data_to_mongodb():
    """Load college data from CSV to MongoDB"""
    try:
        # Load from CSV
        csv_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'college_list.csv')
        if not os.path.exists(csv_path):
            logger.warning(f"College CSV not found at {csv_path}")
            return
        
        df = pd.read_csv(csv_path)
        df = df.dropna(subset=['College_ID']).reset_index(drop=True)
        
        colleges_collection = get_collection(COLLECTIONS['colleges'])
        
        # Check if data already loaded
        try:
            count = colleges_collection.count_documents({})
            if count > 0:
                logger.info("College data already loaded in MongoDB")
                return
        except Exception as e:
            logger.warning(f"Could not check existing data: {e}")
            # Continue with loading
        
        # Convert DataFrame to list of dictionaries
        colleges = df.to_dict('records')
        
        # Add metadata to each college
        for college in colleges:
            college['_id'] = str(college.get('College_ID', ''))
            college['created_at'] = pd.Timestamp.now()
            college['updated_at'] = pd.Timestamp.now()
        
        # Insert into MongoDB
        if colleges:
            colleges_collection.insert_many(colleges)
            logger.info(f"Loaded {len(colleges)} colleges into MongoDB")
        
    except Exception as e:
        logger.error(f"Error loading college data: {e}")

@college_finder_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        colleges_collection = get_collection(COLLECTIONS['colleges'])
        total_colleges = colleges_collection.count_documents({})
        
        return jsonify({
            'status': 'healthy',
            'service': 'College Finder API',
            'version': '1.0.0',
            'total_colleges': total_colleges,
            'database': 'connected'
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'service': 'College Finder API',
            'error': str(e)
        }), 500

@college_finder_bp.route('/colleges', methods=['GET'])
def get_all_colleges():
    """Get all colleges"""
    try:
        colleges_collection = get_collection(COLLECTIONS['colleges'])
        colleges = list(colleges_collection.find({}, {'_id': 0}))
        
        return jsonify({
            'success': True,
            'total_colleges': len(colleges),
            'colleges': colleges
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting colleges: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get colleges',
            'details': str(e)
        }), 500

@college_finder_bp.route('/search', methods=['GET'])
def search_alias():
    """Alias to maintain compatibility with /api/college/search"""
    return search_colleges()

@college_finder_bp.route('/filter', methods=['POST'])
def filter_alias():
    """Alias to maintain compatibility with /api/college/filter"""
    return filter_colleges()

@college_finder_bp.route('/statistics', methods=['GET'])
def statistics_alias():
    """Basic statistics endpoint"""
    try:
        colleges_collection = get_collection(COLLECTIONS['colleges'])
        total = colleges_collection.count_documents({})
        states = colleges_collection.distinct('State')
        return jsonify({
            'success': True,
            'total_colleges': total,
            'states_count': len(states)
        }), 200
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@college_finder_bp.route('/colleges/filter', methods=['POST'])
def filter_colleges():
    """Filter colleges based on criteria"""
    try:
        filter_criteria = request.get_json() or {}
        
        colleges_collection = get_collection(COLLECTIONS['colleges'])
        
        # Build MongoDB query
        query = {}
        
        # State filter
        if 'state' in filter_criteria and filter_criteria['state']:
            query['State'] = {'$regex': filter_criteria['state'], '$options': 'i'}
        
        # City filter
        if 'city' in filter_criteria and filter_criteria['city']:
            query['City'] = {'$regex': filter_criteria['city'], '$options': 'i'}
        
        # College type filter
        if 'college_type' in filter_criteria and filter_criteria['college_type']:
            query['College_Type'] = {'$regex': filter_criteria['college_type'], '$options': 'i'}
        
        # University filter
        if 'university' in filter_criteria and filter_criteria['university']:
            query['University'] = {'$regex': filter_criteria['university'], '$options': 'i'}
        
        # Course filter
        if 'course' in filter_criteria and filter_criteria['course']:
            query['Courses_Offered'] = {'$regex': filter_criteria['course'], '$options': 'i'}
        
        # Fees range filter
        if 'min_fees' in filter_criteria or 'max_fees' in filter_criteria:
            fees_query = {}
            if 'min_fees' in filter_criteria:
                fees_query['$gte'] = filter_criteria['min_fees']
            if 'max_fees' in filter_criteria:
                fees_query['$lte'] = filter_criteria['max_fees']
            query['Fees'] = fees_query
        
        # Execute query
        colleges = list(colleges_collection.find(query, {'_id': 0}))
        
        return jsonify({
            'success': True,
            'filter_criteria': filter_criteria,
            'total_results': len(colleges),
            'colleges': colleges
        }), 200
        
    except Exception as e:
        logger.error(f"Error filtering colleges: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to filter colleges',
            'details': str(e)
        }), 500

@college_finder_bp.route('/colleges/search', methods=['GET'])
def search_colleges():
    """Search colleges by name or keyword"""
    try:
        search_term = request.args.get('q', '').strip()
        
        if not search_term:
            return jsonify({
                'success': False,
                'error': 'Search term is required'
            }), 400
        
        colleges_collection = get_collection(COLLECTIONS['colleges'])
        
        # Build search query
        query = {
            '$or': [
                {'College_Name': {'$regex': search_term, '$options': 'i'}},
                {'University': {'$regex': search_term, '$options': 'i'}},
                {'City': {'$regex': search_term, '$options': 'i'}},
                {'State': {'$regex': search_term, '$options': 'i'}},
                {'Courses_Offered': {'$regex': search_term, '$options': 'i'}}
            ]
        }
        
        colleges = list(colleges_collection.find(query, {'_id': 0}))
        
        return jsonify({
            'success': True,
            'search_term': search_term,
            'total_results': len(colleges),
            'colleges': colleges
        }), 200
        
    except Exception as e:
        logger.error(f"Error searching colleges: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to search colleges',
            'details': str(e)
        }), 500

@college_finder_bp.route('/colleges/stats', methods=['GET'])
def get_college_stats():
    """Get college statistics"""
    try:
        colleges_collection = get_collection(COLLECTIONS['colleges'])
        
        # Aggregation pipeline for statistics
        pipeline = [
            {
                '$group': {
                    '_id': None,
                    'total_colleges': {'$sum': 1},
                    'states': {'$addToSet': '$State'},
                    'cities': {'$addToSet': '$City'},
                    'college_types': {'$addToSet': '$College_Type'},
                    'universities': {'$addToSet': '$University'},
                    'avg_fees': {'$avg': '$Fees'}
                }
            }
        ]
        
        stats = list(colleges_collection.aggregate(pipeline))
        
        if stats:
            stat = stats[0]
            return jsonify({
                'success': True,
                'statistics': {
                    'total_colleges': stat['total_colleges'],
                    'total_states': len(stat['states']),
                    'total_cities': len(stat['cities']),
                    'total_college_types': len(stat['college_types']),
                    'total_universities': len(stat['universities']),
                    'average_fees': round(stat.get('avg_fees', 0), 2)
                }
            }), 200
        else:
            return jsonify({
                'success': True,
                'statistics': {
                    'total_colleges': 0,
                    'total_states': 0,
                    'total_cities': 0,
                    'total_college_types': 0,
                    'total_universities': 0,
                    'average_fees': 0
                }
            }), 200
            
    except Exception as e:
        logger.error(f"Error getting college stats: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get college statistics',
            'details': str(e)
        }), 500

# Data will be loaded on first request or during app initialization
