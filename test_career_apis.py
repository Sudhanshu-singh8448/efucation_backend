#!/usr/bin/env python3
"""
Test script for Career Guidance APIs
"""

import requests
import json
import time

BASE_URL = "http://localhost:8080/api/career"

def test_endpoint(name, method="GET", url="", data=None, expected_status=200):
    """Test a single endpoint"""
    print(f"\n🧪 Testing {name}...")
    print(f"URL: {url}")
    print(f"Method: {method}")

    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)

        print(f"Status Code: {response.status_code}")

        if response.status_code == expected_status:
            print("✅ SUCCESS")
            try:
                result = response.json()
                print("Response:")
                print(json.dumps(result, indent=2))
                return result
            except:
                print("Response (Text):")
                print(response.text)
                return response.text
        else:
            print(f"❌ FAILED - Expected {expected_status}, got {response.status_code}")
            print("Response:")
            print(response.text)
            return None

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return None

def main():
    print("🚀 Career Guidance API Test Suite")
    print("=" * 50)

    # Test 1: Health Check
    test_endpoint("Health Check", "GET", f"{BASE_URL}/health")

    # Test 2: Start Test
    session_data = test_endpoint("Start Test", "POST", f"{BASE_URL}/start-test", {})
    session_id = None

    if session_data and 'session_id' in session_data:
        session_id = session_data['session_id']
        print(f"\n📝 Using Session ID: {session_id}")

        # Test 3: Get First Question
        question_data = test_endpoint("Get Question", "GET", f"{BASE_URL}/question/{session_id}")

        # Test 4: Submit Answer
        if question_data:
            answer_data = test_endpoint("Submit Answer", "POST", f"{BASE_URL}/answer",
                                      {"session_id": session_id, "answer": 4})

            # Test 5: Get Results (should fail since test not complete)
            test_endpoint("Get Results (Incomplete)", "GET", f"{BASE_URL}/results/{session_id}", expected_status=400)

            # Test 6: Complete the test by answering all questions quickly
            print("\n⚡ Completing test quickly...")
            for i in range(23):  # Already answered 1, need 23 more
                try:
                    # Get next question
                    q_response = requests.get(f"{BASE_URL}/question/{session_id}")
                    if q_response.status_code == 200:
                        # Submit answer
                        requests.post(f"{BASE_URL}/answer", json={"session_id": session_id, "answer": 3})
                    else:
                        break
                except:
                    break

            # Test 7: Get Results (should work now)
            test_endpoint("Get Results (Complete)", "GET", f"{BASE_URL}/results/{session_id}")

    else:
        print("❌ Could not get session ID from start-test")

    print("\n" + "=" * 50)
    print("🏁 Test Suite Complete")

if __name__ == "__main__":
    main()
