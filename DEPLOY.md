# Deployment Guide for Render

This guide will help you deploy the NoSQL Education Backend to Render.

## 🚀 Quick Deploy to Render

### Method 1: One-Click Deploy (Recommended)

1. **Fork/Push to GitHub**:
   - Push your `nosql_backend` folder to a GitHub repository
   - Make sure all files are committed

2. **Deploy to Render**:
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Select the repository containing your `nosql_backend` folder

3. **Configuration**:
   - **Name**: `education-backend-nosql`
   - **Environment**: `Python 3`
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Root Directory**: `nosql_backend` (if not in root)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`

4. **Environment Variables**:
   Add these in Render dashboard:
   ```
   MONGODB_URI = mongodb+srv://sudhanshu:Sudha%407250@cluster0.pmdxjrt.mongodb.net/
   DATABASE_NAME = education_platform
   FLASK_ENV = production
   FLASK_DEBUG = False
   PORT = 10000
   HOST = 0.0.0.0
   SECRET_KEY = [Render will auto-generate]
   ```

### Method 2: Using render.yaml (Infrastructure as Code)

1. **Use render.yaml**:
   - The `render.yaml` file is already configured
   - Just set your MongoDB URI in Render dashboard

2. **Deploy**:
   - Push code to GitHub
   - Connect GitHub to Render
   - Render will automatically use `render.yaml` configuration

## 🔧 Environment Variables Required

| Variable | Value | Description |
|----------|--------|-------------|
| `MONGODB_URI` | `mongodb+srv://...` | Your MongoDB Atlas connection string |
| `DATABASE_NAME` | `education_platform` | Database name |
| `FLASK_ENV` | `production` | Flask environment |
| `FLASK_DEBUG` | `False` | Debug mode (off for production) |
| `PORT` | `10000` | Port number (Render default) |
| `HOST` | `0.0.0.0` | Host address |
| `SECRET_KEY` | Auto-generated | Flask secret key |

## 📝 Pre-Deployment Checklist

- [x] MongoDB Atlas connection string updated
- [x] All dependencies in requirements.txt
- [x] Environment variables configured
- [x] Health check endpoint working (`/api/health`)
- [x] CORS enabled for production
- [x] Logging configured
- [x] Error handling implemented

## 🔍 Post-Deployment Testing

After deployment, test these endpoints:

1. **Health Check**:
   ```bash
   curl https://your-app.onrender.com/api/health
   ```

2. **Root Endpoint**:
   ```bash
   curl https://your-app.onrender.com/
   ```

3. **Service Status**:
   ```bash
   curl https://your-app.onrender.com/api/services
   ```

4. **Career Assessment**:
   ```bash
   curl -X POST https://your-app.onrender.com/api/career/start-assessment \
        -H "Content-Type: application/json" \
        -d '{"user_id": "test_user"}'
   ```

## 🛠 Troubleshooting

### Common Issues:

1. **Build Fails**:
   - Check `requirements.txt` format
   - Ensure all dependencies are compatible
   - Check build logs in Render dashboard

2. **Database Connection Fails**:
   - Verify MongoDB URI is correct
   - Check network access in MongoDB Atlas
   - Ensure IP whitelist includes 0.0.0.0/0 for Render

3. **Health Check Fails**:
   - Verify `/api/health` endpoint works locally
   - Check application logs
   - Ensure port 10000 is used

4. **Import Errors**:
   - Make sure all files are uploaded
   - Check file paths are relative
   - Verify Python version compatibility

### Render-Specific Settings:

1. **Auto-Deploy**: Enable auto-deploy from GitHub
2. **Health Check**: Set to `/api/health`
3. **Environment**: Select `Python 3`
4. **Plan**: Free tier is sufficient for development

## 📊 Monitoring

After deployment:

1. **Logs**: Check Render logs for any errors
2. **Metrics**: Monitor response times and uptime
3. **Health**: Set up alerts for health check failures

## 🔒 Security Notes

1. **Environment Variables**: Never commit sensitive data
2. **MongoDB**: Use strong passwords and IP restrictions
3. **CORS**: Configure for your frontend domain in production
4. **HTTPS**: Render provides free SSL certificates

## 📱 Frontend Integration

Your frontend can now connect to:
```
Base URL: https://your-app.onrender.com
API Endpoints: https://your-app.onrender.com/api/
```

Example Flutter/React configuration:
```dart
const String API_BASE_URL = 'https://your-app.onrender.com';
```

## 🎉 Success!

Your NoSQL Education Backend is now live on Render with:
- ✅ MongoDB Atlas integration
- ✅ All 5 microservices (26+ endpoints)
- ✅ RIASEC assessment system
- ✅ Automatic HTTPS
- ✅ Health monitoring
- ✅ Auto-scaling
- ✅ Free hosting (with some limitations)

🚀 **Your backend is ready for production use!**
