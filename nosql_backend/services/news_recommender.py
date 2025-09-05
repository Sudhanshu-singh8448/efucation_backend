"""
News Recommender Service - NoSQL Version
Provides news recommendations based on RIASEC traits with MongoDB storage
"""

from flask import Blueprint, request, jsonify
import logging
from typing import Dict, List, Any, Optional
from database import get_collection, COLLECTIONS
import pandas as pd
import os
import random

logger = logging.getLogger(__name__)

news_recommender_bp = Blueprint('news_recommender', __name__)

def load_news_data_to_mongodb():
    """Load news data from CSV to MongoDB"""
    try:
        csv_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'news_data.csv')
        if not os.path.exists(csv_path):
            logger.warning(f"News CSV not found at {csv_path}")
            return
        
        news_collection = get_collection(COLLECTIONS['news_articles'])
        
        # Check if data already loaded
        try:
            count = news_collection.count_documents({})
            if count > 0:
                logger.info("News data already loaded in MongoDB")
                return
        except Exception as e:
            logger.warning(f"Could not check existing data: {e}")
            # Continue with loading
        
        # Load CSV data
        df = pd.read_csv(csv_path)
        news_articles = df.to_dict('records')
        
        # Add metadata to each article
        for article in news_articles:
            article['created_at'] = pd.Timestamp.now()
            article['updated_at'] = pd.Timestamp.now()
            article['views'] = random.randint(100, 5000)
            article['likes'] = random.randint(10, 500)
        
        if news_articles:
            news_collection.insert_many(news_articles)
            logger.info(f"Loaded {len(news_articles)} news articles into MongoDB")
        
    except Exception as e:
        logger.error(f"Error loading news data: {e}")

# RIASEC type descriptions
RIASEC_DESCRIPTIONS = {
    'R': 'Realistic - Practical, hands-on, mechanical interests',
    'I': 'Investigative - Scientific, analytical, research-oriented',
    'A': 'Artistic - Creative, expressive, artistic pursuits',
    'S': 'Social - Helping others, teaching, counseling',
    'E': 'Enterprising - Leadership, business, entrepreneurial',
    'C': 'Conventional - Organized, detail-oriented, systematic'
}

@news_recommender_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        news_collection = get_collection(COLLECTIONS['news_articles'])
        total_articles = news_collection.count_documents({})
        
        return jsonify({
            'status': 'healthy',
            'service': 'News Recommender API',
            'version': '1.0.0',
            'total_articles': total_articles,
            'database': 'connected'
        }), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'service': 'News Recommender API',
            'error': str(e)
        }), 500

@news_recommender_bp.route('/recommend', methods=['POST'])
def get_news_recommendations():
    """Get news recommendations based on RIASEC traits"""
    try:
        data = request.get_json() or {}
        
        riasec_types = data.get('riasec_types', '')
        num_recommendations = data.get('num_recommendations', 5)
        
        if not riasec_types:
            return jsonify({
                'success': False,
                'error': 'RIASEC types are required'
            }), 400
        
        # Parse RIASEC types
        riasec_list = [t.upper() for t in riasec_types if t.upper() in RIASEC_DESCRIPTIONS]
        
        if not riasec_list:
            return jsonify({
                'success': False,
                'error': 'Valid RIASEC types are required (R, I, A, S, E, C)'
            }), 400
        
        news_collection = get_collection(COLLECTIONS['news_articles'])
        
        # Build query to match RIASEC types
        query = {
            'RIASEC_Type': {'$in': riasec_list}
        }
        
        # Get articles matching RIASEC types
        articles = list(news_collection.find(query, {'_id': 0}))
        
        # If not enough articles for specific types, get some general articles
        if len(articles) < num_recommendations:
            additional_articles = list(news_collection.find(
                {'RIASEC_Type': {'$nin': riasec_list}}, 
                {'_id': 0}
            ).limit(num_recommendations - len(articles)))
            articles.extend(additional_articles)
        
        # Shuffle and limit results
        random.shuffle(articles)
        recommendations = articles[:num_recommendations]
        
        # Add relevance scores
        for article in recommendations:
            if article.get('RIASEC_Type') in riasec_list:
                article['relevance_score'] = 0.9 + random.uniform(0, 0.1)
            else:
                article['relevance_score'] = 0.5 + random.uniform(0, 0.3)
        
        # Sort by relevance score
        recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return jsonify({
            'success': True,
            'riasec_types': riasec_types,
            'total_recommendations': len(recommendations),
            'recommendations': recommendations
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting news recommendations: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get news recommendations',
            'details': str(e)
        }), 500

@news_recommender_bp.route('/articles/search', methods=['GET'])
def articles_search_alias():
    """Alias to maintain compatibility with /api/news/articles/search"""
    return search_articles()

@news_recommender_bp.route('/news-by-type/<riasec_type>', methods=['GET'])
def get_news_by_type(riasec_type):
    """Get news articles by specific RIASEC type"""
    try:
        riasec_type = riasec_type.upper()
        
        if riasec_type not in RIASEC_DESCRIPTIONS:
            return jsonify({
                'success': False,
                'error': f'Invalid RIASEC type. Valid types: {list(RIASEC_DESCRIPTIONS.keys())}'
            }), 400
        
        news_collection = get_collection(COLLECTIONS['news_articles'])
        
        # Get articles for specific RIASEC type
        articles = list(news_collection.find(
            {'RIASEC_Type': riasec_type},
            {'_id': 0}
        ))
        
        return jsonify({
            'success': True,
            'riasec_type': riasec_type,
            'description': RIASEC_DESCRIPTIONS[riasec_type],
            'total_articles': len(articles),
            'articles': articles
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting news by type: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get news by type',
            'details': str(e)
        }), 500

@news_recommender_bp.route('/articles', methods=['GET'])
def get_all_articles():
    """Get all news articles"""
    try:
        news_collection = get_collection(COLLECTIONS['news_articles'])
        articles = list(news_collection.find({}, {'_id': 0}))
        
        return jsonify({
            'success': True,
            'total_articles': len(articles),
            'articles': articles
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting articles: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get articles',
            'details': str(e)
        }), 500

@news_recommender_bp.route('/articles/search', methods=['GET'])
def search_articles():
    """Search news articles by keyword"""
    try:
        search_term = request.args.get('q', '').strip()
        
        if not search_term:
            return jsonify({
                'success': False,
                'error': 'Search term is required'
            }), 400
        
        news_collection = get_collection(COLLECTIONS['news_articles'])
        
        query = {
            '$or': [
                {'Title': {'$regex': search_term, '$options': 'i'}},
                {'Summary': {'$regex': search_term, '$options': 'i'}},
                {'Content': {'$regex': search_term, '$options': 'i'}},
                {'Category': {'$regex': search_term, '$options': 'i'}}
            ]
        }
        
        articles = list(news_collection.find(query, {'_id': 0}))
        
        return jsonify({
            'success': True,
            'search_term': search_term,
            'total_results': len(articles),
            'articles': articles
        }), 200
        
    except Exception as e:
        logger.error(f"Error searching articles: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to search articles',
            'details': str(e)
        }), 500

@news_recommender_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all news categories"""
    try:
        news_collection = get_collection(COLLECTIONS['news_articles'])
        
        # Get distinct categories
        categories = news_collection.distinct('Category')
        riasec_types = news_collection.distinct('RIASEC_Type')
        
        return jsonify({
            'success': True,
            'categories': categories,
            'riasec_types': riasec_types,
            'riasec_descriptions': RIASEC_DESCRIPTIONS
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting categories: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to get categories',
            'details': str(e)
        }), 500

# Data will be loaded on first request or during app initialization
