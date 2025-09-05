# 🚀 Render Deployment Checklist

## Pre-Deployment Steps

### 1. Repository Setup
- [ ] Push `nosql_backend` folder to GitHub repository
- [ ] Ensure all files are committed and pushed
- [ ] Repository is public or you have Render GitHub access

### 2. MongoDB Atlas Setup
- [ ] MongoDB Atlas cluster is running
- [ ] Network access is configured (0.0.0.0/0 for Render)
- [ ] Database user has read/write permissions
- [ ] Connection string is ready: `mongodb+srv://sudhanshu:Sudha%407250@cluster0.pmdxjrt.mongodb.net/`

### 3. Render Account Setup
- [ ] Create account at [render.com](https://render.com)
- [ ] Connect GitHub account to Render
- [ ] Have MongoDB URI ready for environment variables

## Deployment Process

### Option A: Manual Deploy (Recommended)

1. **Create New Web Service**:
   - Go to Render Dashboard
   - Click "New" → "Web Service"
   - Select "Build and deploy from a Git repository"
   - Choose your repository

2. **Configure Service**:
   ```
   Name: education-backend-nosql
   Environment: Python 3
   Region: Oregon (US West) or closest to your users
   Branch: main
   Root Directory: nosql_backend (if not in repo root)
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn --config gunicorn_config.py app:app
   ```

3. **Environment Variables**:
   Add these in the Environment section:
   ```
   MONGODB_URI = mongodb+srv://sudhanshu:Sudha%407250@cluster0.pmdxjrt.mongodb.net/
   DATABASE_NAME = education_platform
   FLASK_ENV = production
   FLASK_DEBUG = False
   PORT = 10000
   HOST = 0.0.0.0
   SECRET_KEY = [Let Render auto-generate this]
   ```

4. **Advanced Settings**:
   ```
   Health Check Path: /api/health
   Auto-Deploy: Yes
   ```

### Option B: Using render.yaml (Infrastructure as Code)

1. **Automatic Detection**:
   - Render will detect the `render.yaml` file
   - Just add the MongoDB URI in environment variables
   - Everything else is preconfigured

## Post-Deployment Verification

### 1. Basic Health Checks
```bash
# Replace YOUR_APP_URL with your actual Render URL
curl https://YOUR_APP_URL.onrender.com/api/health
curl https://YOUR_APP_URL.onrender.com/
curl https://YOUR_APP_URL.onrender.com/api/services
```

### 2. Service-Specific Tests
```bash
# Career Assessment
curl -X POST https://YOUR_APP_URL.onrender.com/api/career/start-assessment \
     -H "Content-Type: application/json" \
     -d '{"user_id": "test_user"}'

# College Search
curl "https://YOUR_APP_URL.onrender.com/api/college/search?q=engineering&limit=3"

# News Recommendations
curl -X POST https://YOUR_APP_URL.onrender.com/api/news/recommend \
     -H "Content-Type: application/json" \
     -d '{"riasec_types": "RI", "num_recommendations": 3}'
```

### 3. Database Connection Test
The health endpoint should return:
```json
{
  "status": "healthy",
  "database": {
    "status": "connected",
    "type": "MongoDB Atlas"
  }
}
```

## Expected URLs

After deployment, your service will be available at:
- **Main URL**: `https://education-backend-nosql.onrender.com`
- **Health Check**: `https://education-backend-nosql.onrender.com/api/health`
- **API Documentation**: `https://education-backend-nosql.onrender.com/api/services`

## Troubleshooting

### Build Issues
- [ ] Check build logs in Render dashboard
- [ ] Verify requirements.txt has all dependencies
- [ ] Ensure Python version compatibility (3.11)

### Runtime Issues
- [ ] Check application logs in Render dashboard
- [ ] Verify MongoDB URI is correct
- [ ] Check environment variables are set
- [ ] Ensure health check endpoint responds

### Database Issues
- [ ] MongoDB Atlas cluster is running
- [ ] Network access allows Render IPs (0.0.0.0/0)
- [ ] Database user credentials are correct
- [ ] Database name matches environment variable

### Performance Issues
- [ ] Monitor response times in Render dashboard
- [ ] Check if free tier limits are exceeded
- [ ] Consider upgrading to paid plan for better performance

## Success Indicators

✅ **Deployment Successful When**:
- [ ] Build completes without errors
- [ ] Health check returns 200 status
- [ ] All API endpoints respond correctly
- [ ] MongoDB connection is established
- [ ] No errors in application logs

🎉 **Your NoSQL Education Backend is now live on Render!**

## Next Steps

1. **Update Frontend**: Point your Flutter/React app to the new Render URL
2. **Custom Domain**: (Optional) Add custom domain in Render dashboard
3. **Monitoring**: Set up alerts for health check failures
4. **Scaling**: Monitor usage and upgrade plan if needed

## Support

- **Render Docs**: https://render.com/docs
- **MongoDB Atlas**: https://docs.atlas.mongodb.com/
- **Issues**: Check logs in Render dashboard first
