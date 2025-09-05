#!/usr/bin/env python3
"""
Simple test to verify backend is working
"""

import requests
import time

def test_backend():
    print("🧪 Testing Backend Endpoints")
    print("=" * 30)

    base_url = "http://localhost:8080"

    # Wait a moment for server to be ready
    time.sleep(2)

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
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {endpoint}: {response.status_code}")
            else:
                print(f"❌ {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: Failed - {e}")

    print("\n🎉 Test completed!")

if __name__ == "__main__":
    test_backend()
