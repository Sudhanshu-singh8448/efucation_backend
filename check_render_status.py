#!/usr/bin/env python3
"""
Render API Status Checker
Checks if your Education Platform API is live on Render
"""

import requests
import json
import time
from datetime import datetime

def test_endpoint(base_url, endpoint, description):
    """Test a single API endpoint"""
    url = f"{base_url}{endpoint}"
    print(f"\n🌐 Testing: {description}")
    print(f"URL: {url}")
    
    try:
        start_time = time.time()
        response = requests.get(url, timeout=30)
        response_time = time.time() - start_time
        
        print(f"Status: {response.status_code}")
        print(f"Response Time: {response_time:.2f}s")
        
        if response.status_code == 200:
            print("✅ SUCCESS")
            try:
                json_data = response.json()
                print("Response (JSON):")
                print(json.dumps(json_data, indent=2)[:300])
                if len(str(json_data)) > 300:
                    print("...")
            except:
                print("Response (Text):")
                print(response.text[:200])
                if len(response.text) > 200:
                    print("...")
        elif response.status_code == 404:
            print("❌ NOT FOUND (404)")
            print("Server might be sleeping or URL is incorrect")
        elif response.status_code == 500:
            print("💥 SERVER ERROR (500)")
            print("Check Render logs for deployment issues")
        else:
            print(f"⚠️  HTTP {response.status_code}")
            print(f"Response: {response.text[:100]}")
            
    except requests.exceptions.Timeout:
        print("⏰ TIMEOUT (30s)")
        print("Server might be sleeping. Try again in 30-60 seconds.")
    except requests.exceptions.ConnectionError:
        print("🔌 CONNECTION ERROR")
        print("Check if the URL is correct or if Render service is running")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
    
    print("-" * 50)

def main():
    print("🔍 Render API Status Checker")
    print("=" * 40)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # You need to replace this with your actual Render URL
    base_url = "https://education-platform-api-xxxx.onrender.com"
    
    print("📋 Instructions:")
    print("1. Go to https://dashboard.render.com/")
    print("2. Find your 'education-platform-api' service")
    print("3. Copy the service URL")
    print("4. Replace the base_url in this script")
    print()
    print("⚠️  Currently testing placeholder URL (will fail):")
    print(f"   {base_url}")
    print()
    
    # Test all endpoints
    endpoints = [
        ("/", "Main API Documentation"),
        ("/health", "Health Check"),
        ("/api/career/health", "Career Guidance Health"),
        ("/api/college/health", "College Finder Health"), 
        ("/api/course/docs", "Course Suggestion Docs"),
        ("/api/news/health", "News Recommender Health"),
        ("/api/scholarship/health", "Scholarship Health"),
        ("/api/career", "Career Guidance Service"),
        ("/api/college", "College Finder Service"),
        ("/api/course", "Course Suggestion Service"),
        ("/api/news", "News Recommender Service"),
        ("/api/scholarship", "Scholarship Service"),
    ]
    
    print("🚀 Starting tests...\n")
    
    for endpoint, description in endpoints:
        test_endpoint(base_url, endpoint, description)
    
    print("\n📊 Summary:")
    print("- If all tests fail: Update the base_url with your actual Render URL")
    print("- If server is sleeping: Wait 30-60 seconds and run again")
    print("- If 500 errors: Check Render dashboard logs")
    print("- If tests pass: Your API is live! 🎉")

if __name__ == "__main__":
    main()
