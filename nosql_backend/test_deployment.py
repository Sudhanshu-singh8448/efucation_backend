#!/usr/bin/env python3
"""
Deployment Test Script
Tests the deployed backend on Render to ensure everything is working
"""

import requests
import json
import sys
import time

def test_deployment(base_url):
    """Test the deployed backend"""
    print(f"🚀 Testing Deployment: {base_url}")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 0
    
    # Test 1: Health Check
    total_tests += 1
    try:
        response = requests.get(f"{base_url}/api/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'healthy':
                print("✅ Health Check: PASSED")
                tests_passed += 1
            else:
                print(f"❌ Health Check: FAILED - Status: {data.get('status')}")
        else:
            print(f"❌ Health Check: FAILED - Status Code: {response.status_code}")
    except Exception as e:
        print(f"❌ Health Check: FAILED - Error: {e}")
    
    # Test 2: Root Endpoint
    total_tests += 1
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('version') == '2.0.0':
                print("✅ Root Endpoint: PASSED")
                tests_passed += 1
            else:
                print(f"❌ Root Endpoint: FAILED - Wrong version: {data.get('version')}")
        else:
            print(f"❌ Root Endpoint: FAILED - Status Code: {response.status_code}")
    except Exception as e:
        print(f"❌ Root Endpoint: FAILED - Error: {e}")
    
    # Test 3: Services List
    total_tests += 1
    try:
        response = requests.get(f"{base_url}/api/services", timeout=10)
        if response.status_code == 200:
            data = response.json()
            services = data.get('services', {})
            if len(services) == 5:
                print("✅ Services List: PASSED")
                tests_passed += 1
            else:
                print(f"❌ Services List: FAILED - Expected 5 services, got {len(services)}")
        else:
            print(f"❌ Services List: FAILED - Status Code: {response.status_code}")
    except Exception as e:
        print(f"❌ Services List: FAILED - Error: {e}")
    
    # Test 4: Career Assessment Start
    total_tests += 1
    try:
        response = requests.post(f"{base_url}/api/career/start-assessment", 
                               json={"user_id": "test_deployment"},
                               timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('session_id'):
                print("✅ Career Assessment: PASSED")
                tests_passed += 1
            else:
                print(f"❌ Career Assessment: FAILED - No session_id returned")
        else:
            print(f"❌ Career Assessment: FAILED - Status Code: {response.status_code}")
    except Exception as e:
        print(f"❌ Career Assessment: FAILED - Error: {e}")
    
    # Test 5: College Search
    total_tests += 1
    try:
        response = requests.get(f"{base_url}/api/college/search?q=engineering&limit=3", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success') == True:
                print("✅ College Search: PASSED")
                tests_passed += 1
            else:
                print(f"❌ College Search: FAILED - Success: {data.get('success')}")
        else:
            print(f"❌ College Search: FAILED - Status Code: {response.status_code}")
    except Exception as e:
        print(f"❌ College Search: FAILED - Error: {e}")
    
    # Results
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests PASSED! Your backend is ready for production!")
        return True
    else:
        print(f"⚠️  {total_tests - tests_passed} tests failed. Please check the issues above.")
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python test_deployment.py <BASE_URL>")
        print("Example: python test_deployment.py https://your-app.onrender.com")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    success = test_deployment(base_url)
    
    if success:
        print(f"\n🔗 Your API is live at: {base_url}")
        print(f"📚 API Documentation: {base_url}/api/services")
        print(f"❤️  Health Check: {base_url}/api/health")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
