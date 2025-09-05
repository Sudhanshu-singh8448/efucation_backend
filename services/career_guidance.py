"""
Career Guidance Service with PostgreSQL Database
Converted from standalone Flask app to Blueprint for unified backend
"""

from flask import Blueprint, request, jsonify
import uuid
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal, CareerSession, CareerAnswer, get_db

# Configure logging
logger = logging.getLogger(__name__)

# Create Blueprint
career_guidance_bp = Blueprint('career_guidance', __name__)

# RIASEC Questions Database
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
    'artistic': ['Artist', 'Writer', 'Designer', 'Musician', 'Actor', 'Photographer', 'Graphic Designer'],
    'social': ['Teacher', 'Counselor', 'Social Worker', 'Nurse', 'Therapist', 'Psychologist', 'Coach'],
    'enterprising': ['Manager', 'Salesperson', 'Entrepreneur', 'Lawyer', 'Executive', 'Business Owner', 'Consultant'],
    'conventional': ['Accountant', 'Administrator', 'Data Entry Clerk', 'Bank Teller', 'Secretary', 'Office Manager']
}

@career_guidance_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        db = SessionLocal()
        active_sessions = db.query(CareerSession).filter(CareerSession.completed == 0).count()
        db.close()

        return jsonify({
            'status': 'healthy',
            'service': 'Career Guidance API',
            'version': '1.0.0',
            'active_sessions': active_sessions,
            'database': 'connected',
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'service': 'Career Guidance API',
            'error': 'Database connection failed',
            'timestamp': datetime.now().isoformat()
        }), 500

