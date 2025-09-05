#!/usr/bin/env python3
"""
Simple test for answer endpoint
"""
import urllib.request
import json
import time

def test_answer():
    url = "http://localhost:8081/api/career/answer"
    data = {
        "session_id": "b94cb658-e6fc-4300-801a-e129feb9ed29",
        "answer": 4
    }

    json_data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=json_data, headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"Status: {response.status}")
            print(f"Response: {result}")
            return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing answer endpoint...")
    test_answer()
