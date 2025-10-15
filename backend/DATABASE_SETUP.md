# 🗄️ Database Setup Guide

## ✅ **ALREADY CONFIGURED!**

Your database is **already set up and working** with SQLite!

---

## 📊 Current Configuration

**Database Type:** SQLite (file-based, no installation needed)  
**Database File:** `backend/strumind.db`  
**Status:** ✅ **Working**

**Tables Created:**
- ✅ `projects` - Store project information
- ✅ `models` - Store structural models
- ✅ `analysis_results` - Store analysis results

---

## 🚀 Quick Start

### Option 1: Just Run It (Recommended)
```bash
cd backend
python main.py
```

The database is already configured and will work automatically!

### Option 2: Reset/Reinitialize Database
```bash
cd backend
python setup_database.py
```

---

## 🔧 Configuration Options

### Current Setup (SQLite - Default)
**File:** `backend/.env`
```
DATABASE_URL=sqlite:///./strumind.db
```

**Advantages:**
- ✅ No installation needed
- ✅ Works immediately
- ✅ Perfect for development
- ✅ Easy to backup (just copy the file)
- ✅ No server to manage

**Limitations:**
- ⚠️ Single file (not for high concurrency)
- ⚠️ Not ideal for production with many users

---

### Production Setup (PostgreSQL - Optional)

If you need PostgreSQL for production:

#### Step 1: Install PostgreSQL
```bash
# Windows (using Chocolatey)
choco install postgresql

# Or download from: https://www.postgresql.org/download/
```

#### Step 2: Create Database
```bash
# Open PostgreSQL command line
psql -U postgres

# Create database and user
CREATE DATABASE strumind;
CREATE USER strumind_user WITH PASSWORD 'strumind_pass';
GRANT ALL PRIVILEGES ON DATABASE strumind TO strumind_user;
\q
```

#### Step 3: Update Configuration
Edit `backend/.env`:
```
DATABASE_URL=postgresql://strumind_user:strumind_pass@localhost:5432/strumind
```

#### Step 4: Initialize
```bash
cd backend
python setup_database.py
```

---

## 📋 Database Commands

### Check Database Status
```bash
cd backend
python -c "from app.core.database import init_db; init_db()"
```

### View Database Contents (SQLite)
```bash
cd backend
sqlite3 strumind.db
.tables
.schema projects
.quit
```

### Backup Database (SQLite)
```bash
cd backend
copy strumind.db strumind_backup.db
```

### Reset Database
```bash
cd backend
del strumind.db
python setup_database.py
```

---

## 🎯 What Works Now

With the database configured, you can now use:

### ✅ **Working Features:**
1. **Project Management**
   - Create projects
   - List projects
   - Get project details
   - Delete projects

2. **Model Storage**
   - Save structural models
   - Load models
   - Model versioning

3. **Analysis Results**
   - Store analysis results
   - Retrieve past analyses
   - Compare results

4. **Collaboration** (when implemented)
   - Multi-user access
   - Comments
   - Version history

---

## 🔍 Verify Setup

### Test 1: Check Database File
```bash
cd backend
dir strumind.db
```
Should show the database file exists.

### Test 2: Check Tables
```bash
cd backend
python setup_database.py
```
Should show 3 tables created.

### Test 3: Test API
```bash
cd backend
python main.py
```
Then visit: http://localhost:8000/docs

Try the `/api/projects/create` endpoint!

---

## 🐛 Troubleshooting

### Issue: "No such table" error
**Solution:** Run database setup
```bash
cd backend
python setup_database.py
```

### Issue: "Database is locked"
**Solution:** Close any programs accessing the database
```bash
cd backend
del strumind.db
python setup_database.py
```

### Issue: Want to switch to PostgreSQL
**Solution:** Follow "Production Setup" section above

---

## 📊 Database Schema

### Projects Table
```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY,
    name VARCHAR,
    client VARCHAR,
    location VARCHAR,
    created_at DATETIME
);
```

### Models Table
```sql
CREATE TABLE models (
    id INTEGER PRIMARY KEY,
    project_id INTEGER,
    geometry_data JSON,
    materials JSON,
    sections JSON,
    created_at DATETIME,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);
```

### Analysis Results Table
```sql
CREATE TABLE analysis_results (
    id INTEGER PRIMARY KEY,
    model_id INTEGER,
    analysis_type VARCHAR,
    results JSON,
    created_at DATETIME,
    FOREIGN KEY (model_id) REFERENCES models(id)
);
```

---

## ✅ Summary

**Current Status:** ✅ **CONFIGURED AND WORKING**

- ✅ Database file created: `strumind.db`
- ✅ Tables initialized: 3 tables
- ✅ Configuration file: `.env` created
- ✅ Setup script: `setup_database.py` available

**You're ready to use all database features!**

---

## 🚀 Next Steps

1. ✅ Database is configured
2. ⏭️ Run the backend: `python main.py`
3. ⏭️ Test the API: http://localhost:8000/docs
4. ⏭️ Create your first project!

**Everything is ready to go! 🎉**
