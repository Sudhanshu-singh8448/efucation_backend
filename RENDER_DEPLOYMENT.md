# Deploying Your Education Platform Backend to Render

This guide will help you deploy your unified backend to Render. Your project is already well-configured for deployment!

## 🔍 Pre-Deployment Checklist

✅ **Project Structure**: Your project has all necessary files  
✅ **Dependencies**: `requirements.txt` is properly configured  
✅ **Entry Point**: `app.py` is ready with proper port configuration  
✅ **Production Config**: `render.yaml` is configured with Gunicorn  
✅ **CORS**: Flask-CORS is enabled for frontend integration  
✅ **Health Check**: `/health` endpoint is available  

## 📋 What You Need to Do

### Step 1: Initialize Git Repository
Your project isn't in a git repository yet. Run these commands in your terminal:

```bash
# Navigate to your project directory
cd /Users/sudhanshukumar/project/backend/unified_backend

# Initialize git repository
git init

# Add all files to git
git add .

# Create initial commit
git commit -m "Initial commit: Education Platform Unified Backend"
```

### Step 2: Create GitHub Repository
1. Go to [GitHub.com](https://github.com) and sign in
2. Click **New Repository** (green button)
3. Name it: `education-platform-backend` or similar
4. Keep it **Public** (required for Render free tier)
5. Don't initialize with README (you already have one)
6. Click **Create Repository**

### Step 3: Push to GitHub
Replace `YOUR_USERNAME` with your GitHub username:

```bash
# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/education-platform-backend.git

# Set main branch
git branch -M main

# Push to GitHub
git push -u origin main
```

### Step 4: Deploy to Render

1. **Sign up/Login to Render**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub (recommended)

2. **Create Web Service**
   - Click **New +** → **Web Service**
   - Connect your GitHub repository
   - Select your `education-platform-backend` repository

3. **Configure Service** (Render will auto-detect from your `render.yaml`):
   - **Name**: `education-platform-api`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 app:app`
   - **Plan**: Free (or upgrade as needed)

4. **Deploy**
   - Click **Create Web Service**
   - Wait 3-5 minutes for build and deployment

## 🔧 Your Current Configuration

### App Configuration (`app.py`)
- ✅ Listens on `0.0.0.0` (required for Render)
- ✅ Uses `PORT` environment variable
- ✅ Production-ready error handlers
- ✅ Health check endpoint at `/health`

### Production Server (`render.yaml`)
- ✅ Uses Gunicorn for production serving
- ✅ 4 workers for better performance
- ✅ 120-second timeout for long requests
- ✅ Health check configured

### Dependencies (`requirements.txt`)
- ✅ All required packages listed
- ✅ Gunicorn included for production
- ✅ Version pinning for stability

## 🚀 After Deployment

Your API will be available at:
```
https://education-platform-api.onrender.com
```

### Test Your Deployment
```bash
# Health check
curl https://your-app-name.onrender.com/health

# API documentation
curl https://your-app-name.onrender.com/

# Test a service (example)
curl https://your-app-name.onrender.com/api/career/health
```

### Available Endpoints
- **Main API**: `/`
- **Health Check**: `/health`
- **Career Guidance**: `/api/career/*`
- **College Finder**: `/api/college/*`
- **Course Suggestions**: `/api/course/*`
- **News Recommender**: `/api/news/*`
- **Scholarships**: `/api/scholarship/*`

## 🔧 Environment Variables (if needed)

If your services require API keys or other config:
1. Go to your Render service dashboard
2. Click **Environment** tab
3. Add variables like:
   - `API_KEY=your_key_here`
   - `DATABASE_URL=your_db_url`

## 🛠️ Troubleshooting

### Common Issues:
1. **Build Fails**: Check `requirements.txt` dependencies
2. **App Won't Start**: Verify port configuration in `app.py`
3. **502 Error**: Check Gunicorn configuration in `render.yaml`
4. **Timeout**: Increase timeout in `render.yaml` if needed

### Logs:
- View logs in Render dashboard → **Logs** tab
- Look for startup errors or service failures

## 🔄 Continuous Deployment

Once connected:
- Push changes to your `main` branch
- Render automatically rebuilds and deploys
- Zero-downtime deployments

---

## 🎯 Ready to Deploy?

Run the git commands in Step 1, create your GitHub repo in Step 2, push your code in Step 3, then deploy to Render in Step 4. Your backend is already optimized for production deployment!
