# Deployment Guide

## Overview

This guide covers deploying the Research Paper Assistant to various platforms.

## Table of Contents
1. [Local Production Build](#local-production-build)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Environment Configuration](#environment-configuration)
5. [Monitoring and Logs](#monitoring-and-logs)

---

## Local Production Build

### Backend Production Setup

1. **Install dependencies**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure environment**
```bash
cp .env.example .env
# Edit .env with production values
```

3. **Run with Gunicorn (Linux/Mac)**
```bash
pip install gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

4. **Run with Uvicorn (Windows)**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend Production Build

1. **Build for production**
```bash
cd frontend
npm run build
```

2. **Output location**
```
frontend/dist/research-paper-assistant/
```

3. **Serve with web server**

**Using Python HTTP Server:**
```bash
cd frontend/dist/research-paper-assistant
python -m http.server 4200
```

**Using Node.js serve:**
```bash
npm install -g serve
serve -s frontend/dist/research-paper-assistant -l 4200
```

**Using Nginx:**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/frontend/dist/research-paper-assistant;
    
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

### Backend Dockerfile

Create `backend/Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directory for ChromaDB
RUN mkdir -p /app/chroma_db

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile

Create `frontend/Dockerfile`:
```dockerfile
FROM node:18-alpine AS build

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Build application
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built files
COPY --from=build /app/dist/research-paper-assistant /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Nginx Configuration

Create `frontend/nginx.conf`:
```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./backend/chroma_db:/app/chroma_db
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=research_db
      - POSTGRES_USER=research_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

### Build and Run

```bash
# Create .env file
echo "GEMINI_API_KEY=your_key_here" > .env
echo "DB_PASSWORD=secure_password" >> .env

# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## Cloud Deployment

### AWS Deployment

#### Using Elastic Beanstalk

1. **Install EB CLI**
```bash
pip install awsebcli
```

2. **Initialize EB application**
```bash
cd backend
eb init -p python-3.11 research-paper-assistant
```

3. **Create environment**
```bash
eb create production
```

4. **Set environment variables**
```bash
eb setenv GEMINI_API_KEY=your_key_here
```

5. **Deploy**
```bash
eb deploy
```

#### Using EC2

1. **Launch EC2 instance** (Ubuntu 22.04)
2. **Connect via SSH**
3. **Install dependencies**
```bash
sudo apt update
sudo apt install python3-pip nodejs npm nginx
```

4. **Clone and setup project**
```bash
git clone your-repo-url
cd research-paper-assistant
# Follow local production setup
```

5. **Configure Nginx**
```bash
sudo cp nginx.conf /etc/nginx/sites-available/research-app
sudo ln -s /etc/nginx/sites-available/research-app /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

6. **Setup systemd service**

Create `/etc/systemd/system/research-backend.service`:
```ini
[Unit]
Description=Research Paper Assistant Backend
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/research-paper-assistant/backend
Environment="PATH=/home/ubuntu/research-paper-assistant/backend/venv/bin"
ExecStart=/home/ubuntu/research-paper-assistant/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable research-backend
sudo systemctl start research-backend
```

### Google Cloud Platform

#### Using Cloud Run

1. **Build container**
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/research-backend
```

2. **Deploy to Cloud Run**
```bash
gcloud run deploy research-backend \
  --image gcr.io/PROJECT_ID/research-backend \
  --platform managed \
  --region us-central1 \
  --set-env-vars GEMINI_API_KEY=your_key
```

### Heroku Deployment

1. **Create Heroku apps**
```bash
heroku create research-backend
heroku create research-frontend
```

2. **Add buildpacks**
```bash
heroku buildpacks:add heroku/python -a research-backend
heroku buildpacks:add heroku/nodejs -a research-frontend
```

3. **Set environment variables**
```bash
heroku config:set GEMINI_API_KEY=your_key -a research-backend
```

4. **Deploy**
```bash
git push heroku main
```

### Vercel (Frontend Only)

1. **Install Vercel CLI**
```bash
npm i -g vercel
```

2. **Deploy**
```bash
cd frontend
vercel --prod
```

3. **Configure API proxy** in `vercel.json`:
```json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://your-backend-url.com/api/:path*"
    }
  ]
}
```

---

## Environment Configuration

### Production Environment Variables

**Backend (.env):**
```env
# Required
GEMINI_API_KEY=your_production_key
OPENAI_API_KEY=your_production_key

# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Security
SECRET_KEY=generate_a_strong_random_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com

# Logging
LOG_LEVEL=INFO
```

**Frontend (environment.prod.ts):**
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://api.your-domain.com/api'
};
```

### Generating Secure Keys

```python
import secrets
print(secrets.token_urlsafe(32))
```

---

## SSL/HTTPS Setup

### Using Let's Encrypt (Certbot)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal is configured automatically
# Test renewal:
sudo certbot renew --dry-run
```

### Nginx HTTPS Configuration

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Frontend
    location / {
        root /var/www/research-app;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

---

## Monitoring and Logs

### Application Logging

**Backend logging (config in main.py):**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### System Monitoring

**Using PM2 (Node.js process manager):**
```bash
npm install -g pm2

# Start backend
pm2 start "uvicorn main:app --host 0.0.0.0 --port 8000" --name research-backend

# Monitor
pm2 monit

# Logs
pm2 logs research-backend

# Auto-restart on crash
pm2 startup
pm2 save
```

### Health Checks

Add to your deployment:
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check if frontend is accessible
curl http://localhost:4200
```

### Error Tracking

Consider integrating:
- **Sentry** for error tracking
- **LogRocket** for session replay
- **CloudWatch** for AWS deployments
- **Stackdriver** for GCP deployments

---

## Database Migration

### Setting up PostgreSQL

1. **Install PostgreSQL**
```bash
sudo apt install postgresql
```

2. **Create database**
```sql
CREATE DATABASE research_db;
CREATE USER research_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE research_db TO research_user;
```

3. **Update connection string**
```env
DATABASE_URL=postgresql://research_user:secure_password@localhost:5432/research_db
```

---

## Backup Strategy

### Database Backups

```bash
# PostgreSQL backup
pg_dump research_db > backup_$(date +%Y%m%d).sql

# Restore
psql research_db < backup_20260604.sql
```

### Vector Database Backups

```bash
# Backup ChromaDB
tar -czf chroma_backup_$(date +%Y%m%d).tar.gz backend/chroma_db/

# Restore
tar -xzf chroma_backup_20260604.tar.gz
```

---

## Performance Optimization

### Backend Optimization

1. **Enable response caching**
2. **Use connection pooling**
3. **Implement rate limiting**
4. **Optimize database queries**

### Frontend Optimization

1. **Enable compression in Nginx**
```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript;
gzip_min_length 1000;
```

2. **Use CDN for static assets**
3. **Implement lazy loading**
4. **Enable service workers**

---

## Security Checklist

- [ ] HTTPS enabled
- [ ] Environment variables secured
- [ ] CORS properly configured
- [ ] Rate limiting implemented
- [ ] Input validation in place
- [ ] SQL injection prevention
- [ ] XSS protection
- [ ] API keys rotated regularly
- [ ] Firewall configured
- [ ] Regular security updates

---

## Rollback Procedure

### Quick Rollback

```bash
# Docker Compose
docker-compose down
git checkout previous-commit
docker-compose up -d

# Heroku
heroku rollback -a research-backend
```

### Database Rollback

```bash
# Restore from backup
psql research_db < backup_previous.sql
```

---

## Troubleshooting

### Common Issues

**Issue: Backend won't start**
- Check logs: `docker-compose logs backend`
- Verify environment variables
- Check port availability

**Issue: Frontend can't reach backend**
- Verify CORS configuration
- Check proxy settings
- Confirm backend is running

**Issue: Database connection fails**
- Verify DATABASE_URL
- Check PostgreSQL is running
- Verify credentials

---

## Support

For deployment issues:
- Review logs carefully
- Check environment configuration
- Verify network connectivity
- Test individual components

## Next Steps After Deployment

1. Set up monitoring alerts
2. Configure automated backups
3. Implement logging aggregation
4. Set up CI/CD pipeline
5. Document custom configurations
