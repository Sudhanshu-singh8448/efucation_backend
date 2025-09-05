#!/usr/bin/env python3
"""
Quick API Test for Career Guidance with Database
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_api():
    print("🧪 Testing Career Guidance APIs with Neon Database")
    print("=" * 60)

    base_url = "http://localhost:5000/api/career"

    # Test 1: Health Check
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health Check Successful!")
            print(f"   Database: {data.get('database', 'unknown')}")
            print(f"   Active Sessions: {data.get('active_sessions', 0)}")
        else:
            print("❌ Health check failed")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

    # Test 2: Start Test
    print("\n2. Testing Start Test...")
    try:
        response = requests.post(f"{base_url}/start-test", timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            session_id = data.get('session_id')
            print("✅ Test Started Successfully!")
            print(f"   Session ID: {session_id}")
        else:
            print("❌ Start test failed")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ Start test error: {e}")
        return False

    # Test 3: Get Question
    print("\n3. Testing Get Question...")
    try:
        response = requests.get(f"{base_url}/question/{session_id}", timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Question Retrieved Successfully!")
            print(f"   Question: {data.get('question', '')[:50]}...")
        else:
            print("❌ Get question failed")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ Get question error: {e}")
        return False

    print("\n" + "=" * 60)
    print("✅ All API tests passed!")
    print("🎉 Career Guidance service is working with Neon Database!")
    return True

if __name__ == "__main__":
    # Install python-dotenv if needed
    try:
        import dotenv
    except ImportError:
        print("Installing python-dotenv...")
        os.system("pip install python-dotenv")
        import dotenv

    test_api()
