# Quick Start Guide - Production Deployment

This guide provides the fastest path to production deployment.

---

## ⚡ 5-Minute Local Test

```bash
# 1. Clone and setup
git clone https://github.com/liljoker919/car_maintenance.git
cd car_maintenance
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup
mkdir -p static logs
python manage.py migrate
python manage.py createsuperuser

# 4. Run
python manage.py runserver

# Visit: http://localhost:8000
# Admin: http://localhost:8000/admin
```

---

## 🐳 5-Minute Docker Test

```bash
# 1. Clone repository
git clone https://github.com/liljoker919/car_maintenance.git
cd car_maintenance

# 2. Create .env file
cp .env.example .env

# 3. Start with Docker Compose
docker-compose up -d --build

# 4. Run migrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

# Visit: http://localhost:8000
```

---

## 🚀 Production Deployment (AWS Lightsail)

### Prerequisites
- AWS account
- Domain name (optional but recommended)
- 30-60 minutes

### Step 1: Create Lightsail Instance (5 min)
1. Go to https://lightsail.aws.amazon.com/
2. Click "Create instance"
3. Select: Linux/Unix → Ubuntu 22.04 LTS
4. Choose: $5/month plan (1GB RAM minimum)
5. Name: `car-maintenance-tracker`
6. Create instance

### Step 2: Configure Environment (10 min)

```bash
# SSH into instance
ssh ubuntu@YOUR_INSTANCE_IP

# Install requirements
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y python3-pip python3-venv nginx postgresql postgresql-contrib git

# Setup PostgreSQL
sudo -u postgres psql -c "CREATE DATABASE car_maintenance_db;"
sudo -u postgres psql -c "CREATE USER caruser WITH PASSWORD 'YOUR_SECURE_PASSWORD';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE car_maintenance_db TO caruser;"
```

### Step 3: Deploy Application (15 min)

```bash
# Create app directory
sudo mkdir -p /var/www/car_maintenance
sudo chown ubuntu:ubuntu /var/www/car_maintenance
cd /var/www/car_maintenance

# Clone repository
git clone https://github.com/liljoker919/car_maintenance.git .

# Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Edit configuration (see below)

# Run migrations
mkdir -p logs static
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### Step 4: Environment Configuration

Edit `/var/www/car_maintenance/.env`:

```env
# Generate new secret key:
# python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

DJANGO_SECRET_KEY=your-generated-secret-key-here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-domain.com,www.your-domain.com,YOUR_IP

DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=car_maintenance_db
DATABASE_USER=caruser
DATABASE_PASSWORD=YOUR_SECURE_PASSWORD
DATABASE_HOST=localhost
DATABASE_PORT=5432

DJANGO_SECURE_SSL=True
DJANGO_SECURE_HSTS_SECONDS=31536000
DJANGO_SESSION_COOKIE_SECURE=True
DJANGO_CSRF_COOKIE_SECURE=True
```

### Step 5: Configure Gunicorn (10 min)

Create service: `sudo nano /etc/systemd/system/car_maintenance.service`

```ini
[Unit]
Description=Car Maintenance Tracker
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
    car_maintenance.wsgi:application

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable car_maintenance
sudo systemctl start car_maintenance
sudo systemctl status car_maintenance
```

### Step 6: Configure Nginx (5 min)

Create config: `sudo nano /etc/nginx/sites-available/car_maintenance`

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location /static/ {
        alias /var/www/car_maintenance/staticfiles/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/car_maintenance/gunicorn.sock;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/car_maintenance /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 7: SSL Certificate (5-10 min)

**Option A: Let's Encrypt (Free)**
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

**Option B: Lightsail Load Balancer**
1. Go to Lightsail Console → Networking → Load Balancers
2. Create load balancer
3. Attach SSL certificate
4. Add your instance as target

### Step 8: Firewall Configuration (3 min)

In Lightsail Console → Networking:
- ✅ HTTP (80) - from anywhere
- ✅ HTTPS (443) - from anywhere  
- ✅ SSH (22) - from your IP only
- ❌ Remove port 8000 if added

---

## ✅ Post-Deployment Checklist

### Security
- [ ] Changed SECRET_KEY from default
- [ ] Set DEBUG=False
- [ ] Configured ALLOWED_HOSTS
- [ ] SSL certificate installed
- [ ] Firewall configured (SSH restricted)
- [ ] Using PostgreSQL (not SQLite)

### Functionality
- [ ] Application loads at https://your-domain.com
- [ ] Admin interface accessible
- [ ] User registration works
- [ ] Vehicle CRUD operations work
- [ ] Static files loading correctly

### Monitoring (Optional)
- [ ] Set up uptime monitoring (UptimeRobot, Pingdom)
- [ ] Configure error tracking (Sentry)
- [ ] Set up database backups
- [ ] Enable AWS CloudWatch monitoring

---

## 🔧 Common Issues

### "502 Bad Gateway"
```bash
# Check Gunicorn status
sudo systemctl status car_maintenance

# Check logs
sudo journalctl -u car_maintenance -f

# Restart service
sudo systemctl restart car_maintenance
```

### "Static files not loading"
```bash
cd /var/www/car_maintenance
source venv/bin/activate
python manage.py collectstatic --noinput
sudo systemctl restart car_maintenance
sudo systemctl restart nginx
```

### "Database connection error"
```bash
# Verify PostgreSQL is running
sudo systemctl status postgresql

# Check database exists
sudo -u postgres psql -l

# Test connection
sudo -u postgres psql -d car_maintenance_db -c "\dt"
```

### "Permission denied"
```bash
sudo chown -R ubuntu:www-data /var/www/car_maintenance
sudo chmod -R 755 /var/www/car_maintenance
sudo chmod 775 /var/www/car_maintenance/logs
```

---

## 📚 Documentation

- **SECURITY_REVIEW.md** - Comprehensive security review and recommendations
- **DEPLOYMENT.md** - Detailed deployment guide with troubleshooting
- **IMPLEMENTATION_SUMMARY.md** - Summary of all changes made
- **README.md** - Project overview and features

---

## 🆘 Support

1. Check logs: `/var/www/car_maintenance/logs/django.log`
2. Review error in terminal: `sudo journalctl -u car_maintenance -f`
3. Check Nginx logs: `sudo tail -f /var/log/nginx/error.log`
4. Refer to DEPLOYMENT.md for detailed troubleshooting

---

## 🎯 Success Indicators

Your deployment is successful when:
- ✅ Application loads over HTTPS
- ✅ No security warnings in browser
- ✅ Admin interface accessible
- ✅ User registration works
- ✅ All tests pass: `python manage.py test`
- ✅ CodeQL scan clean: 0 vulnerabilities

---

**Estimated Total Time:** 45-90 minutes  
**Difficulty Level:** Intermediate  
**Cost:** $5-15/month (Lightsail + optional database)

**Ready to deploy?** Follow this guide step-by-step for a secure production deployment!
