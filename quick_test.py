#!/usr/bin/env python3
"""
Quick test script for career guidance APIs
"""
import requests
import json
import time

BASE_URL = "http://localhost:8081/api/career"

def test_health():
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health: {response.status_code}")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print("❌ Health check failed")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_start_session():
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
            return None
    except Exception as e:
        print(f"❌ Start test error: {e}")
        return None

def test_get_question(session_id):
    try:
        response = requests.get(f"{BASE_URL}/question/{session_id}")
        print(f"Get Question: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Question retrieved: {result.get('question_number')}")
            return True
        else:
            print("❌ Get question failed")
            return False
    except Exception as e:
        print(f"❌ Get question error: {e}")
        return False

def test_submit_answer(session_id):
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
    print("Testing Career Guidance APIs...")

    # Test health
    if not test_health():
        print("Server not running or health check failed")
        exit(1)

    # Test start session
    session_id = test_start_session()
    if not session_id:
        print("Failed to start session")
        exit(1)

    # Test get question
    if not test_get_question(session_id):
        print("Failed to get question")
        exit(1)

    # Test submit answer
    if not test_submit_answer(session_id):
        print("Failed to submit answer")
        exit(1)

    print("✅ All tests passed!")
