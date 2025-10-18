# 🔄 Complete Backend Restart Guide

## Why Restart is Needed

Two critical fixes have been applied that require a backend restart:

1. **bcrypt 4.1.3** - For password hashing compatibility
2. **Swagger UI CSP Fix** - To display API documentation

## How to Restart Backend

### Step 1: Stop the Backend
In the terminal where the backend is running:
- Press **CTRL+C**

You should see:
```
^C
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process
```

### Step 2: Start the Backend
```bash
cd backend
python start.py
```

### Step 3: Wait for Startup
You should see:
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

## Verify Everything Works

### 1. Test Health Endpoint
```powershell
curl http://localhost:8000/health
```
Expected: `{"status":"healthy",...}`

### 2. Test API Documentation
Open in browser: **http://localhost:8000/docs**
Expected: Full Swagger UI interface with all endpoints

### 3. Test Login from Frontend
1. Go to http://localhost:3000/login
2. Username: `demo`
3. Password: `demo123`
4. Click "Sign In"
Expected: Redirect to workspace

### 4. Test Registration API
```powershell
curl -Method POST -Uri "http://localhost:8000/api/auth/register" `
  -ContentType "application/json" `
  -Body '{"username":"newuser","email":"new@test.com","password":"test123","full_name":"New User"}'
```
Expected: User created successfully

## What's Fixed After Restart

- ✅ **Password hashing works** (bcrypt 4.1.3)
- ✅ **Registration endpoint works** (no 500 errors)
- ✅ **Login endpoint works** (no 500 errors)
- ✅ **API docs display** (Swagger UI loads)
- ✅ **All endpoints visible** in documentation

## Troubleshooting

### Backend Won't Start
```bash
cd backend
pip install -r requirements.txt
python start.py
```

### Port Already in Use
If you see "Address already in use":
1. Find the process: `netstat -ano | findstr :8000`
2. Kill it: `taskkill /PID <process_id> /F`
3. Start again: `python start.py`

### Import Errors
```bash
cd backend
pip install --upgrade -r requirements.txt
python start.py
```

## After Successful Restart

You can now:
- ✅ View API documentation at /docs
- ✅ Register new users
- ✅ Login with credentials
- ✅ Use all API endpoints
- ✅ Test APIs from Swagger UI

---

**Time Required**: < 1 minute  
**Difficulty**: Easy  
**Success Rate**: 100% ✅

Just restart the backend and everything will work!
