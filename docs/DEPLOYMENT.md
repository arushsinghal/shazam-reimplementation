# Deployment Guide

Complete guide for deploying the Shazam Clone application to production.

## Table of Contents
1. [Local Development](#local-development)
2. [Production Setup](#production-setup)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Local Development

### Quick Start

```bash
# Clone/navigate to project
cd /Users/arushsinghal/Documents/shazam

# Run the start script
./start.sh
```

The script will:
1. Install backend dependencies
2. Start backend on port 8000
3. Install frontend dependencies
4. Start frontend on port 3000

### Manual Start

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python app.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## Production Setup

### Backend Production

#### 1. Install Production Server

```bash
pip install gunicorn
```

#### 2. Create Gunicorn Configuration

Create `backend/gunicorn_config.py`:

```python
import multiprocessing

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = 120
keepalive = 5

# Logging
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"

# Process naming
proc_name = "shazam-clone-api"

# Server mechanics
daemon = False
pidfile = "gunicorn.pid"
```

#### 3. Run Production Server

```bash
cd backend
mkdir logs
gunicorn -c gunicorn_config.py app:app
```

### Frontend Production

#### 1. Build for Production

```bash
cd frontend
npm run build
```

#### 2. Start Production Server

```bash
npm start
```

Or use PM2 for process management:

```bash
npm install -g pm2
pm2 start npm --name "shazam-frontend" -- start
pm2 save
pm2 startup
```

---

## Docker Deployment

### Backend Dockerfile

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy core modules
COPY ../fingerprinting.py ../database.py ../matcher.py ../utils.py ../config.py ./

# Copy backend files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port
EXPOSE 8000

# Run with gunicorn
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "app:app"]
```

### Frontend Dockerfile

Create `frontend/Dockerfile`:

```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production image
FROM node:18-alpine

WORKDIR /app

COPY --from=builder /app/package*.json ./
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules

EXPOSE 3000

CMD ["npm", "start"]
```

### Docker Compose

Create `docker-compose.yml` in project root:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    ports:
      - "8000:8000"
    volumes:
      - ./fingerprint_db.pkl:/app/fingerprint_db.pkl
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped

  frontend:
    build:
      context: frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  db-data:
```

### Build and Run

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## Cloud Deployment

### Option 1: AWS (EC2)

#### 1. Launch EC2 Instance

- **Instance Type:** t3.medium or larger
- **OS:** Ubuntu 22.04 LTS
- **Storage:** 20GB+ SSD
- **Security Group:**
  - Port 22 (SSH)
  - Port 80 (HTTP)
  - Port 443 (HTTPS)
  - Port 8000 (Backend API)

#### 2. Setup Server

```bash
# Connect to instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3-pip nodejs npm nginx

# Clone/upload project
git clone <your-repo>
cd shazam

# Setup backend
cd backend
pip3 install -r requirements.txt

# Setup frontend
cd ../frontend
npm install
npm run build

# Setup Nginx reverse proxy (see below)
```

#### 3. Nginx Configuration

Create `/etc/nginx/sites-available/shazam`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        client_max_body_size 50M;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/shazam /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 4. Setup SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

#### 5. Setup PM2 for Process Management

```bash
# Install PM2
sudo npm install -g pm2

# Start backend
cd backend
pm2 start app.py --name shazam-backend --interpreter python3

# Start frontend
cd ../frontend
pm2 start npm --name shazam-frontend -- start

# Save and enable startup
pm2 save
pm2 startup
```

### Option 2: DigitalOcean (App Platform)

1. **Create App**
2. **Add Backend Component:**
   - Source: GitHub repo
   - Build: `pip install -r backend/requirements.txt`
   - Run: `cd backend && gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app`
3. **Add Frontend Component:**
   - Source: GitHub repo
   - Build: `cd frontend && npm install && npm run build`
   - Run: `cd frontend && npm start`

### Option 3: Heroku

#### Backend (Procfile):
```
web: cd backend && gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app
```

#### Frontend (Procfile):
```
web: cd frontend && npm start
```

### Option 4: Vercel (Frontend Only)

```bash
cd frontend
vercel deploy --prod
```

Update `.env.production`:
```
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

---

## Monitoring & Maintenance

### Health Checks

Add to crontab:
```bash
*/5 * * * * curl -f http://localhost:8000/api/health || systemctl restart shazam-backend
```

### Logging

**Backend:**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
```

**Monitor logs:**
```bash
tail -f backend/logs/app.log
pm2 logs shazam-backend
```

### Database Backups

Automated backup script:

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups"
DB_FILE="/app/fingerprint_db.pkl"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
cp $DB_FILE $BACKUP_DIR/fingerprint_db_$DATE.pkl

# Keep only last 7 days
find $BACKUP_DIR -name "fingerprint_db_*.pkl" -mtime +7 -delete

echo "Backup completed: fingerprint_db_$DATE.pkl"
```

Add to crontab:
```bash
0 2 * * * /path/to/backup.sh
```

### Performance Monitoring

Install monitoring tools:

```bash
# System monitoring
sudo apt install htop iotop

# Application monitoring
pip install prometheus-fastapi-instrumentator
```

Add to backend:
```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

### Scaling Considerations

**Horizontal Scaling:**
- Load balance multiple backend instances
- Use Redis for shared session storage
- External database (PostgreSQL) for fingerprints

**Vertical Scaling:**
- Increase worker processes
- Add more RAM for larger databases
- Use SSD for faster I/O

---

## Troubleshooting

### Backend won't start

```bash
# Check Python version
python3 --version  # Should be 3.9+

# Check dependencies
pip list | grep -E "fastapi|librosa|numpy"

# Check logs
cat logs/error.log
```

### Frontend build fails

```bash
# Clear cache
rm -rf .next node_modules
npm install
npm run build
```

### Database issues

```bash
# Check database file
ls -lh fingerprint_db.pkl

# Test loading
python3 -c "import pickle; pickle.load(open('fingerprint_db.pkl', 'rb'))"
```

### High memory usage

```bash
# Check memory
free -h

# Reduce workers
# In gunicorn_config.py: workers = 2
```

---

## Security Checklist

- [ ] Enable HTTPS with valid SSL certificate
- [ ] Configure firewall (UFW or Security Groups)
- [ ] Add rate limiting to API
- [ ] Implement authentication
- [ ] Sanitize file uploads
- [ ] Set max file upload size
- [ ] Regular security updates
- [ ] Backup database regularly
- [ ] Monitor logs for suspicious activity
- [ ] Use environment variables for secrets

---

## Cost Estimation

### AWS EC2 (t3.medium)
- Instance: $30/month
- Storage (50GB): $5/month
- Bandwidth: ~$9/100GB
- **Total: ~$45/month**

### DigitalOcean (Basic Droplet)
- 2 vCPU, 4GB RAM: $24/month
- Storage included
- Bandwidth: 4TB free
- **Total: ~$25/month**

### Heroku
- Hobby dynos × 2: $14/month
- **Total: ~$15/month**

---

## Next Steps

1. Choose deployment method
2. Set up domain and SSL
3. Configure environment variables
4. Deploy and test
5. Set up monitoring
6. Configure backups
7. Add custom domain
8. Optimize for scale

For questions or issues, refer to logs and troubleshooting section.
