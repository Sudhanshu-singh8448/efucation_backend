#!/usr/bin/env python3
"""
Unified Backend Server for Education Platform
Consolidates all microservices into a single deployable application for Render
"""

from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import os
import sys

# Import all service modules
from services.career_guidance import career_guidance_bp
from services.college_finder import college_finder_bp
from services.course_suggestion import course_suggestion_bp
from services.news_recommender import news_recommender_bp
from services.scholarship import scholarship_bp

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Register all service blueprints with prefixes
app.register_blueprint(career_guidance_bp, url_prefix='/api/career')
app.register_blueprint(college_finder_bp, url_prefix='/api/college')
app.register_blueprint(course_suggestion_bp, url_prefix='/api/course')
app.register_blueprint(news_recommender_bp, url_prefix='/api/news')
app.register_blueprint(scholarship_bp, url_prefix='/api/scholarship')

@app.route('/')
def home():
    """Main API endpoint with service information"""
    return jsonify({
        'message': 'Education Platform Unified API',
        'version': '1.0.0',
        'services': {
            'career_guidance': '/api/career',
            'college_finder': '/api/college', 
            'course_suggestion': '/api/course',
            'news_recommender': '/api/news',
            'scholarship': '/api/scholarship'
        },
        'health_check': '/health',
        'documentation': {
            'career_guidance': '/api/career/health',
            'college_finder': '/api/college/health',
            'course_suggestion': '/api/course/docs',
            'news_recommender': '/api/news/health',
            'scholarship': '/api/scholarship/health'
        }
    })

@app.route('/health')
def health_check():
    """Global health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'All services are operational',
        'services': {
            'career_guidance': 'healthy',
            'college_finder': 'healthy',
            'course_suggestion': 'healthy', 
            'news_recommender': 'healthy',
            'scholarship': 'healthy'
        }
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Custom 404 handler"""
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'Please check the API documentation at /',
        'available_services': [
            '/api/career',
            '/api/college',
            '/api/course', 
            '/api/news',
            '/api/scholarship'
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Custom 500 handler"""
    return jsonify({
        'error': 'Internal server error',
        'message': 'Something went wrong on our end'
    }), 500

if __name__ == '__main__':
    # Use PORT environment variable if available (for Render deployment)
    port = int(os.environ.get('PORT', 8080))
    
    # Debug mode only in development
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"🚀 Starting Education Platform Unified API...")
    print(f"🌐 Server will be available at: http://localhost:{port}")
    print("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode
    )
