#!/bin/bash

# Deploy to Render Script
# Run this to prepare your unified backend for Render deployment

echo "🚀 Preparing Education Platform for Render Deployment"
echo "========================================================="

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: Please run this script from the unified_backend directory"
    exit 1
fi

echo "✅ Found app.py - in correct directory"

# Check Python version
python_version=$(python3 --version 2>&1)
echo "✅ Python version: $python_version"

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found"
    exit 1
fi

echo "✅ Found requirements.txt"

# Check if data files exist
echo "📁 Checking data files:"
if [ -f "data/college_list.csv" ]; then
    echo "  ✅ college_list.csv"
else
    echo "  ❌ college_list.csv missing"
fi

if [ -f "data/courseAndCollegedata.csv" ]; then
    echo "  ✅ courseAndCollegedata.csv"
else
    echo "  ❌ courseAndCollegedata.csv missing"
fi

if [ -f "data/news_data.csv" ]; then
    echo "  ✅ news_data.csv"
else
    echo "  ❌ news_data.csv missing"
fi

if [ -f "data/scholarship.json" ]; then
    echo "  ✅ scholarship.json"
else
    echo "  ❌ scholarship.json missing"
fi

# Test local installation
echo "🧪 Testing local installation:"
if python3 -c "import flask, pandas, numpy, scikit_learn, geopy, requests" 2>/dev/null; then
    echo "  ✅ All required packages can be imported"
else
    echo "  ❌ Some packages missing. Run: pip install -r requirements.txt"
fi

echo ""
echo "📋 Render Deployment Instructions:"
echo "======================================"
echo ""
echo "1. 🌐 Go to https://render.com and create an account"
echo ""
echo "2. 📝 Create a new Web Service with these settings:"
echo "   - Repository: Connect your GitHub repository"
echo "   - Branch: main (or your preferred branch)"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: gunicorn --bind 0.0.0.0:\$PORT --workers 4 --timeout 120 app:app"
echo "   - Environment: Python 3"
echo ""
echo "3. 🔧 Environment Variables (optional):"
echo "   - FLASK_ENV: production"
echo "   - PYTHONUNBUFFERED: 1"
echo ""
echo "4. 🚀 Deploy and wait for build completion"
echo ""
echo "5. 🧪 Test your deployed API:"
echo "   - Health check: https://your-app.onrender.com/health"
echo "   - API docs: https://your-app.onrender.com/"
echo ""
echo "📊 Service Endpoints:"
echo "====================="
echo "• Career Guidance: /api/career"
echo "• College Finder: /api/college"
echo "• Course Suggestion: /api/course"
echo "• News Recommender: /api/news"
echo "• Scholarship: /api/scholarship"
echo ""
echo "✅ Your unified backend is ready for deployment!"
echo "🔗 All your original APIs will work with the new base URL + service prefix"
