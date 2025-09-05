# Deploying to Render - Complete Guide

Follow these steps to deploy your backend to Render. This guide ensures your project is fully ready for deployment.

## 1. Pre-Deployment Setup & Testing

### Create Virtual Environment (Local Testing)
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Test Your App Locally
```bash
# Make sure you're in the project directory and virtual environment is activated
python app.py

# Your app should start on http://localhost:8080
# Test the health endpoint: curl http://localhost:8080/health
```

### Verify All Required Files Exist
- ✅ `app.py` - Main application file
- ✅ `requirements.txt` - All dependencies listed
- ✅ `render.yaml` - Render configuration
- ✅ `services/` - All service modules
- ✅ `data/` - Data files (CSV, JSON)
- ✅ `.gitignore` - Excludes unnecessary files

## 2. Initialize Git Repository & Push to Remote

### Initialize Git (if not already done)
```bash
git init
git add .
git commit -m "Initial commit - Education Platform API"
```

### Create Repository on GitHub/GitLab/Bitbucket
1. Go to GitHub.com and create a new repository
2. Name it something like `education-platform-backend`
3. Don't initialize with README (since you already have files)

### Connect and Push to Remote
```bash
# Replace <YOUR_REPO_URL> with your actual repository URL
git remote add origin <YOUR_REPO_URL>
git branch -M main
git push -u origin main
```

## 3. Deploy on Render

### Create Web Service
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New +** → **Web Service**
3. Connect your GitHub/GitLab/Bitbucket account
4. Select your repository

### Configure Service Settings
**Using render.yaml (Recommended):**
- Render will auto-detect your `render.yaml` file
- All settings are pre-configured in the file

**Manual Configuration (Alternative):**
- **Environment**: Python
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 app:app`
- **Instance Type**: Free (or paid as needed)

### Environment Variables (Already configured in render.yaml)
- `FLASK_ENV=production`
- `PYTHONUNBUFFERED=1`

## 4. Monitor Deployment

1. **Build Process**: Watch the build logs for any errors
2. **Health Check**: Render will check `/health` endpoint
3. **Live URL**: Your app will be available at `https://your-service-name.onrender.com`

## 5. Test Your Deployed API

Once deployed, test these endpoints:
```bash
# Health check
curl https://your-service-name.onrender.com/health

# Main API info
curl https://your-service-name.onrender.com/

# Test a service endpoint
curl https://your-service-name.onrender.com/api/career/health
```

---

## Current Configuration Files

### render.yaml
```yaml
services:
  - type: web
    name: education-platform-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 app:app
    envVars:
      - key: FLASK_ENV
        value: production
      - key: PYTHONUNBUFFERED
        value: "1"
    healthCheckPath: /health
```

### Key Dependencies (requirements.txt)
```txt
Flask==3.0.0
Flask-CORS==4.0.0
pandas>=2.3.2
numpy>=2.3.2
scikit-learn>=1.3.0
geopy>=2.3.0
requests>=2.31.0
python-dateutil>=2.8.2
pytz>=2023.3
pytest>=7.4.0
gunicorn>=21.2.0
```

---

## Troubleshooting

### Common Issues & Solutions

**Build Fails:**
- Check that all dependencies in `requirements.txt` are compatible
- Ensure Python version compatibility (Render uses Python 3.11+ by default)

**App Won't Start:**
- Verify `app.py` has `if __name__ == '__main__':` block
- Check that gunicorn can find your Flask app object

**Health Check Fails:**
- Ensure `/health` endpoint returns 200 status
- Check that app is listening on `0.0.0.0:$PORT`

**Service Errors:**
- Check build and runtime logs in Render dashboard
- Verify all CSV/JSON data files are included in git

### Getting Help
- [Render Python Deployment Guide](https://render.com/docs/deploy-python)
- [Flask Deployment Documentation](https://flask.palletsprojects.com/en/3.0.x/deploying/)

---

## ✅ Pre-Deployment Checklist

Before deploying, ensure:
- [ ] Virtual environment created and tested locally
- [ ] All dependencies installed via `pip install -r requirements.txt`
- [ ] App runs successfully with `python app.py`
- [ ] Health endpoint accessible at `/health`
- [ ] All service endpoints working
- [ ] Git repository initialized and committed
- [ ] Remote repository created on GitHub/GitLab/Bitbucket
- [ ] Code pushed to remote repository
- [ ] `render.yaml` configuration verified
- [ ] `.gitignore` excludes unnecessary files

Your app is now ready for Render deployment! 🚀
