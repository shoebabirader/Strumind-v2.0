# 🔄 How to Restart the Backend Server

## Quick Restart Instructions

### Step 1: Stop the Current Backend
In the terminal where the backend is running:
- Press `CTRL+C` to stop the server

### Step 2: Start the Backend Again
```bash
cd backend
python start.py
```

## Alternative: One-Command Restart

If you want to restart with fresh dependencies:

```bash
cd backend
pip install -r requirements.txt
python start.py
```

## What You Should See

When the backend starts successfully, you'll see:
```
🚀 Starting StruMind Backend Server...
📍 Server will be available at: http://localhost:8000
📚 API Documentation: http://localhost:8000/docs
🔧 Health Check: http://localhost:8000/health
⚠️  Press CTRL+C to stop the server

INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [XXXX] using WatchFiles
INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
INFO:     Starting StruMind API...
INFO:     StruMind API started successfully
✅ Database tables created successfully
INFO:     Application startup complete.
```

## Verify It's Working

Test the health endpoint:
```powershell
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0-beta",
  "rate_limit": "100 requests/minute"
}
```

## Test Registration

```powershell
curl -Method POST -Uri "http://localhost:8000/api/auth/register" `
  -ContentType "application/json" `
  -Body '{"username":"testuser","email":"test@test.com","password":"test123","full_name":"Test User"}'
```

## After Restart

Once the backend is running:
1. Frontend at http://localhost:3000 will connect automatically
2. You can register new users
3. You can login with demo credentials (username: `demo`, password: `demo123`)

---

**Current Issue**: Backend needs restart to load bcrypt 4.1.3
**Solution**: Follow steps above to restart
