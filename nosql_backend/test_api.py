"""
Comprehensive Test Suite for Unified Education Backend - NoSQL Version
Tests all API endpoints across all services
"""

import requests
import json
import time
import random

# Base URL for the API
BASE_URL = "http://localhost:8080"

def test_health_endpoints():
    """Test all health check endpoints"""
    print("=" * 60)
    print("TESTING HEALTH ENDPOINTS")
    print("=" * 60)
    
    endpoints = [
        "/api/health",
        "/api/career/health",
        "/api/college/health",
        "/api/course/health",
        "/api/news/health",
        "/api/scholarship/health"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            print(f"✓ {endpoint}: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"  Status: {data.get('status', 'unknown')}")
            else:
                print(f"  Error: {response.text}")
        except Exception as e:
            print(f"✗ {endpoint}: Failed - {e}")
        print()

def test_career_guidance():
    """Test career guidance endpoints"""
    print("=" * 60)
    print("TESTING CAREER GUIDANCE SERVICE")
    print("=" * 60)
    
    # Start assessment
    try:
        response = requests.post(f"{BASE_URL}/api/career/start-assessment", 
                               json={"user_id": "test_user_123"})
        print(f"✓ Start Assessment: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            session_id = data.get('session_id')
            print(f"  Session ID: {session_id}")
            
            # Submit answers
            sample_answers = []
            for i in range(24):
                sample_answers.append(random.randint(1, 5))
            
            answer_response = requests.post(f"{BASE_URL}/api/career/submit-answers",
                                          json={
                                              "session_id": session_id,
                                              "answers": sample_answers
                                          })
            print(f"✓ Submit Answers: {answer_response.status_code}")
            
            if answer_response.status_code == 200:
                # Get recommendations
                rec_response = requests.get(f"{BASE_URL}/api/career/recommendations/{session_id}")
                print(f"✓ Get Recommendations: {rec_response.status_code}")
                
                if rec_response.status_code == 200:
                    rec_data = rec_response.json()
                    print(f"  RIASEC Scores: {rec_data.get('riasec_scores', {})}")
                    print(f"  Top Career: {rec_data.get('career_recommendations', [{}])[0].get('career', 'N/A')}")
        
    except Exception as e:
        print(f"✗ Career Guidance Test Failed: {e}")
    print()

def test_college_finder():
    """Test college finder endpoints"""
    print("=" * 60)
    print("TESTING COLLEGE FINDER SERVICE")
    print("=" * 60)
    
    # Search colleges
    try:
        response = requests.get(f"{BASE_URL}/api/college/search", 
                              params={"q": "engineering", "limit": 5})
        print(f"✓ College Search: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  Found {data.get('total_results', 0)} colleges")
        
        # Get statistics
        stats_response = requests.get(f"{BASE_URL}/api/college/statistics")
        print(f"✓ College Statistics: {stats_response.status_code}")
        
        if stats_response.status_code == 200:
            stats_data = stats_response.json()
            print(f"  Total Colleges: {stats_data.get('total_colleges', 0)}")
        
        # Filter colleges
        filter_response = requests.post(f"{BASE_URL}/api/college/filter",
                                      json={
                                          "state": "Maharashtra",
                                          "course_type": "Engineering",
                                          "limit": 3
                                      })
        print(f"✓ College Filter: {filter_response.status_code}")
        
        if filter_response.status_code == 200:
            filter_data = filter_response.json()
            print(f"  Filtered Results: {filter_data.get('total_results', 0)}")
        
    except Exception as e:
        print(f"✗ College Finder Test Failed: {e}")
    print()

def test_course_suggestion():
    """Test course suggestion endpoints"""
    print("=" * 60)
    print("TESTING COURSE SUGGESTION SERVICE")
    print("=" * 60)
    
    try:
        # Get course recommendations
        response = requests.post(f"{BASE_URL}/api/course/recommend",
                               json={
                                   "riasec_scores": {
                                       "R": 4.2,
                                       "I": 3.8,
                                       "A": 2.1,
                                       "S": 3.0,
                                       "E": 3.5,
                                       "C": 2.8
                                   },
                                   "location": "Mumbai",
                                   "num_recommendations": 5
                               })
        print(f"✓ Course Recommendations: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  Total Recommendations: {data.get('total_recommendations', 0)}")
            if data.get('recommendations'):
                print(f"  Top Course: {data['recommendations'][0].get('course_name', 'N/A')}")
        
        # Search courses
        search_response = requests.get(f"{BASE_URL}/api/course/search",
                                     params={"q": "computer science", "limit": 3})
        print(f"✓ Course Search: {search_response.status_code}")
        
        if search_response.status_code == 200:
            search_data = search_response.json()
            print(f"  Search Results: {search_data.get('total_results', 0)}")
        
    except Exception as e:
        print(f"✗ Course Suggestion Test Failed: {e}")
    print()

def test_news_recommender():
    """Test news recommender endpoints"""
    print("=" * 60)
    print("TESTING NEWS RECOMMENDER SERVICE")
    print("=" * 60)
    
    try:
        # Get news recommendations
        response = requests.post(f"{BASE_URL}/api/news/recommend",
                               json={
                                   "riasec_types": "RI",
                                   "num_recommendations": 5
                               })
        print(f"✓ News Recommendations: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  Total Recommendations: {data.get('total_recommendations', 0)}")
        
        # Get news by type
        type_response = requests.get(f"{BASE_URL}/api/news/news-by-type/R")
        print(f"✓ News by Type (R): {type_response.status_code}")
        
        if type_response.status_code == 200:
            type_data = type_response.json()
            print(f"  Articles for Type R: {type_data.get('total_articles', 0)}")
        
        # Search articles
        search_response = requests.get(f"{BASE_URL}/api/news/articles/search",
                                     params={"q": "technology"})
        print(f"✓ News Search: {search_response.status_code}")
        
        if search_response.status_code == 200:
            search_data = search_response.json()
            print(f"  Search Results: {search_data.get('total_results', 0)}")
        
        # Get categories
        cat_response = requests.get(f"{BASE_URL}/api/news/categories")
        print(f"✓ News Categories: {cat_response.status_code}")
        
    except Exception as e:
        print(f"✗ News Recommender Test Failed: {e}")
    print()

def test_scholarship():
    """Test scholarship endpoints"""
    print("=" * 60)
    print("TESTING SCHOLARSHIP SERVICE")
    print("=" * 60)
    
    try:
        # Get scholarship recommendations
        response = requests.post(f"{BASE_URL}/api/scholarship/recommend",
                               json={
                                   "riasec_types": "IE",
                                   "cgpa": 3.5,
                                   "income_level": "low",
                                   "location": "India",
                                   "field_of_study": "Engineering"
                               })
        print(f"✓ Scholarship Recommendations: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  Total Recommendations: {data.get('total_recommendations', 0)}")
        
        # Search scholarships
        search_response = requests.get(f"{BASE_URL}/api/scholarship/search",
                                     params={"field": "engineering"})
        print(f"✓ Scholarship Search: {search_response.status_code}")
        
        if search_response.status_code == 200:
            search_data = search_response.json()
            print(f"  Search Results: {search_data.get('total_results', 0)}")
        
        # Get scholarships by RIASEC type
        riasec_response = requests.get(f"{BASE_URL}/api/scholarship/by-riasec/I")
        print(f"✓ Scholarships by RIASEC (I): {riasec_response.status_code}")
        
        if riasec_response.status_code == 200:
            riasec_data = riasec_response.json()
            print(f"  Scholarships for Type I: {riasec_data.get('total_scholarships', 0)}")
        
        # Get fields
        fields_response = requests.get(f"{BASE_URL}/api/scholarship/fields")
        print(f"✓ Scholarship Fields: {fields_response.status_code}")
        
    except Exception as e:
        print(f"✗ Scholarship Test Failed: {e}")
    print()

def test_general_endpoints():
    """Test general endpoints"""
    print("=" * 60)
    print("TESTING GENERAL ENDPOINTS")
    print("=" * 60)
    
    try:
        # Root endpoint
        response = requests.get(f"{BASE_URL}/")
        print(f"✓ Root Endpoint: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  Message: {data.get('message', 'N/A')}")
            print(f"  Version: {data.get('version', 'N/A')}")
        
        # Services list
        services_response = requests.get(f"{BASE_URL}/api/services")
        print(f"✓ Services List: {services_response.status_code}")
        
        if services_response.status_code == 200:
            services_data = services_response.json()
            services = services_data.get('services', {})
            print(f"  Available Services: {len(services)}")
            for service_name in services.keys():
                print(f"    - {service_name}")
        
    except Exception as e:
        print(f"✗ General Endpoints Test Failed: {e}")
    print()

def run_all_tests():
    """Run all API tests"""
    print("🚀 STARTING COMPREHENSIVE API TESTS")
    print("📅 Time:", time.strftime("%Y-%m-%d %H:%M:%S"))
    print("🌐 Base URL:", BASE_URL)
    print()
    
    # Wait a moment for server to be ready
    time.sleep(2)
    
    # Run all tests
    test_general_endpoints()
    test_health_endpoints()
    test_career_guidance()
    test_college_finder()
    test_course_suggestion()
    test_news_recommender()
    test_scholarship()
    
    print("=" * 60)
    print("✅ ALL TESTS COMPLETED")
    print("=" * 60)
    print()
    print("📋 TEST SUMMARY:")
    print("• Health endpoints tested")
    print("• Career guidance workflow tested")
    print("• College finder functionality tested")
    print("• Course suggestion system tested")
    print("• News recommender service tested")
    print("• Scholarship service tested")
    print()
    print("🔍 Check the output above for any failed tests (marked with ✗)")

if __name__ == "__main__":
    run_all_tests()
