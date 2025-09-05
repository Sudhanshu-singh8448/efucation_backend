#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
    echo "✅ Environment variables loaded from .env"
else
    echo "⚠️  No .env file found. Please create one from .env.example"
    echo "   cp .env.example .env"
    echo "   Then edit .env with your actual DATABASE_URL"
    exit 1
fi

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo "❌ DATABASE_URL is not set in .env file"
    echo "   Please add your Neon PostgreSQL connection string to .env"
    exit 1
fi

echo "🔗 Database URL configured: ${DATABASE_URL:0:50}..."

# Start the server
echo "🚀 Starting Flask server..."
./venv/bin/python3 app.py
