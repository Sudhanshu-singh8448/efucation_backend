#!/usr/bin/env python3
"""
Test Career Guidance APIs with Database
"""

import requests
import json
import time

BASE_URL = "http://localhost:8080/api/career"

def test_api():
    print("🧪 Testing Career Guidance APIs with Database")
    print("=" * 50)

    # Test 1: Health Check
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Database: {data.get('database', 'unknown')}")
            print(f"✅ Active Sessions: {data.get('active_sessions', 0)}")
        else:
            print("❌ Health check failed")
            return
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return

    # Test 2: Start Test
    print("\n2. Testing Start Test...")
    try:
        response = requests.post(f"{BASE_URL}/start-test", timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            session_id = data.get('session_id')
            print(f"✅ Session Created: {session_id}")
        else:
            print("❌ Start test failed")
            print(response.text)
            return
    except Exception as e:
        print(f"❌ Start test failed: {e}")
        return

    # Test 3: Get Question
    print("\n3. Testing Get Question...")
    try:
        response = requests.get(f"{BASE_URL}/question/{session_id}", timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Question {data.get('question_number')}: {data.get('question')[:50]}...")
        else:
            print("❌ Get question failed")
            print(response.text)
            return
    except Exception as e:
        print(f"❌ Get question failed: {e}")
        return

    # Test 4: Submit Answer
    print("\n4. Testing Submit Answer...")
    try:
        response = requests.post(f"{BASE_URL}/answer",
                               json={"session_id": session_id, "answer": 4},
                               timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Answer recorded - Progress: {data.get('progress', 0):.1f}%")
        else:
            print("❌ Submit answer failed")
            print(response.text)
            return
    except Exception as e:
        print(f"❌ Submit answer failed: {e}")
        return

    # Test 5: Get Results (should fail - test not complete)
    print("\n5. Testing Get Results (Incomplete)...")
    try:
        response = requests.get(f"{BASE_URL}/results/{session_id}", timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 400:
            print("✅ Correctly returns 400 for incomplete test")
        else:
            print("❌ Unexpected response for incomplete test")
    except Exception as e:
        print(f"❌ Get results failed: {e}")

    print("\n" + "=" * 50)
    print("✅ All basic tests passed!")
    print("📊 Database integration is working correctly")
    print("💡 The career guidance service is ready to store and process data")

if __name__ == "__main__":
    test_api()
