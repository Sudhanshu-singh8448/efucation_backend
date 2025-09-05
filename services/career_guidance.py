"""
Career Guidance Service
Converted from standalone Flask app to Blueprint for unified backend
"""

from flask import Blueprint, request, jsonify
import uuid
import logging
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

# Create Blueprint
career_guidance_bp = Blueprint('career_guidance', __name__)

# In-memory session storage
sessions = {}

@career_guidance_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Career Guidance API',
        'version': '1.0.0',
        'active_sessions': len(sessions),
        'timestamp': datetime.now().isoformat()
    }), 200

@career_guidance_bp.route('/start-test', methods=['POST'])
def start_test():
    """Start a new test session"""
    try:
        session_id = str(uuid.uuid4())
        
        sessions[session_id] = {
            'session_id': session_id,
            'created_at': datetime.now(),
            'current_question': 0,
            'answers': [],
            'riasec_scores': {
                'realistic': 0,
                'investigative': 0,
                'artistic': 0,
                'social': 0,
                'enterprising': 0,
                'conventional': 0
            },
            'completed': False
        }
        
        logger.info(f"Started new test session: {session_id}")
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'total_questions': 24,
            'message': 'Test session started successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Error starting test: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to start test session',
            'details': str(e)
        }), 500

@career_guidance_bp.route('/question/<session_id>', methods=['GET'])
def get_question(session_id):
    """Get the next question"""
    try:
        if session_id not in sessions:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        session_data = sessions[session_id]
        current_question_num = session_data['current_question']
        
        # Sample questions for testing (in production, import from models/question_bank.py)
        questions = [
            {"question": "I enjoy working with my hands to build or repair things.", "riasec_type": "Realistic"},
            {"question": "I like to analyze data and solve complex problems.", "riasec_type": "Investigative"},
            {"question": "I enjoy creating original artwork or creative writing.", "riasec_type": "Artistic"},
            {"question": "I like to help others and work in teams.", "riasec_type": "Social"},
            {"question": "I enjoy leading projects and convincing others.", "riasec_type": "Enterprising"},
            {"question": "I prefer organized, structured work environments.", "riasec_type": "Conventional"},
            {"question": "I like working outdoors and with animals.", "riasec_type": "Realistic"},
            {"question": "I enjoy conducting research and experiments.", "riasec_type": "Investigative"},
            {"question": "I like to write stories, poems, or music.", "riasec_type": "Artistic"},
            {"question": "I enjoy teaching and mentoring others.", "riasec_type": "Social"},
            {"question": "I like to start new businesses or projects.", "riasec_type": "Enterprising"},
            {"question": "I prefer following clear procedures and guidelines.", "riasec_type": "Conventional"},
            {"question": "I enjoy physical activities and sports.", "riasec_type": "Realistic"},
            {"question": "I like to study scientific concepts and theories.", "riasec_type": "Investigative"},
            {"question": "I enjoy photography and visual design.", "riasec_type": "Artistic"},
            {"question": "I like to volunteer for community service.", "riasec_type": "Social"},
            {"question": "I enjoy sales and business negotiations.", "riasec_type": "Enterprising"},
            {"question": "I prefer working with numbers and data entry.", "riasec_type": "Conventional"},
            {"question": "I like to work with tools and machinery.", "riasec_type": "Realistic"},
            {"question": "I enjoy laboratory work and scientific analysis.", "riasec_type": "Investigative"},
            {"question": "I like to perform in front of audiences.", "riasec_type": "Artistic"},
            {"question": "I enjoy counseling and helping people with problems.", "riasec_type": "Social"},
            {"question": "I like to manage teams and coordinate projects.", "riasec_type": "Enterprising"},
            {"question": "I prefer organized filing and record keeping.", "riasec_type": "Conventional"}
        ]
        
        if current_question_num >= len(questions):
            return jsonify({
                'success': False,
                'error': 'No more questions',
                'message': 'All questions have been answered'
            }), 400
        
        question_data = questions[current_question_num]
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'question_number': current_question_num + 1,
            'total_questions': len(questions),
            'question': question_data['question'],
            'riasec_type': question_data['riasec_type'],
            'progress': ((current_question_num) / len(questions)) * 100
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting question: {str(e)}")
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
        answer = data.get('answer')  # 1-5 scale
        
        if not session_id or answer is None:
            return jsonify({
                'success': False,
                'error': 'Missing session_id or answer'
            }), 400
        
        if session_id not in sessions:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        session_data = sessions[session_id]
        current_question_num = session_data['current_question']
        
        # Get question type to update RIASEC scores
        questions = [
            {"question": "I enjoy working with my hands to build or repair things.", "riasec_type": "Realistic"},
            {"question": "I like to analyze data and solve complex problems.", "riasec_type": "Investigative"},
            {"question": "I enjoy creating original artwork or creative writing.", "riasec_type": "Artistic"},
            {"question": "I like to help others and work in teams.", "riasec_type": "Social"},
            {"question": "I enjoy leading projects and convincing others.", "riasec_type": "Enterprising"},
            {"question": "I prefer organized, structured work environments.", "riasec_type": "Conventional"},
            {"question": "I like working outdoors and with animals.", "riasec_type": "Realistic"},
            {"question": "I enjoy conducting research and experiments.", "riasec_type": "Investigative"},
            {"question": "I like to write stories, poems, or music.", "riasec_type": "Artistic"},
            {"question": "I enjoy teaching and mentoring others.", "riasec_type": "Social"},
            {"question": "I like to start new businesses or projects.", "riasec_type": "Enterprising"},
            {"question": "I prefer following clear procedures and guidelines.", "riasec_type": "Conventional"},
            {"question": "I enjoy physical activities and sports.", "riasec_type": "Realistic"},
            {"question": "I like to study scientific concepts and theories.", "riasec_type": "Investigative"},
            {"question": "I enjoy photography and visual design.", "riasec_type": "Artistic"},
            {"question": "I like to volunteer for community service.", "riasec_type": "Social"},
            {"question": "I enjoy sales and business negotiations.", "riasec_type": "Enterprising"},
            {"question": "I prefer working with numbers and data entry.", "riasec_type": "Conventional"},
            {"question": "I like to work with tools and machinery.", "riasec_type": "Realistic"},
            {"question": "I enjoy laboratory work and scientific analysis.", "riasec_type": "Investigative"},
            {"question": "I like to perform in front of audiences.", "riasec_type": "Artistic"},
            {"question": "I enjoy counseling and helping people with problems.", "riasec_type": "Social"},
            {"question": "I like to manage teams and coordinate projects.", "riasec_type": "Enterprising"},
            {"question": "I prefer organized filing and record keeping.", "riasec_type": "Conventional"}
        ]
        
        if current_question_num < len(questions):
            question_type = questions[current_question_num]['riasec_type'].lower()
            
            # Update RIASEC score
            session_data['riasec_scores'][question_type] += int(answer)
            
            # Store the answer
            session_data['answers'].append({
                'question_number': current_question_num + 1,
                'answer': answer,
                'riasec_type': question_type
            })
            
            # Move to next question
            session_data['current_question'] += 1
            
            # Check if test is completed
            if session_data['current_question'] >= len(questions):
                session_data['completed'] = True
                
                # Calculate final results
                total_score = sum(session_data['riasec_scores'].values())
                percentages = {}
                
                for riasec_type, score in session_data['riasec_scores'].items():
                    percentages[riasec_type] = round((score / total_score) * 100, 2) if total_score > 0 else 0
                
                # Find dominant personality type
                dominant_type = max(session_data['riasec_scores'], key=session_data['riasec_scores'].get)
                
                return jsonify({
                    'success': True,
                    'session_id': session_id,
                    'completed': True,
                    'results': {
                        'riasec_scores': session_data['riasec_scores'],
                        'percentages': percentages,
                        'dominant_type': dominant_type,
                        'total_questions': len(questions),
                        'total_score': total_score
                    },
                    'message': 'Test completed successfully!'
                }), 200
            else:
                return jsonify({
                    'success': True,
                    'session_id': session_id,
                    'completed': False,
                    'next_question': session_data['current_question'] + 1,
                    'progress': (session_data['current_question'] / len(questions)) * 100,
                    'message': 'Answer recorded successfully'
                }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'Test already completed'
            }), 400
            
    except Exception as e:
        logger.error(f"Error submitting answer: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to submit answer',
            'details': str(e)
        }), 500

