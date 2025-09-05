#!/usr/bin/env python3
"""
Simple test script to check if the NoSQL backend is working
"""

import requests
import json
import time

def test_api():
    base_url = "http://localhost:8080"
    
    print("🚀 Testing NoSQL Backend API")
    print("=" * 40)
    
    # Test 1: Root endpoint
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"✅ Root endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Version: {data.get('version', 'N/A')}")
            print(f"   Database: {data.get('database', 'N/A')}")
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
    
    # Test 2: Health check
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        print(f"✅ Health check: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Status: {data.get('status', 'N/A')}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    # Test 3: Career guidance health
    try:
        response = requests.get(f"{base_url}/api/career/health", timeout=5)
        print(f"✅ Career health: {response.status_code}")
    except Exception as e:
        print(f"❌ Career health failed: {e}")
    
    # Test 4: Start assessment
    try:
        response = requests.post(f"{base_url}/api/career/start-assessment", 
                               json={"user_id": "test_user"},
                               timeout=5)
        print(f"✅ Start assessment: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Session ID: {data.get('session_id', 'N/A')[:8]}...")
    except Exception as e:
        print(f"❌ Start assessment failed: {e}")
    
    print("\n🎉 Basic API test completed!")

if __name__ == "__main__":
    test_api()
