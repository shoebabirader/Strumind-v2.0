# 🚀 How to Start StruMind Servers

## ⚠️ IMPORTANT: You Need BOTH Servers Running!

The 404 errors you're seeing are because the **backend server is not running**.

---

## 📋 Step-by-Step Instructions

### Step 1: Start Backend Server (REQUIRED)

Open a terminal and run:

```bash
cd backend
python start.py
```

**Expected Output:**
```
🚀 Starting StruMind Backend Server...
📍 Server will be available at: http://localhost:8000
📚 API Documentation: http://localhost:8000/docs
🔧 Health Check: http://localhost:8000/health

⚠️  Press CTRL+C to stop the server

INFO:     Will watch for changes in these directories: ['C:\\Users\\hp\\wisal2\\backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
✅ Database tables created successfully
INFO:     Application startup complete.
```

**✅ Backend is Ready When You See:**
- `Uvicorn running on http://0.0.0.0:8000`
- `Application startup complete`

---

### Step 2: Verify Backend is Running

Open your browser and go to:
**http://localhost:8000/health**

**Expected Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0-beta",
  "rate_limit": "100 requests/minute"
}
```

If you see this, backend is working! ✅

---

### Step 3: Start Frontend (In a NEW Terminal)

**IMPORTANT:** Keep the backend terminal running! Open a **NEW** terminal:

```bash
cd frontend
npm run dev
```

**Expected Output:**
```
  ▲ Next.js 15.5.5
  - Local:        http://localhost:3000
  - Network:      http://192.168.x.x:3000

 ✓ Starting...
 ✓ Ready in 2.5s
```

---

### Step 4: Access the Application

Open your browser and go to:
**http://localhost:3000**

Now all API calls should work! ✅

---

## 🔍 Troubleshooting 404 Errors

### Problem: "Request failed with status code 404"

**Cause:** Backend server is not running

**Solution:**
1. Check if backend terminal is still running
2. Check if you can access http://localhost:8000/health
3. If not, restart backend: `cd backend && python start.py`

---

### Problem: "Network Error" or "ERR_CONNECTION_REFUSED"

**Cause:** Backend server crashed or not started

**Solution:**
1. Go to backend terminal
2. Look for error messages
3. Restart: `python start.py`

---

### Problem: Backend starts but crashes immediately

**Cause:** Port 8000 might be in use

**Solution:**
```bash
# Check what's using port 8000
netstat -ano | findstr :8000

# Kill the process or use a different port
python -m uvicorn main:app --reload --port 8001
```

Then update frontend `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8001/api
```

---

## 📊 Quick Status Check

### Is Backend Running?
```bash
curl http://localhost:8000/health
```
✅ If you get JSON response → Backend is running
❌ If you get error → Backend is NOT running

### Is Frontend Running?
Open browser to http://localhost:3000
✅ If page loads → Frontend is running
❌ If "can't reach" → Frontend is NOT running

---

## 🎯 Common Mistakes

1. ❌ **Only starting frontend** → Will get 404 errors
2. ❌ **Closing backend terminal** → Backend stops, 404 errors
3. ❌ **Wrong directory** → Make sure you're in `backend/` folder
4. ❌ **Port conflicts** → Check if ports 8000/3000 are free

---

## ✅ Correct Setup

You should have **TWO terminals open**:

**Terminal 1 (Backend):**
```
C:\Users\hp\wisal2\backend> python start.py
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Terminal 2 (Frontend):**
```
C:\Users\hp\wisal2\frontend> npm run dev
▲ Next.js 15.5.5
- Local:        http://localhost:3000
✓ Ready in 2.5s
```

---

## 🌐 URLs to Remember

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 💡 Pro Tips

1. **Keep both terminals visible** so you can see errors
2. **Check backend terminal** when you get 404 errors
3. **Use API docs** at http://localhost:8000/docs to test endpoints
4. **Browser DevTools** (F12) → Network tab to see API calls

---

**Status**: Ready to start! 🚀
**Next Step**: Run `cd backend && python start.py` in a terminal
