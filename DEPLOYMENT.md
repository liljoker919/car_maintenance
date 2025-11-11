# Deployment Guide - Car Maintenance Tracker

This guide covers deployment options for the Car Maintenance Tracker Django application.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Deployment](#docker-deployment)
4. [AWS Lightsail Deployment](#aws-lightsail-deployment)
5. [Database Migration](#database-migration)
6. [SSL/HTTPS Setup](#sslhttps-setup)
7. [Post-Deployment Checklist](#post-deployment-checklist)

---

## Prerequisites

- Python 3.12+
- PostgreSQL 12+ (for production)
- Git
- Domain name (for production HTTPS)
- AWS account (for Lightsail deployment)

---

## Local Development Setup

### 1. Clone Repository
```bash
git clone https://github.com/liljoker919/car_maintenance.git
cd car_maintenance
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
# For development, you can use the defaults
```

### 5. Run Migrations
```bash
# Create static directory
mkdir -p static

# Apply database migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 6. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Visit http://localhost:8000 to view the application.

---

## Docker Deployment

### Using Docker Compose (Recommended for Development)

1. **Install Docker and Docker Compose**
   - [Docker Installation Guide](https://docs.docker.com/get-docker/)
   - [Docker Compose Installation](https://docs.docker.com/compose/install/)

2. **Create .env File**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Build and Start Services**
   ```bash
   docker-compose up -d --build
   ```

4. **Run Migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Create Superuser**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. **Access Application**
   - Application: http://localhost:8000
   - Admin: http://localhost:8000/admin

7. **View Logs**
   ```bash
   docker-compose logs -f web
   ```

8. **Stop Services**
   ```bash
   docker-compose down
   ```

---

## AWS Lightsail Deployment

### Option 1: Manual Deployment

#### Step 1: Create Lightsail Instance

1. Go to [AWS Lightsail Console](https://lightsail.aws.amazon.com/)
2. Click "Create instance"
3. Choose instance location (closest to users)
4. Select platform: Linux/Unix
5. Select blueprint: OS Only → Ubuntu 22.04 LTS
6. Choose instance plan: $5/month (1GB RAM) minimum
7. Name your instance: `car-maintenance-tracker`
8. Click "Create instance"

#### Step 2: Configure Firewall

1. Go to instance → Networking tab
2. Add firewall rules:
   - HTTP (port 80) - from anywhere
   - HTTPS (port 443) - from anywhere
   - SSH (port 22) - from your IP only
   - Custom (port 8000) - temporary for testing

#### Step 3: Connect and Set Up Server

```bash
# SSH into instance
ssh ubuntu@YOUR_INSTANCE_IP

# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Python and dependencies
sudo apt-get install -y python3-pip python3-venv nginx postgresql postgresql-contrib git

# Install and configure PostgreSQL
sudo -u postgres psql -c "CREATE DATABASE car_maintenance_db;"
sudo -u postgres psql -c "CREATE USER caruser WITH PASSWORD 'secure_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE car_maintenance_db TO caruser;"
```

#### Step 4: Deploy Application

```bash
# Create application directory
sudo mkdir -p /var/www/car_maintenance
sudo chown ubuntu:ubuntu /var/www/car_maintenance
cd /var/www/car_maintenance

# Clone repository
git clone https://github.com/liljoker919/car_maintenance.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
nano .env  # Edit with production settings
```

#### Step 5: Configure Environment Variables

Edit `/var/www/car_maintenance/.env`:
```env
DJANGO_SECRET_KEY=your-generated-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-domain.com,www.your-domain.com,YOUR_INSTANCE_IP

DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=car_maintenance_db
DATABASE_USER=caruser
DATABASE_PASSWORD=secure_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

DJANGO_SECURE_SSL=True
DJANGO_SECURE_HSTS_SECONDS=31536000
DJANGO_SESSION_COOKIE_SECURE=True
DJANGO_CSRF_COOKIE_SECURE=True
```

#### Step 6: Run Migrations and Collect Static Files

```bash
# Activate virtual environment
source /var/www/car_maintenance/venv/bin/activate

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser

# Create logs directory
mkdir -p logs
chmod 755 logs
```

#### Step 7: Configure Gunicorn

Create systemd service file:
```bash
sudo nano /etc/systemd/system/car_maintenance.service
```

```ini
[Unit]
Description=Car Maintenance Tracker Gunicorn Application
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/var/www/car_maintenance
Environment="PATH=/var/www/car_maintenance/venv/bin"
EnvironmentFile=/var/www/car_maintenance/.env
ExecStart=/var/www/car_maintenance/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/var/www/car_maintenance/gunicorn.sock \
    --timeout 60 \
    --access-logfile /var/www/car_maintenance/logs/gunicorn-access.log \
    --error-logfile /var/www/car_maintenance/logs/gunicorn-error.log \
    car_maintenance.wsgi:application

[Install]
WantedBy=multi-user.target
```

Enable and start service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable car_maintenance
sudo systemctl start car_maintenance
sudo systemctl status car_maintenance
```

#### Step 8: Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/car_maintenance
```

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /var/www/car_maintenance/staticfiles/;
    }

    location /media/ {
        alias /var/www/car_maintenance/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/car_maintenance/gunicorn.sock;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/car_maintenance /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Database Migration

### Migrating from SQLite to PostgreSQL

#### Step 1: Backup SQLite Data
```bash
# With SQLite configured
python manage.py dumpdata \
    --natural-foreign \
    --natural-primary \
    -e contenttypes \
    -e auth.Permission \
    --indent 4 > datadump.json
```

#### Step 2: Update Database Configuration
Update `.env` with PostgreSQL settings:
```env
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=car_maintenance_db
DATABASE_USER=caruser
DATABASE_PASSWORD=secure_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

#### Step 3: Migrate Schema
```bash
# Run migrations on PostgreSQL
python manage.py migrate
```

#### Step 4: Load Data
```bash
python manage.py loaddata datadump.json
```

#### Step 5: Verify Migration
```bash
# Create test superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Test functionality
```

---

## SSL/HTTPS Setup

### Option 1: Using Let's Encrypt (Free)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

Certbot automatically:
- Obtains SSL certificate
- Configures Nginx
- Sets up auto-renewal cron job

### Option 2: Using Lightsail Load Balancer

1. Go to Lightsail Console → Networking → Load Balancers
2. Create load balancer
3. Attach SSL certificate
4. Configure target instances
5. Update ALLOWED_HOSTS in .env

Load balancer benefits:
- AWS manages SSL certificates
- Automatic SSL renewal
- Health checks
- Better availability

---

## Post-Deployment Checklist

### Security Checklist

- [ ] Changed SECRET_KEY from default
- [ ] Set DEBUG=False
- [ ] Configured ALLOWED_HOSTS correctly
- [ ] Enabled HTTPS/SSL
- [ ] Set secure cookie flags (SECURE_SSL_REDIRECT, etc.)
- [ ] Restricted SSH access to specific IPs
- [ ] Using PostgreSQL (not SQLite)
- [ ] Configured firewall rules
- [ ] Set up database backups
- [ ] Reviewed logs directory permissions

### Functionality Checklist

- [ ] All migrations applied
- [ ] Static files collected
- [ ] Superuser account created
- [ ] Test user registration
- [ ] Test vehicle creation
- [ ] Test insurance policy creation
- [ ] Test service record creation
- [ ] Test admin interface
- [ ] Verify email configuration (if applicable)

### Monitoring Checklist

- [ ] Set up error tracking (Sentry)
- [ ] Configure log rotation
- [ ] Set up uptime monitoring
- [ ] Configure database backups
- [ ] Set up alerts for critical errors
- [ ] Monitor disk space usage
- [ ] Monitor database performance

### Performance Checklist

- [ ] Run database migrations for indexes
- [ ] Verify query optimization (prefetch_related)
- [ ] Test application under load
- [ ] Configure caching (if needed)
- [ ] Optimize Gunicorn worker count
- [ ] Review Nginx configuration

---

## Troubleshooting

### Common Issues

#### Issue: Static files not loading
**Solution:**
```bash
python manage.py collectstatic --noinput
sudo systemctl restart car_maintenance
```

#### Issue: Database connection error
**Solution:**
- Verify PostgreSQL is running: `sudo systemctl status postgresql`
- Check database credentials in .env
- Verify database exists: `sudo -u postgres psql -l`

#### Issue: 502 Bad Gateway
**Solution:**
- Check Gunicorn status: `sudo systemctl status car_maintenance`
- Check logs: `sudo journalctl -u car_maintenance -f`
- Verify socket file exists: `ls -l /var/www/car_maintenance/gunicorn.sock`

#### Issue: Permission denied errors
**Solution:**
```bash
sudo chown -R ubuntu:www-data /var/www/car_maintenance
sudo chmod -R 755 /var/www/car_maintenance
sudo chmod 775 /var/www/car_maintenance/logs
```

---

## Backup and Recovery

### Database Backup
```bash
# Create backup
sudo -u postgres pg_dump car_maintenance_db > backup_$(date +%Y%m%d).sql

# Restore from backup
sudo -u postgres psql car_maintenance_db < backup_20231115.sql
```

### Application Backup
```bash
# Backup entire application
tar -czf car_maintenance_backup_$(date +%Y%m%d).tar.gz /var/www/car_maintenance

# Exclude unnecessary files
tar -czf car_maintenance_backup.tar.gz \
    --exclude='venv' \
    --exclude='*.pyc' \
    --exclude='__pycache__' \
    --exclude='staticfiles' \
    /var/www/car_maintenance
```

---

## Maintenance

### Regular Tasks

**Daily:**
- Monitor error logs
- Check application availability

**Weekly:**
- Review database performance
- Check disk space usage
- Review security logs

**Monthly:**
- Update dependencies: `pip list --outdated`
- Run security audit: `safety check`
- Review and optimize slow queries
- Test backup restoration
- Review SSL certificate expiration

---

## Support

For issues or questions:
- Check logs: `/var/www/car_maintenance/logs/`
- Review Django documentation: https://docs.djangoproject.com/
- Review this guide's troubleshooting section
- Contact repository maintainer

---

## Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [AWS Lightsail Documentation](https://lightsail.aws.amazon.com/ls/docs/)
