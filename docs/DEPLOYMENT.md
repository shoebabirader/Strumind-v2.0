# StruMind Deployment Guide

## Prerequisites

- Docker & Docker Compose
- Kubernetes cluster (for production)
- kubectl configured
- PostgreSQL 15
- Python 3.11+
- Node.js 20+

## Local Development

### 1. Clone Repository
```bash
git clone https://github.com/yourorg/strumind.git
cd strumind
```

### 2. Environment Setup

**Backend:**
```bash
cd backend
cp .env.example .env
# Edit .env with your configuration
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### 3. Database Setup
```bash
docker run -d \
  --name strumind-postgres \
  -e POSTGRES_DB=strumind \
  -e POSTGRES_USER=strumind_user \
  -e POSTGRES_PASSWORD=strumind_pass \
  -p 5432:5432 \
  postgres:15
```

### 4. Run Services

**Backend:**
```bash
cd backend
python main.py
# API available at http://localhost:8000
```

**Frontend:**
```bash
cd frontend
npm run dev
# App available at http://localhost:3000
```

## Docker Compose Deployment

### 1. Build and Start
```bash
docker-compose up --build
```

### 2. Access Services
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432

### 3. Stop Services
```bash
docker-compose down
```

### 4. Clean Volumes
```bash
docker-compose down -v
```

## Kubernetes Deployment

### 1. Create Namespace
```bash
kubectl create namespace strumind
kubectl config set-context --current --namespace=strumind
```

### 2. Configure Secrets
```bash
# Edit kubernetes/secrets.yaml with production values
kubectl apply -f kubernetes/secrets.yaml
```

### 3. Deploy PostgreSQL
```bash
kubectl apply -f kubernetes/pvc.yaml
kubectl apply -f kubernetes/postgres-deployment.yaml
```

### 4. Deploy Application
```bash
kubectl apply -f kubernetes/deployment.yaml
```

### 5. Verify Deployment
```bash
kubectl get pods
kubectl get services
kubectl logs -f deployment/strumind-backend
```

### 6. Access Application
```bash
# Get external IP
kubectl get service strumind-backend-service

# Or use port forwarding
kubectl port-forward service/strumind-backend-service 8000:80
```

## AWS Deployment

### 1. EKS Cluster Setup
```bash
eksctl create cluster \
  --name strumind-cluster \
  --region us-east-1 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 3 \
  --nodes-min 1 \
  --nodes-max 5
```

### 2. RDS PostgreSQL
```bash
aws rds create-db-instance \
  --db-instance-identifier strumind-db \
  --db-instance-class db.t3.medium \
  --engine postgres \
  --engine-version 15.3 \
  --master-username admin \
  --master-user-password <password> \
  --allocated-storage 100
```

### 3. S3 for ML Models
```bash
aws s3 mb s3://strumind-ml-models
aws s3 mb s3://strumind-exports
```

### 4. Update Secrets
```bash
kubectl create secret generic strumind-secrets \
  --from-literal=database-url="postgresql://admin:<password>@<rds-endpoint>:5432/strumind" \
  --from-literal=jwt-secret="<random-secret>" \
  --from-literal=aws-access-key="<key>" \
  --from-literal=aws-secret-key="<secret>"
```

### 5. Deploy to EKS
```bash
kubectl apply -f kubernetes/deployment.yaml
```

## Monitoring Setup

### 1. Install Prometheus
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack
```

### 2. Access Grafana
```bash
kubectl port-forward service/prometheus-grafana 3000:80
# Default credentials: admin/prom-operator
```

### 3. Import Dashboards
- Import dashboard ID: 1860 (Node Exporter)
- Import dashboard ID: 6417 (Kubernetes Cluster)
- Create custom dashboard for StruMind metrics

## CI/CD Pipeline

### GitHub Actions
The pipeline automatically:
1. Runs tests on push/PR
2. Builds Docker images
3. Pushes to registry (on main branch)
4. Deploys to staging (optional)

### Manual Deployment
```bash
# Build images
docker build -t strumind/backend:v1.0.0 ./backend
docker build -t strumind/frontend:v1.0.0 ./frontend

# Push to registry
docker push strumind/backend:v1.0.0
docker push strumind/frontend:v1.0.0

# Update Kubernetes
kubectl set image deployment/strumind-backend backend=strumind/backend:v1.0.0
```

## Scaling

### Horizontal Pod Autoscaler
```bash
kubectl autoscale deployment strumind-backend \
  --cpu-percent=70 \
  --min=3 \
  --max=10
```

### Database Scaling
- Enable read replicas in RDS
- Configure connection pooling (PgBouncer)
- Implement caching layer (Redis)

## Backup & Recovery

### Database Backup
```bash
# Automated backups in RDS
aws rds modify-db-instance \
  --db-instance-identifier strumind-db \
  --backup-retention-period 7 \
  --preferred-backup-window "03:00-04:00"
```

### ML Model Backup
```bash
# Sync to S3
aws s3 sync ./ml_models s3://strumind-ml-models/backup/
```

## Troubleshooting

### Check Logs
```bash
kubectl logs -f deployment/strumind-backend
kubectl logs -f deployment/postgres
```

### Database Connection Issues
```bash
kubectl exec -it deployment/strumind-backend -- python -c "from app.core.database import engine; print(engine.connect())"
```

### Pod Not Starting
```bash
kubectl describe pod <pod-name>
kubectl get events --sort-by=.metadata.creationTimestamp
```

## Health Checks

### API Health
```bash
curl http://localhost:8000/health
```

### Database Health
```bash
kubectl exec -it deployment/postgres -- psql -U strumind_user -d strumind -c "SELECT 1"
```

## Performance Tuning

1. **Database**: Increase connection pool size
2. **Backend**: Enable Gunicorn workers
3. **Frontend**: Enable Next.js caching
4. **Kubernetes**: Adjust resource limits
5. **Network**: Enable CDN for static assets