@career_guidance_bp.route('/results/<session_id>', methods=['GET'])
def get_results(session_id):
    """Get test results for a session"""
    try:
        if session_id not in sessions:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404
        
        session_data = sessions[session_id]
        
        if not session_data['completed']:
            return jsonify({
                'success': False,
                'error': 'Test not completed yet'
            }), 400
        
        # Calculate results
        total_score = sum(session_data['riasec_scores'].values())
        percentages = {}
        
        for riasec_type, score in session_data['riasec_scores'].items():
            percentages[riasec_type] = round((score / total_score) * 100, 2) if total_score > 0 else 0
        
        dominant_type = max(session_data['riasec_scores'], key=session_data['riasec_scores'].get)
        
        # Career recommendations based on dominant type
        career_recommendations = {
            'realistic': ['Engineer', 'Carpenter', 'Mechanic', 'Farmer', 'Pilot'],
            'investigative': ['Scientist', 'Doctor', 'Researcher', 'Analyst', 'Psychologist'],
            'artistic': ['Artist', 'Writer', 'Designer', 'Musician', 'Actor'],
            'social': ['Teacher', 'Counselor', 'Social Worker', 'Nurse', 'Therapist'],
            'enterprising': ['Manager', 'Salesperson', 'Entrepreneur', 'Lawyer', 'Executive'],
            'conventional': ['Accountant', 'Administrator', 'Data Entry Clerk', 'Bank Teller', 'Secretary']
        }
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'results': {
                'riasec_scores': session_data['riasec_scores'],
                'percentages': percentages,
                'dominant_type': dominant_type,
                'career_recommendations': career_recommendations.get(dominant_type, []),
                'created_at': session_data['created_at'].isoformat(),
                'total_questions': len(session_data['answers'])
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting results: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to get results',
            'details': str(e)
        }), 500
