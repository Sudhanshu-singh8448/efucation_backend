#!/usr/bin/env python3
"""
Test script for the unified backend API
"""

import sys
import os

# Add the current directory to the path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

def test_unified_api():
    print("🧪 Testing Unified Backend API")
    print("=" * 50)
    
    # Test main endpoint
    try:
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Main endpoint working")
                data = response.get_json()
                print(f"   Services available: {list(data['services'].keys())}")
            else:
                print(f"❌ Main endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Main endpoint error: {e}")
    
    # Test health check
    try:
        with app.test_client() as client:
            response = client.get('/health')
            if response.status_code == 200:
                print("✅ Health check working")
            else:
                print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test career guidance service
    try:
        with app.test_client() as client:
            response = client.get('/api/career/health')
            if response.status_code == 200:
                print("✅ Career guidance service healthy")
            else:
                print(f"❌ Career guidance service failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Career guidance service error: {e}")
    
    # Test college finder service
    try:
        with app.test_client() as client:
            response = client.get('/api/college/health')
            if response.status_code == 200:
                print("✅ College finder service healthy")
            else:
                print(f"❌ College finder service failed: {response.status_code}")
    except Exception as e:
        print(f"❌ College finder service error: {e}")
    
    # Test course suggestion service
    try:
        with app.test_client() as client:
            response = client.get('/api/course/health')
            if response.status_code == 200:
                print("✅ Course suggestion service healthy")
            else:
                print(f"❌ Course suggestion service failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Course suggestion service error: {e}")
    
    # Test news recommender service
    try:
        with app.test_client() as client:
            response = client.get('/api/news/health')
            if response.status_code == 200:
                print("✅ News recommender service healthy")
            else:
                print(f"❌ News recommender service failed: {response.status_code}")
    except Exception as e:
        print(f"❌ News recommender service error: {e}")
    
    # Test scholarship service
    try:
        with app.test_client() as client:
            response = client.get('/api/scholarship/health')
            if response.status_code == 200:
                print("✅ Scholarship service healthy")
            else:
                print(f"❌ Scholarship service failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Scholarship service error: {e}")
    
    print("\n🎉 API testing completed!")

if __name__ == "__main__":
    test_unified_api()
