"""
College Finder Service
Converted from standalone Flask app to Blueprint for unified backend
"""

from flask import Blueprint, request, jsonify
import pandas as pd
import os

# Create Blueprint
college_finder_bp = Blueprint('college_finder', __name__)

# Load college data
def load_college_data():
    """Load college data from CSV file"""
    try:
        # Try to load from the data directory
        csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'college_list.csv')
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
        else:
            # Fallback to original location
            df = pd.read_csv('/Users/sudhanshukumar/project/backend/college_finder_backend/college_list.csv')
        
        # Remove rows that are just division headers (they have empty College_ID)
        df = df.dropna(subset=['College_ID'])
        # Reset index after dropping rows
        df = df.reset_index(drop=True)
        return df
    except FileNotFoundError:
        print("Warning: college_list.csv file not found!")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error loading college data: {str(e)}")
        return pd.DataFrame()

# Load data on startup
college_data = load_college_data()

@college_finder_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'College Finder API',
        'version': '1.0.0',
        'total_colleges': len(college_data)
    }), 200

@college_finder_bp.route('/', methods=['GET'])
def home():
    """Home endpoint with API information"""
    return jsonify({
        "message": "College Filter API",
        "version": "1.0",
        "endpoints": {
            "/": "GET - API information",
            "/colleges": "GET - Get all colleges",
            "/colleges/filter": "POST - Filter colleges based on criteria",
            "/colleges/search": "GET - Search colleges by name",
            "/colleges/fields": "GET - Get available filter fields",
            "/colleges/stats": "GET - Get college statistics"
        },
        "total_colleges": len(college_data)
    })

@college_finder_bp.route('/colleges', methods=['GET'])
def get_all_colleges():
    """Get all colleges"""
    if college_data.empty:
        return jsonify({"error": "No college data available"}), 500
    
    colleges = college_data.to_dict('records')
    return jsonify({
        "total": len(colleges),
        "colleges": colleges
    })

@college_finder_bp.route('/colleges/filter', methods=['POST'])
def filter_colleges():
    """Filter colleges based on user criteria"""
    if college_data.empty:
        return jsonify({"error": "No college data available"}), 500
    
    try:
        filters = request.get_json()
        
        if not filters:
            return jsonify({"error": "No filter criteria provided"}), 400
        
        # Start with all data
        filtered_data = college_data.copy()
        
        # Apply filters
        for key, value in filters.items():
            if value and key in filtered_data.columns:
                if isinstance(value, str):
                    # Case-insensitive partial matching for string filters
                    filtered_data = filtered_data[
                        filtered_data[key].astype(str).str.contains(value, case=False, na=False)
                    ]
                elif isinstance(value, list):
                    # For list values, check if any value matches
                    mask = pd.Series([False] * len(filtered_data))
                    for v in value:
                        mask |= filtered_data[key].astype(str).str.contains(str(v), case=False, na=False)
                    filtered_data = filtered_data[mask]
                else:
                    # Exact matching for other types
                    filtered_data = filtered_data[filtered_data[key] == value]
        
        # Convert to records
        result = filtered_data.to_dict('records')
        
        return jsonify({
            "total": len(result),
            "filters_applied": filters,
            "colleges": result
        })
        
    except Exception as e:
        return jsonify({"error": f"Filter error: {str(e)}"}), 500

@college_finder_bp.route('/colleges/search', methods=['GET'])
def search_colleges():
    """Search colleges by name"""
    if college_data.empty:
        return jsonify({"error": "No college data available"}), 500
    
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({"error": "Search query parameter 'q' is required"}), 400
    
    try:
        # Search in college name (case-insensitive)
        filtered_data = college_data[
            college_data['College_Name'].astype(str).str.contains(query, case=False, na=False)
        ]
        
        result = filtered_data.to_dict('records')
        
        return jsonify({
            "total": len(result),
            "search_query": query,
            "colleges": result
        })
        
    except Exception as e:
        return jsonify({"error": f"Search error: {str(e)}"}), 500

@college_finder_bp.route('/colleges/fields', methods=['GET'])
def get_available_fields():
    """Get all available fields for filtering"""
    if college_data.empty:
        return jsonify({"error": "No college data available"}), 500
    
    fields = {}
    for column in college_data.columns:
        unique_values = college_data[column].dropna().unique().tolist()
        # Limit to reasonable number of unique values
        if len(unique_values) <= 50:
            fields[column] = unique_values
        else:
            fields[column] = f"Too many unique values ({len(unique_values)})"
    
    return jsonify({
        "available_fields": fields,
        "total_columns": len(college_data.columns)
    })

@college_finder_bp.route('/colleges/stats', methods=['GET'])
def get_stats():
    """Get basic statistics about the college data"""
    if college_data.empty:
        return jsonify({"error": "No college data available"}), 500
    
    stats = {
        "total_colleges": len(college_data),
        "colleges_by_division": college_data['Division'].value_counts().to_dict() if 'Division' in college_data.columns else {},
        "colleges_by_district": college_data['District'].value_counts().to_dict() if 'District' in college_data.columns else {},
        "colleges_by_type": college_data['College_Type'].value_counts().to_dict() if 'College_Type' in college_data.columns else {},
        "columns": list(college_data.columns)
    }
    
    return jsonify(stats)
