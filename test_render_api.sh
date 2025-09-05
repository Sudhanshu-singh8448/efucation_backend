#!/bin/bash

# Render API Testing Script
# This script tests all your API endpoints on Render

echo "🔍 Testing Render API Deployment"
echo "================================="

# You need to replace this with your actual Render URL
# Go to your Render dashboard to find the correct URL
RENDER_URL="https://efucation-backend.onrender.com"

echo "📋 Instructions to find your Render URL:"
echo "1. Go to https://dashboard.render.com/"
echo "2. Click on your 'education-platform-api' service"
echo "3. Copy the URL from the service dashboard"
echo "4. Replace RENDER_URL in this script with your actual URL"
echo ""

echo "🧪 Current URL being tested: $RENDER_URL"
echo ""

# Function to test an endpoint
test_endpoint() {
    local endpoint="$1"
    local description="$2"
    
    echo "🌐 Testing: $description"
    echo "URL: $RENDER_URL$endpoint"
    
    # Test with timeout and show response time
    response=$(curl -s -w "\n%{http_code}\n%{time_total}" --max-time 30 "$RENDER_URL$endpoint" 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        # Extract response body, status code, and time
        body=$(echo "$response" | head -n -2)
        status_code=$(echo "$response" | tail -n 2 | head -n 1)
        response_time=$(echo "$response" | tail -n 1)
        
        echo "Status: $status_code"
        echo "Response Time: ${response_time}s"
        
        if [ "$status_code" = "200" ]; then
            echo "✅ SUCCESS"
            echo "Response: $body" | head -c 200
            if [ ${#body} -gt 200 ]; then echo "..."; fi
        elif [ "$status_code" = "404" ]; then
            echo "❌ NOT FOUND (404)"
        elif [ "$status_code" = "500" ]; then
            echo "💥 SERVER ERROR (500)"
        else
            echo "⚠️  HTTP $status_code"
            echo "Response: $body"
        fi
    else
        echo "🔌 CONNECTION FAILED (Timeout or Network Error)"
        echo "This could mean:"
        echo "- Server is sleeping (wait 30-60 seconds and try again)"
        echo "- Wrong URL (check your Render dashboard)"
        echo "- Service deployment failed"
    fi
    
    echo ""
    echo "----------------------------------------"
}

# Test all endpoints
echo "🚀 Starting API Tests..."
echo ""

# Main endpoints
test_endpoint "/" "Main API Documentation"
test_endpoint "/health" "Health Check"

# Service endpoints - Health checks
test_endpoint "/api/career/health" "Career Guidance Health"
test_endpoint "/api/college/health" "College Finder Health"
test_endpoint "/api/course/docs" "Course Suggestion Docs"
test_endpoint "/api/news/health" "News Recommender Health"
test_endpoint "/api/scholarship/health" "Scholarship Health"

# Example service endpoints (you can add more specific tests)
echo "🔬 Testing Sample Service Endpoints..."
echo ""

# Career guidance example
test_endpoint "/api/career" "Career Guidance Service"

# College finder example  
test_endpoint "/api/college" "College Finder Service"

# Course suggestion example
test_endpoint "/api/course" "Course Suggestion Service"

# News recommender example
test_endpoint "/api/news" "News Recommender Service"

# Scholarship example
test_endpoint "/api/scholarship" "Scholarship Service"

echo "📊 Test Summary"
echo "==============="
echo "If you see CONNECTION FAILED or 404 errors:"
echo "1. 🔍 Check your actual Render URL in the dashboard"
echo "2. ⏰ Wait 30-60 seconds for server to wake up if sleeping"
echo "3. 📋 Check Render logs for deployment issues"
echo "4. 🔧 Verify your app is deployed and running"
echo ""
echo "If tests pass:"
echo "✅ Your API is live and ready!"
echo "🔗 Update the FLUTTER_KEEP_ALIVE_PROMPT.md with the correct URL"
echo ""
echo "🌐 Render Dashboard: https://dashboard.render.com/"