@career_guidance_bp.route('/start-test', methods=['POST'])
def start_test():
    """Start a new test session"""
    try:
        db = SessionLocal()
        session_id = str(uuid.uuid4())

        # Create new session in database
        new_session = CareerSession(
            id=session_id,
            created_at=datetime.utcnow(),
            completed=0,
            current_question=0,
            realistic_score=0,
            investigative_score=0,
            artistic_score=0,
            social_score=0,
            enterprising_score=0,
            conventional_score=0
        )

        db.add(new_session)
        db.commit()
        db.close()

        logger.info(f"Started new test session: {session_id}")

        return jsonify({
            'success': True,
            'session_id': session_id,
            'total_questions': len(QUESTIONS),
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
        db = SessionLocal()
        session_data = db.query(CareerSession).filter(CareerSession.session_id == session_id).first()
        db.close()

        if not session_data:
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404

        current_question_num = session_data.current_question

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
            'progress': ((current_question_num) / len(QUESTIONS)) * 100
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

        db = SessionLocal()
        session_data = db.query(CareerSession).filter(CareerSession.session_id == session_id).first()

        if not session_data:
            db.close()
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404

        current_question_num = session_data.current_question

        if current_question_num < len(QUESTIONS):
            question_data = QUESTIONS[current_question_num]

            # Store the answer in database
            new_answer = CareerAnswer(
                session_id=session_id,
                question_number=current_question_num + 1,
                question_text=question_data['question'],
                riasec_type=question_data['riasec_type'],
                answer_value=int(answer)
            )
            db.add(new_answer)

            # Update RIASEC score and move to next question
            riasec_type = question_data['riasec_type']
            if riasec_type == 'realistic':
                session_data.realistic_score += int(answer)
            elif riasec_type == 'investigative':
                session_data.investigative_score += int(answer)
            elif riasec_type == 'artistic':
                session_data.artistic_score += int(answer)
            elif riasec_type == 'social':
                session_data.social_score += int(answer)
            elif riasec_type == 'enterprising':
                session_data.enterprising_score += int(answer)
            elif riasec_type == 'conventional':
                session_data.conventional_score += int(answer)

            session_data.current_question += 1

            # Check if test is completed
            if session_data.current_question >= len(QUESTIONS):
                session_data.completed = 1

                # Calculate final results
                total_score = (session_data.realistic_score + session_data.investigative_score +
                             session_data.artistic_score + session_data.social_score +
                             session_data.enterprising_score + session_data.conventional_score)

                percentages = {}
                if total_score > 0:
                    percentages = {
                        'realistic': round((session_data.realistic_score / total_score) * 100, 2),
                        'investigative': round((session_data.investigative_score / total_score) * 100, 2),
                        'artistic': round((session_data.artistic_score / total_score) * 100, 2),
                        'social': round((session_data.social_score / total_score) * 100, 2),
                        'enterprising': round((session_data.enterprising_score / total_score) * 100, 2),
                        'conventional': round((session_data.conventional_score / total_score) * 100, 2)
                    }

                # Find dominant personality type
                scores = {
                    'realistic': session_data.realistic_score,
                    'investigative': session_data.investigative_score,
                    'artistic': session_data.artistic_score,
                    'social': session_data.social_score,
                    'enterprising': session_data.enterprising_score,
                    'conventional': session_data.conventional_score
                }
                dominant_type = max(scores, key=scores.get)

                db.commit()
                db.close()

                return jsonify({
                    'success': True,
                    'session_id': session_id,
                    'completed': True,
                    'results': {
                        'riasec_scores': scores,
                        'percentages': percentages,
                        'dominant_type': dominant_type,
                        'total_questions': len(QUESTIONS),
                        'total_score': total_score
                    },
                    'message': 'Test completed successfully!'
                }), 200
            else:
                db.commit()
                db.close()

                return jsonify({
                    'success': True,
                    'session_id': session_id,
                    'completed': False,
                    'next_question': session_data.current_question + 1,
                    'progress': (session_data.current_question / len(QUESTIONS)) * 100,
                    'message': 'Answer recorded successfully'
                }), 200
        else:
            db.close()
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
        db = SessionLocal()
        session_data = db.query(CareerSession).filter(CareerSession.session_id == session_id).first()

        if not session_data:
            db.close()
            return jsonify({
                'success': False,
                'error': 'Session not found'
            }), 404

        if session_data.completed == 0:
            db.close()
            return jsonify({
                'success': False,
                'error': 'Test not completed yet'
            }), 400

        # Get all answers for this session
        answers = db.query(CareerAnswer).filter(CareerAnswer.session_id == session_id).all()
        db.close()

        # Calculate results
        total_score = (session_data.realistic_score + session_data.investigative_score +
                     session_data.artistic_score + session_data.social_score +
                     session_data.enterprising_score + session_data.conventional_score)

        percentages = {}
        if total_score > 0:
            percentages = {
                'realistic': round((session_data.realistic_score / total_score) * 100, 2),
                'investigative': round((session_data.investigative_score / total_score) * 100, 2),
                'artistic': round((session_data.artistic_score / total_score) * 100, 2),
                'social': round((session_data.social_score / total_score) * 100, 2),
                'enterprising': round((session_data.enterprising_score / total_score) * 100, 2),
                'conventional': round((session_data.conventional_score / total_score) * 100, 2)
            }

        scores = {
            'realistic': session_data.realistic_score,
            'investigative': session_data.investigative_score,
            'artistic': session_data.artistic_score,
            'social': session_data.social_score,
            'enterprising': session_data.enterprising_score,
            'conventional': session_data.conventional_score
        }

        dominant_type = max(scores, key=scores.get)

        return jsonify({
            'success': True,
            'session_id': session_id,
            'results': {
                'riasec_scores': scores,
                'percentages': percentages,
                'dominant_type': dominant_type,
                'career_recommendations': CAREER_RECOMMENDATIONS.get(dominant_type, []),
                'created_at': session_data.created_at.isoformat(),
                'total_questions': len(answers)
            }
        }), 200

    except Exception as e:
        logger.error(f"Error getting results: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to get results',
            'details': str(e)
        }), 500
