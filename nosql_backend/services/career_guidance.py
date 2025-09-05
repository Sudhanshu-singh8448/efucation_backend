"""
Career Guidance Service - NoSQL Version
Implements RIASEC personality assessment with MongoDB storage
"""

from flask import Blueprint, request, jsonify
import uuid
import logging
from datetime import datetime
from typing import Dict, List, Any
from database import get_collection, COLLECTIONS

logger = logging.getLogger(__name__)

career_guidance_bp = Blueprint('career_guidance', __name__)

# RIASEC Questions Database (24 questions)
QUESTIONS = [
    {"question": "I enjoy working with my hands to build or repair things.", "riasec_type": "realistic"},
    {"question": "I like to analyze data and solve complex problems.", "riasec_type": "investigative"},
    {"question": "I enjoy creating original artwork or creative writing.", "riasec_type": "artistic"},
    {"question": "I like to help others and work in teams.", "riasec_type": "social"},
    {"question": "I enjoy leading projects and convincing others.", "riasec_type": "enterprising"},
    {"question": "I prefer organized, structured work environments.", "riasec_type": "conventional"},
    {"question": "I like working outdoors and with animals.", "riasec_type": "realistic"},
    {"question": "I enjoy conducting research and experiments.", "riasec_type": "investigative"},
    {"question": "I like to write stories, poems, or music.", "riasec_type": "artistic"},
    {"question": "I enjoy teaching and mentoring others.", "riasec_type": "social"},
    {"question": "I like to start new businesses or projects.", "riasec_type": "enterprising"},
    {"question": "I prefer following clear procedures and guidelines.", "riasec_type": "conventional"},
    {"question": "I enjoy physical activities and sports.", "riasec_type": "realistic"},
    {"question": "I like to study scientific concepts and theories.", "riasec_type": "investigative"},
    {"question": "I enjoy photography and visual design.", "riasec_type": "artistic"},
    {"question": "I like to volunteer for community service.", "riasec_type": "social"},
    {"question": "I enjoy sales and business negotiations.", "riasec_type": "enterprising"},
    {"question": "I prefer working with numbers and data entry.", "riasec_type": "conventional"},
    {"question": "I like to work with tools and machinery.", "riasec_type": "realistic"},
    {"question": "I enjoy laboratory work and scientific analysis.", "riasec_type": "investigative"},
    {"question": "I like to perform in front of audiences.", "riasec_type": "artistic"},
    {"question": "I enjoy counseling and helping people with problems.", "riasec_type": "social"},
    {"question": "I like to manage teams and coordinate projects.", "riasec_type": "enterprising"},
    {"question": "I prefer organized filing and record keeping.", "riasec_type": "conventional"}
]

# Career recommendations based on RIASEC types
CAREER_RECOMMENDATIONS = {
    'realistic': ['Engineer', 'Carpenter', 'Mechanic', 'Farmer', 'Pilot', 'Electrician', 'Plumber'],
    'investigative': ['Scientist', 'Doctor', 'Researcher', 'Analyst', 'Psychologist', 'Chemist', 'Programmer'],
    'artistic': ['Artist', 'Writer', 'Designer', 'Musician', 'Actor', 'Photographer', 'Architect'],
    'social': ['Teacher', 'Counselor', 'Social Worker', 'Nurse', 'Therapist', 'Coach', 'Librarian'],
    'enterprising': ['Manager', 'Salesperson', 'Lawyer', 'Entrepreneur', 'Marketing Director', 'CEO', 'Banker'],
    'conventional': ['Accountant', 'Administrator', 'Secretary', 'Bookkeeper', 'Data Analyst', 'Clerk', 'Auditor']
}

@career_guidance_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        sessions_collection = get_collection(COLLECTIONS['career_sessions'])
        active_sessions = sessions_collection.count_documents({"completed": False})
        
        return jsonify({
            'status': 'healthy',
            'service': 'Career Guidance API',
            'version': '1.0.0',
            'database': 'connected',
            'active_sessions': active_sessions,
            'total_questions': len(QUESTIONS),
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'service': 'Career Guidance API',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

# Backward-compatible aliases (to support older clients/tests)
@career_guidance_bp.route('/start-assessment', methods=['POST'])
def start_assessment_alias():
    """Alias for /start-test"""
    return start_test()

@career_guidance_bp.route('/submit-answers', methods=['POST'])
def submit_answers_alias():
    """Alias for /answer"""
    return submit_answer()

@career_guidance_bp.route('/recommendations/<session_id>', methods=['GET'])
def recommendations_alias(session_id):
    """Alias for /results/<session_id>"""
    return get_results(session_id)

@career_guidance_bp.route('/start-test', methods=['POST'])
def start_test():
    """Start a new career assessment session"""
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id', 'anonymous')
        
        session_id = str(uuid.uuid4())
        
        session_document = {
            'session_id': session_id,
            'user_id': user_id,
            'created_at': datetime.utcnow(),
            'completed': False,
            'current_question': 0,
            'scores': {
                'realistic': 0,
                'investigative': 0,
                'artistic': 0,
                'social': 0,
                'enterprising': 0,
                'conventional': 0
            },
            'answers': [],
            'results': None
        }
        
        sessions_collection = get_collection(COLLECTIONS['career_sessions'])
        sessions_collection.insert_one(session_document)
        
        logger.info(f"Started new career session: {session_id}")
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'total_questions': len(QUESTIONS),
            'message': 'Test session started successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Error starting test: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to start test session',
            'details': str(e)
        }), 500

