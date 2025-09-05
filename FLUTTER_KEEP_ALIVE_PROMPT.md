# Flutter App - Keep Render Server Alive Implementation

## Prompt for Flutter AI Agent

I need you to help me implement a keep-alive system in my Flutter app to prevent my Render.com backend server from sleeping due to inactivity. Here are the requirements:

### 📋 Requirements

1. **Background Keep-Alive Service**: Call the server every 14 minutes to prevent the 15-minute sleep timeout
2. **App Launch Wake-Up**: Make an immediate API call when the app starts to wake up the server if it's sleeping
3. **Smart Scheduling**: Only run keep-alive calls when the app is active or in foreground
4. **Error Handling**: Gracefully handle network errors and retry logic
5. **Battery Optimization**: Minimize battery drain while keeping server alive
6. **User Control**: Allow users to enable/disable the keep-alive feature

### 🌐 Backend Server Details

- **Server URL**: `https://your-actual-render-url.onrender.com` (⚠️ **IMPORTANT**: Replace with your actual Render service URL)
- **Health Endpoint**: `GET /health`
- **Expected Response**: JSON with `{"status": "healthy", ...}`
- **Server Sleep Time**: 15 minutes of inactivity
- **Keep-Alive Interval**: Every 14 minutes

**🔍 How to find your actual Render URL:**
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click on your `education-platform-api` service
3. Copy the service URL from the dashboard
4. Replace the placeholder URL above with your actual URL

### 🛠 Implementation Requirements

#### 1. Background Service/Timer
```dart
// Create a background timer that:
// - Runs every 14 minutes (840 seconds)
// - Only when app is in foreground or background (not terminated)
// - Calls the health endpoint
// - Handles timeouts and retries
```

#### 2. App Lifecycle Management
```dart
// Implement AppLifecycleState handling:
// - On app resume: Immediate wake-up call
// - On app pause: Continue keep-alive in background
// - On app detach: Stop keep-alive timer
```

#### 3. API Service Class
```dart
// Create a KeepAliveService class with:
// - HTTP client for API calls
// - Timeout handling (30 seconds)
// - Retry logic (3 attempts)
// - Connection status tracking
// - Error logging
```

#### 4. User Settings
```dart
// Add settings to control:
// - Enable/disable keep-alive feature
// - Show connection status in UI
// - Display last successful ping time
// - Battery optimization warnings
```

#### 5. UI Indicators
```dart
// Show in the app:
// - Server status indicator (green/red/yellow)
// - Last ping timestamp
// - Keep-alive toggle switch
// - Connection error messages
```

### 📱 Flutter Packages Needed

Please use these packages in the implementation:
```yaml
dependencies:
  http: ^1.1.0                    # For API calls
  shared_preferences: ^2.2.2      # For storing settings
  connectivity_plus: ^5.0.1       # For network connectivity
  workmanager: ^0.5.2            # For background tasks (Android)
  
dev_dependencies:
  flutter_lints: ^3.0.0
```

### 🔧 Code Structure

Create these files:
1. `lib/services/keep_alive_service.dart` - Main keep-alive logic
2. `lib/services/api_client.dart` - HTTP client wrapper
3. `lib/models/server_status.dart` - Data models
4. `lib/widgets/server_status_widget.dart` - UI component
5. `lib/screens/settings_screen.dart` - Settings page

### ⚡ Key Features to Implement

#### Immediate Wake-Up on App Start
```dart
// When app launches:
// 1. Check if server needs wake-up
// 2. Show loading indicator
// 3. Call health endpoint
// 4. Update UI based on response
// 5. Start keep-alive timer
```

#### Smart Background Management
```dart
// Background behavior:
// - Use WorkManager for Android background tasks
// - Use Timer for iOS when app is active
// - Respect battery optimization settings
// - Handle network changes gracefully
```

#### Error Handling & Retry Logic
```dart
// Error scenarios to handle:
// - Network timeout (30s)
// - Server errors (5xx)
// - No internet connection
// - Server sleeping (slow response)
// - Rate limiting
```

#### User Experience
```dart
// UI/UX considerations:
// - Non-intrusive operation
// - Clear status indicators
// - Minimal battery impact
// - Optional notifications
// - Settings persistence
```

### 🎯 Example Implementation Pattern

Show me how to:
1. **Create the KeepAliveService** with proper timer management
2. **Integrate with app lifecycle** (AppLifecycleState)
3. **Handle background execution** (WorkManager for Android)
4. **Create a status widget** showing server connectivity
5. **Add settings screen** for user control
6. **Implement error handling** with exponential backoff
7. **Add logging** for debugging issues

### 📊 Success Metrics

The implementation should achieve:
- ✅ Server stays alive during app usage
- ✅ Automatic wake-up when app opens
- ✅ Battery usage < 2% per day
- ✅ Graceful handling of network issues
- ✅ User can control the feature
- ✅ Clear status indicators in UI

### 🔍 Testing Requirements

Help me test:
1. **Timer accuracy**: Verify 14-minute intervals
2. **Wake-up speed**: Server response time after sleep
3. **Battery impact**: Monitor battery usage
4. **Network resilience**: Handle poor connectivity
5. **Background behavior**: Test with app in background

### 💡 Additional Considerations

- **Platform differences**: Handle iOS vs Android background limitations
- **Production readiness**: Add proper error reporting
- **Scalability**: Support multiple server endpoints if needed
- **Security**: Don't expose sensitive server details in logs
- **Performance**: Minimize impact on app startup time

Please provide a complete, production-ready implementation with proper error handling, user controls, and clear documentation. Include code comments explaining the keep-alive strategy and any platform-specific considerations.

---

**🔍 Finding Your Current Server Details:**
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Find your `education-platform-api` service 
3. Copy the actual service URL (format: `https://service-name-xxxx.onrender.com`)
4. Test these endpoints to verify they're working:
   - Health Endpoint: `https://your-actual-url.onrender.com/health`
   - Expected Response: `{"status": "healthy", "message": "All services are operational"}`
   - Sleep Timeout: 15 minutes
   - Keep-Alive Interval: 14 minutes

**⚠️ Important**: The URL `education-platform-api.onrender.com` is a placeholder. Your actual URL will be different!
