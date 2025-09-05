"""
News Recommender Service
Converted from standalone Flask app to Blueprint for unified backend
"""

from flask import Blueprint, request, jsonify
import pandas as pd
import random
import os
from typing import List, Dict, Any

# Create Blueprint
news_recommender_bp = Blueprint('news_recommender', __name__)

class NewsRecommender:
    def __init__(self, csv_file_path: str):
        """Initialize the recommender with news data"""
        try:
            self.df = pd.read_csv(csv_file_path)
            self.riasec_types = ['R', 'I', 'A', 'S', 'E', 'C']
            
            # RIASEC type descriptions for reference
            self.riasec_descriptions = {
                'R': 'Realistic - Practical, hands-on, mechanical interests',
                'I': 'Investigative - Scientific, analytical, research-oriented',
                'A': 'Artistic - Creative, expressive, artistic pursuits',
                'S': 'Social - Helping others, teaching, counseling',
                'E': 'Enterprising - Leadership, business, entrepreneurial',
                'C': 'Conventional - Organized, detail-oriented, systematic'
            }
        except FileNotFoundError:
            print(f"Warning: News data file {csv_file_path} not found!")
            self.df = pd.DataFrame()
            self.riasec_types = ['R', 'I', 'A', 'S', 'E', 'C']
            self.riasec_descriptions = {}
    
    def get_recommendations(self, riasec_input: str, num_recommendations: int = 5) -> List[Dict[str, Any]]:
        """
        Get news recommendations based on RIASEC personality type(s)
        
        Args:
            riasec_input: String containing RIASEC types (e.g., 'I', 'IE', 'SIA')
            num_recommendations: Number of news articles to recommend
            
        Returns:
            List of recommended news articles
        """
        if self.df.empty:
            return []
            
        # Validate RIASEC input
        riasec_types = list(riasec_input.upper())
        valid_types = [t for t in riasec_types if t in self.riasec_types]
        
        if not valid_types:
            return []
        
        # Filter news based on RIASEC types
        matching_news = self.df[self.df['RIASEC'].isin(valid_types)]
        
        if matching_news.empty:
            # If no exact matches, return random sample from all news
            matching_news = self.df
        
        # Sample random articles if we have more than requested
        if len(matching_news) > num_recommendations:
            recommended_articles = matching_news.sample(n=num_recommendations)
        else:
            recommended_articles = matching_news
        
        # Convert to list of dictionaries
        recommendations = []
        for _, article in recommended_articles.iterrows():
            recommendations.append({
                'news_id': article['News_ID'],
                'headline': article['Headline'],
                'description': article['Description'],
                'riasec_type': article['RIASEC'],
                'riasec_description': self.riasec_descriptions.get(article['RIASEC'], '')
            })
        
        return recommendations
    
    def get_all_riasec_types(self) -> Dict[str, str]:
        """Get all RIASEC types and their descriptions"""
        return self.riasec_descriptions
    
    def get_news_by_type(self, riasec_type: str) -> List[Dict[str, Any]]:
        """Get all news articles for a specific RIASEC type"""
        if self.df.empty or riasec_type.upper() not in self.riasec_types:
            return []
        
        filtered_news = self.df[self.df['RIASEC'] == riasec_type.upper()]
        
        articles = []
        for _, article in filtered_news.iterrows():
            articles.append({
                'news_id': article['News_ID'],
                'headline': article['Headline'],
                'description': article['Description'],
                'riasec_type': article['RIASEC']
            })
        
        return articles

# Initialize the recommender
def load_news_data():
    """Load news data from CSV file"""
    # Try to load from the data directory
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'news_data.csv')
    if not os.path.exists(csv_path):
        # Fallback to original location
        csv_path = '/Users/sudhanshukumar/project/backend/news_recomender_backend/news_data.csv'
    
    return csv_path

news_data_path = load_news_data()
recommender = NewsRecommender(news_data_path)

@news_recommender_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'News Recommender API',
        'version': '1.0.0',
        'total_articles': len(recommender.df) if not recommender.df.empty else 0
    }), 200

@news_recommender_bp.route('/', methods=['GET'])
def home():
    """API information endpoint"""
    return jsonify({
        'message': 'RIASEC-based News Recommendation API',
        'version': '1.0',
        'endpoints': {
            '/': 'GET - API information',
            '/recommend': 'POST - Get news recommendations based on RIASEC types',
            '/riasec-types': 'GET - Get all RIASEC types and descriptions',
            '/news-by-type/<type>': 'GET - Get all news for a specific RIASEC type',
            '/stats': 'GET - Get dataset statistics'
        },
        'riasec_types': recommender.get_all_riasec_types()
    })

@news_recommender_bp.route('/recommend', methods=['POST'])
def recommend_news():
    """
    Recommend news based on RIASEC personality types
    
    Expected JSON payload:
    {
        "riasec_types": "IE",  // String containing RIASEC types
        "num_recommendations": 5  // Optional: number of recommendations (default: 5)
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'riasec_types' not in data:
            return jsonify({
                'error': 'Missing required field: riasec_types',
                'example': {
                    'riasec_types': 'IE',
                    'num_recommendations': 5
                }
            }), 400
        
        riasec_input = data['riasec_types']
        num_recommendations = data.get('num_recommendations', 5)
        
        # Validate input
        if not isinstance(riasec_input, str) or not riasec_input:
            return jsonify({
                'error': 'riasec_types must be a non-empty string'
            }), 400
        
        if not isinstance(num_recommendations, int) or num_recommendations < 1:
            return jsonify({
                'error': 'num_recommendations must be a positive integer'
            }), 400
        
        # Get recommendations
        recommendations = recommender.get_recommendations(riasec_input, num_recommendations)
        
        return jsonify({
            'riasec_input': riasec_input.upper(),
            'num_recommendations': len(recommendations),
            'recommendations': recommendations
        })
    
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}'
        }), 500

@news_recommender_bp.route('/riasec-types', methods=['GET'])
def get_riasec_types():
    """Get all RIASEC types and their descriptions"""
    return jsonify({
        'riasec_types': recommender.get_all_riasec_types()
    })

@news_recommender_bp.route('/news-by-type/<riasec_type>', methods=['GET'])
def get_news_by_type(riasec_type):
    """Get all news articles for a specific RIASEC type"""
    articles = recommender.get_news_by_type(riasec_type)
    
    if not articles:
        return jsonify({
            'error': f'No news found for RIASEC type: {riasec_type}',
            'valid_types': list(recommender.riasec_types)
        }), 404
    
    return jsonify({
        'riasec_type': riasec_type.upper(),
        'count': len(articles),
        'articles': articles
    })

@news_recommender_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get statistics about the news dataset"""
    if recommender.df.empty:
        return jsonify({
            'error': 'No news data available'
        }), 404
    
    total_articles = len(recommender.df)
    riasec_counts = recommender.df['RIASEC'].value_counts().to_dict()
    
    return jsonify({
        'total_articles': total_articles,
        'articles_by_riasec': riasec_counts,
        'riasec_descriptions': recommender.get_all_riasec_types()
    })