@career_guidance_bp.route('/question/<session_id>', methods=['GET'])
def get_question(session_id):
    """Get the current question for a session"""
    try:
        sessions_collection = get_collection(COLLECTIONS['career_sessions'])
        session = sessions_collection.find_one({'session_id': session_id})
        
        if not session:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        current_question_num = session['current_question']
        
        if current_question_num >= len(QUESTIONS):
            return jsonify({
                'success': False,
                'error': 'No more questions',
                'message': 'All questions have been answered'
            }), 400
        
        question_data = QUESTIONS[current_question_num]
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'question_number': current_question_num + 1,
            'total_questions': len(QUESTIONS),
            'question': question_data['question'],
            'riasec_type': question_data['riasec_type'],
            'progress': (current_question_num / len(QUESTIONS)) * 100
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting question: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get question',
            'details': str(e)
        }), 500

@career_guidance_bp.route('/answer', methods=['POST'])
def submit_answer():
    """Submit answer for current question"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        answer = data.get('answer')
        
        if not session_id or answer is None:
            return jsonify({
                'success': False,
                'error': 'Missing session_id or answer'
            }), 400
        
        if not isinstance(answer, int) or answer < 1 or answer > 5:
            return jsonify({
                'success': False,
                'error': 'Answer must be an integer between 1 and 5'
            }), 400
        
        sessions_collection = get_collection(COLLECTIONS['career_sessions'])
        session = sessions_collection.find_one({'session_id': session_id})
        
        if not session:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        current_question_num = session['current_question']
        
        if current_question_num >= len(QUESTIONS):
            return jsonify({
                'success': False,
                'error': 'All questions have been answered'
            }), 400
        
        question_data = QUESTIONS[current_question_num]
        
        # Create answer document
        answer_doc = {
            'question_number': current_question_num + 1,
            'question': question_data['question'],
            'riasec_type': question_data['riasec_type'],
            'answer_value': answer,
            'timestamp': datetime.utcnow()
        }
        
        # Update session with answer and scores
        riasec_type = question_data['riasec_type']
        update_doc = {
            '$push': {'answers': answer_doc},
            '$inc': {
                f'scores.{riasec_type}': answer,
                'current_question': 1
            }
        }
        
        # Check if test is completed
        if current_question_num + 1 >= len(QUESTIONS):
            # Calculate final results
            new_scores = session['scores'].copy()
            new_scores[riasec_type] += answer
            
            total_score = sum(new_scores.values())
            percentages = {}
            if total_score > 0:
                percentages = {k: round((v / total_score) * 100, 2) for k, v in new_scores.items()}
            
            dominant_type = max(new_scores, key=new_scores.get)
            recommendations = CAREER_RECOMMENDATIONS.get(dominant_type, [])
            
            results = {
                'riasec_scores': new_scores,
                'percentages': percentages,
                'dominant_type': dominant_type,
                'total_score': total_score,
                'career_recommendations': recommendations,
                'completed_at': datetime.utcnow()
            }
            
            update_doc['$set'] = {
                'completed': True,
                'results': results
            }
        
        sessions_collection.update_one(
            {'session_id': session_id},
            update_doc
        )
        
        # Get updated session
        updated_session = sessions_collection.find_one({'session_id': session_id})
        
        if updated_session['completed']:
            return jsonify({
                'success': True,
                'session_id': session_id,
                'completed': True,
                'results': updated_session['results'],
                'message': 'Test completed successfully!'
            }), 200
        else:
            return jsonify({
                'success': True,
                'session_id': session_id,
                'completed': False,
                'next_question': updated_session['current_question'] + 1,
                'progress': (updated_session['current_question'] / len(QUESTIONS)) * 100,
                'message': 'Answer recorded successfully'
            }), 200
            
    except Exception as e:
        logger.error(f"Error submitting answer: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to submit answer',
            'details': str(e)
        }), 500

@career_guidance_bp.route('/results/<session_id>', methods=['GET'])
def get_results(session_id):
    """Get test results for a session"""
    try:
        sessions_collection = get_collection(COLLECTIONS['career_sessions'])
        session = sessions_collection.find_one({'session_id': session_id})
        
        if not session:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        if not session['completed']:
            return jsonify({
                'success': False,
                'error': 'Test not completed yet',
                'current_question': session['current_question'] + 1,
                'total_questions': len(QUESTIONS)
            }), 400
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'results': session['results'],
            'answers': session['answers'],
            'message': 'Results retrieved successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting results: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get results',
            'details': str(e)
        }), 500
