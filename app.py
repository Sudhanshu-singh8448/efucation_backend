"""
Unified Education Backend - NoSQL Version
Main Flask application with MongoDB integration
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import os
from dotenv import load_dotenv

# Import MongoDB database connection
from database import init_database, get_database, close_database

# Import service blueprints
from services.career_guidance import career_guidance_bp
from services.college_finder import college_finder_bp
from services.course_suggestion import course_suggestion_bp
from services.news_recommender import news_recommender_bp
from services.scholarship import scholarship_bp

# Load environment variables
load_dotenv()

# Configure logging for production and development
def configure_logging():
    """Configure logging based on environment"""
    flask_env = os.getenv('FLASK_ENV', 'development')
    log_level = logging.DEBUG if flask_env == 'development' else logging.INFO
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Configure logging
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    handlers = [logging.StreamHandler()]
    
    # Add file handler for production
    if flask_env == 'production':
        handlers.append(logging.FileHandler('logs/app.log'))
    else:
        handlers.append(logging.FileHandler('app.log'))
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=handlers
    )

# Configure logging
configure_logging()

logger = logging.getLogger(__name__)

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Configure app
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Enable CORS for all domains and routes
    CORS(app, origins="*", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    
    # Initialize database
    init_database()
    
    # Data is now loaded via a separate migration script
    # initialize_data()
    
    # Register service blueprints with URL prefixes
    app.register_blueprint(career_guidance_bp, url_prefix='/api/career')
    app.register_blueprint(college_finder_bp, url_prefix='/api/college')
    app.register_blueprint(course_suggestion_bp, url_prefix='/api/course')
    app.register_blueprint(news_recommender_bp, url_prefix='/api/news')
    app.register_blueprint(scholarship_bp, url_prefix='/api/scholarship')
    
    return app

def initialize_data():
    """Initialize all data collections"""
    try:
        # Import data loading functions
        from services.college_finder import load_college_data_to_mongodb
        from services.course_suggestion import load_course_data_to_mongodb
        from services.news_recommender import load_news_data_to_mongodb
        from services.scholarship import load_scholarship_data_to_mongodb
        
        logger.info("Initializing data collections...")
        
        # Load data for each service
        load_college_data_to_mongodb()
        load_course_data_to_mongodb()
        load_news_data_to_mongodb()
        load_scholarship_data_to_mongodb()
        
        logger.info("Data initialization completed")
        
    except Exception as e:
        logger.error(f"Error during data initialization: {e}")
        # Don't fail the app startup, just log the error

# Create Flask app
app = create_app()

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'message': 'Welcome to Unified Education Backend - NoSQL Version',
        'version': '2.0.0',
        'status': 'running',
        'database': 'MongoDB Atlas',
        'services': [
            'Career Guidance',
            'College Finder',
            'Course Suggestions',
            'News Recommender',
            'Scholarship'
        ]
    }), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    """Global health check endpoint"""
    try:
        db = get_database()
        
        # Test database connection
        server_info = db.client.server_info()
        
        return jsonify({
            'status': 'healthy',
            'message': 'All systems operational',
            'version': '2.0.0',
            'database': {
                'status': 'connected',
                'type': 'MongoDB Atlas',
                'server_version': server_info.get('version', 'unknown')
            },
            'services': {
                'career_guidance': '/api/career/health',
                'college_finder': '/api/college/health',
                'course_suggestion': '/api/course/health',
                'news_recommender': '/api/news/health',
                'scholarship': '/api/scholarship/health'
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'message': 'System experiencing issues',
            'error': str(e)
        }), 500

@app.route('/api/services', methods=['GET'])
def list_services():
    """List all available services and their endpoints"""
    return jsonify({
        'success': True,
        'services': {
            'career_guidance': {
                'name': 'Career Guidance Service',
                'base_url': '/api/career',
                'endpoints': {
                    'health': 'GET /api/career/health',
                    'start_assessment': 'POST /api/career/start-assessment',
                    'submit_answers': 'POST /api/career/submit-answers',
                    'get_recommendations': 'GET /api/career/recommendations/<session_id>'
                }
            },
            'college_finder': {
                'name': 'College Finder Service',
                'base_url': '/api/college',
                'endpoints': {
                    'health': 'GET /api/college/health',
                    'search': 'GET /api/college/search',
                    'filter': 'POST /api/college/filter',
                    'statistics': 'GET /api/college/statistics'
                }
            },
            'course_suggestion': {
                'name': 'Course Suggestion Service',
                'base_url': '/api/course',
                'endpoints': {
                    'health': 'GET /api/course/health',
                    'recommend': 'POST /api/course/recommend',
                    'search': 'GET /api/course/search'
                }
            },
            'news_recommender': {
                'name': 'News Recommender Service',
                'base_url': '/api/news',
                'endpoints': {
                    'health': 'GET /api/news/health',
                    'recommend': 'POST /api/news/recommend',
                    'by_type': 'GET /api/news/news-by-type/<riasec_type>',
                    'search': 'GET /api/news/articles/search',
                    'all_articles': 'GET /api/news/articles',
                    'categories': 'GET /api/news/categories'
                }
            },
            'scholarship': {
                'name': 'Scholarship Service',
                'base_url': '/api/scholarship',
                'endpoints': {
                    'health': 'GET /api/scholarship/health',
                    'recommend': 'POST /api/scholarship/recommend',
                    'search': 'GET /api/scholarship/search',
                    'all': 'GET /api/scholarship/all',
                    'by_riasec': 'GET /api/scholarship/by-riasec/<riasec_type>',
                    'fields': 'GET /api/scholarship/fields'
                }
            }
        }
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found',
        'message': 'The requested endpoint does not exist',
        'available_services': '/api/services'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

@app.errorhandler(400)
def bad_request(error):
    """Handle 400 errors"""
    return jsonify({
        'success': False,
        'error': 'Bad request',
        'message': 'The request was invalid or malformed'
    }), 400

@app.before_request
def before_request():
    """Log incoming requests"""
    if request.endpoint != 'health_check':  # Don't log health checks
        logger.info(f"{request.method} {request.path} from {request.remote_addr}")

@app.after_request
def after_request(response):
    """Log outgoing responses"""
    if request.endpoint != 'health_check':  # Don't log health check responses
        logger.info(f"Response: {response.status_code} for {request.method} {request.path}")
    return response

@app.teardown_appcontext
def close_db(error):
    """Close database connection on app context teardown"""
    if error:
        logger.error(f"App context error: {error}")

if __name__ == '__main__':
    try:
        port = int(os.getenv('PORT', 10000))
        host = os.getenv('HOST', '0.0.0.0')
        debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
        flask_env = os.getenv('FLASK_ENV', 'development')
        
        logger.info(f"Starting Unified Education Backend - NoSQL Version")
        logger.info(f"Environment: {flask_env}")
        logger.info(f"Server running on {host}:{port}")
        logger.info(f"Debug mode: {debug}")
        
        if flask_env == 'production':
            # Production mode - use gunicorn settings
            import gunicorn.app.wsgiapp as wsgi
            app.run(host=host, port=port, debug=False, threaded=True)
        else:
            # Development mode
            app.run(host=host, port=port, debug=debug)
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
    finally:
        close_database()
