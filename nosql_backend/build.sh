#!/bin/bash

# Build script for Render deployment
echo "🚀 Starting build process for Education Backend..."

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs

# Set permissions
echo "🔒 Setting permissions..."
chmod +x app.py

# Verify installation
echo "✅ Verifying installation..."
python -c "import flask, pymongo, pandas; print('All dependencies installed successfully')"

echo "🎉 Build completed successfully!"
