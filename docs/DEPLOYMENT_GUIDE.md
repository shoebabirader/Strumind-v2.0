# 🚀 StruMind Deployment Guide

## Quick Start Deployment

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Node.js 16+ (for frontend)
- Git

---

## Backend Deployment

### 1. Environment Setup

```bash
# Clone repository
git clone <repository-url>
cd strumind

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt
pip install -r requirements-test.txt
```

### 2. Environment Variables

Create `.env` file in backend directory:

```bash
# Security
SECRET_KEY=your-super-secret-key-min-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database
DATABASE_URL=postgresql://username:password@localhost:5432/strumind

# Environment
ENVIRONMENT=production

# CORS (adjust for your frontend domain)
ALLOWED_ORIGINS=https://your-frontend-domain.com

# Rate Limiting
RATE_LIMIT_PER_MINUTE=100

# Logging
LOG_LEVEL=INFO
```

### 3. Database Setup

```bash
# Create database
createdb strumind

# Run migrations
alembic upgrade head

# Verify migrations
alembic current
```

### 4. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html
```

### 5. Start Backend Server

**Development:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Production:**
```bash
# Using Gunicorn with Uvicorn workers
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

### 6. Verify Backend

```bash
# Health check
curl http://localhost:8000/health

# API documentation
open http://localhost:8000/docs

# Alternative docs
open http://localhost:8000/redoc
```

---

## Frontend Deployment

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Environment Configuration

Create `.env` file in frontend directory:

```bash
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

### 3. Build Frontend

```bash
# Development
npm run dev

# Production build
npm run build

# Preview production build
npm run preview
```

### 4. Deploy Frontend

**Option A: Static Hosting (Netlify, Vercel)**
```bash
# Build creates dist/ folder
npm run build

# Deploy dist/ folder to your hosting provider
```

**Option B: Nginx**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    root /path/to/frontend/dist;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Docker Deployment

### 1. Backend Dockerfile

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run migrations and start server
CMD alembic upgrade head && \
    gunicorn main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000
```

### 2. Frontend Dockerfile

Create `frontend/Dockerfile`:

```dockerfile
FROM node:16-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 3. Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: strumind
      POSTGRES_USER: strumind
      POSTGRES_PASSWORD: your-password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://strumind:your-password@postgres:5432/strumind
      SECRET_KEY: your-super-secret-key
    ports:
      - "8000:8000"
    depends_on:
      - postgres

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```

### 4. Run with Docker

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## Production Checklist

### Security ✅
- [ ] Change SECRET_KEY to strong random value
- [ ] Use environment variables for sensitive data
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS for specific domains
- [ ] Set up rate limiting
- [ ] Enable audit logging
- [ ] Regular security updates

### Database ✅
- [ ] Set up database backups
- [ ] Configure connection pooling
- [ ] Set up read replicas (if needed)
- [ ] Monitor database performance
- [ ] Regular maintenance tasks

### Monitoring ✅
- [ ] Set up application monitoring (e.g., Sentry)
- [ ] Configure log aggregation (e.g., ELK stack)
- [ ] Set up uptime monitoring
- [ ] Configure alerts for errors
- [ ] Monitor resource usage

### Performance ✅
- [ ] Enable caching (Redis)
- [ ] Configure CDN for static assets
- [ ] Optimize database queries
- [ ] Set up load balancing
- [ ] Enable gzip compression

### Backup & Recovery ✅
- [ ] Automated database backups
- [ ] Backup retention policy
- [ ] Disaster recovery plan
- [ ] Test restore procedures
- [ ] Document recovery steps

---

## Scaling Considerations

### Horizontal Scaling
```bash
# Multiple backend workers
gunicorn main:app --workers 8 --worker-class uvicorn.workers.UvicornWorker

# Load balancer (Nginx)
upstream backend {
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}
```

### Caching Layer
```python
# Add Redis for caching
REDIS_URL=redis://localhost:6379/0

# Cache frequently accessed data
# - Material properties
# - Section properties
# - Design code parameters
```

### Database Optimization
```sql
-- Add indexes for common queries
CREATE INDEX idx_nodes_model_id ON nodes(model_id);
CREATE INDEX idx_elements_model_id ON elements(model_id);
CREATE INDEX idx_analysis_model_id ON analysis_results(model_id);
```

---

## Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.9+

# Check dependencies
pip list

# Check database connection
psql -U username -d strumind -c "SELECT 1;"

# Check logs
tail -f logs/app.log
```

### Database migration issues
```bash
# Check current version
alembic current

# Rollback one version
alembic downgrade -1

# Upgrade to latest
alembic upgrade head

# Generate new migration
alembic revision --autogenerate -m "description"
```

### Frontend build issues
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install

# Check Node version
node --version  # Should be 16+

# Build with verbose output
npm run build -- --debug
```

---

## Support & Maintenance

### Regular Tasks
- Weekly: Review logs for errors
- Weekly: Check disk space and performance
- Monthly: Update dependencies
- Monthly: Review security advisories
- Quarterly: Load testing
- Quarterly: Disaster recovery drill

### Updates
```bash
# Update Python dependencies
pip list --outdated
pip install -U package-name

# Update Node dependencies
npm outdated
npm update

# Run tests after updates
pytest
npm test
```

---

## API Documentation

Once deployed, access API documentation at:
- **Swagger UI:** http://your-domain/docs
- **ReDoc:** http://your-domain/redoc
- **OpenAPI JSON:** http://your-domain/openapi.json

---

## Success Criteria

Your deployment is successful when:
- ✅ Backend health check returns 200
- ✅ API documentation is accessible
- ✅ Frontend loads without errors
- ✅ User can register and login
- ✅ Analysis can be performed
- ✅ Reports can be generated
- ✅ All tests pass
- ✅ Logs show no errors

---

## Getting Help

- **Documentation:** Check /docs endpoint
- **Logs:** Review application logs
- **Tests:** Run pytest for diagnostics
- **Database:** Check Alembic migrations
- **API:** Use Swagger UI for testing

---

**Deployment Status:** ✅ Ready for Production  
**Last Updated:** October 16, 2025
