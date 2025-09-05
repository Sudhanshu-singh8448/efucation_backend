#!/usr/bin/env python3
"""
Simple API test script for career guidance endpoints
"""
import requests
import json
import time

BASE_URL = "http://localhost:8080/api/career"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health Check: {response.status_code}")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"Response: {response.json()}")
            return True
        else:
            print("❌ Health check failed")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_start_session():
    """Test starting a new test session"""
    try:
        data = {"user_id": "test_user_123"}
        response = requests.post(f"{BASE_URL}/start-test", json=data)
        print(f"Start Test: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            session_id = result.get('session_id')
            print(f"✅ Session started: {session_id}")
            return session_id
        else:
            print("❌ Start test failed")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Start test error: {e}")
        return None

def test_get_question(session_id):
    """Test getting a question"""
    try:
        response = requests.get(f"{BASE_URL}/question/{session_id}")
        print(f"Get Question: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Question retrieved: Q{result.get('question_number')}")
            print(f"Question: {result.get('question')}")
            return True
        else:
            print("❌ Get question failed")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Get question error: {e}")
        return False

def test_submit_answer(session_id):
    """Test submitting an answer"""
    try:
        data = {"session_id": session_id, "answer": 4}
        response = requests.post(f"{BASE_URL}/answer", json=data)
        print(f"Submit Answer: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Answer submitted: {result.get('message')}")
            return True
        else:
            print(f"❌ Submit answer failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Submit answer error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Career Guidance APIs...")
    print("=" * 50)

    # Test health
    if not test_health():
        print("❌ Server not running or health check failed")
        exit(1)

    print("\n" + "=" * 50)

    # Test start session
    session_id = test_start_session()
    if not session_id:
        print("❌ Failed to start session")
        exit(1)

    print("\n" + "=" * 50)

    # Test get question
    if not test_get_question(session_id):
        print("❌ Failed to get question")
        exit(1)

    print("\n" + "=" * 50)

    # Test submit answer
    if not test_submit_answer(session_id):
        print("❌ Failed to submit answer")
        exit(1)

    print("\n" + "=" * 50)
    print("✅ All tests passed successfully!")
