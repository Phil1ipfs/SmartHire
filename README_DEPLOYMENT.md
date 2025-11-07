# SmartHire - Deployment Guide

## 🎯 Your Deployment Setup

**Application**: SmartHire (Flask AI-powered recruitment platform)
**App Server**: Hostinger VPS
**Database**: Render PostgreSQL (already deployed ✅)

---

## 📚 Documentation Files

You have three comprehensive guides to help with deployment:

### 1. **[HOSTINGER_RENDER_DB_DEPLOYMENT.md](HOSTINGER_RENDER_DB_DEPLOYMENT.md)** ⭐ START HERE
   - Complete step-by-step deployment guide
   - Specific to Hostinger VPS + Render Database setup
   - Includes Nginx configuration
   - SSL setup instructions

### 2. **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)**
   - Interactive checklist format
   - Track your deployment progress
   - Security checklist included
   - Post-deployment testing steps

### 3. **Legacy Guides** (for reference)
   - [HOSTINGER_QUICK_REFERENCE.md](HOSTINGER_QUICK_REFERENCE.md)
   - [HOSTINGER_DEPLOYMENT.md](HOSTINGER_DEPLOYMENT.md)
   - [DEPLOY_NOW.md](DEPLOY_NOW.md)

---

## 🚀 Quick Start (5 Minutes)

### What Changed?

✅ **Code Updates** (Already Done):
- `app.py` now uses environment variables for database and email
- Added PostgreSQL support (`psycopg2-binary`)
- Created `.env.example` for easy configuration

### What You Need:

1. **Render Database URL**
   - Login to Render Dashboard
   - Copy your PostgreSQL "External Database URL"
   - Example: `postgresql://user:pass@host:5432/database`

2. **Hostinger VPS Access**
   - SSH credentials
   - Server IP or domain name

3. **Gmail App Password**
   - For sending verification emails
   - Generate at: https://myaccount.google.com/apppasswords

---

## 📋 Deployment in 3 Steps

### Step 1: Upload Files to Hostinger

**Option A - Git (Recommended):**
```bash
ssh username@your-server-ip
cd ~
git clone <your-repo-url> smarthire
cd smarthire
```

**Option B - File Manager:**
- Login to hPanel
- Upload all files to `~/smarthire/`

### Step 2: Run Setup Script

```bash
cd ~/smarthire
bash setup_env.sh
```

This will:
- Generate secure `SECRET_KEY`
- Create `.env` file with your credentials
- Configure database connection

**OR** manually create `.env`:
```bash
nano .env
```

Paste this (replace with your values):
```env
SECRET_KEY=<generate-with-python>
DATABASE_URL=postgresql://user:pass@host:5432/db
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Step 3: Deploy Application

```bash
# Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Create directories
mkdir -p logs static/uploads static/screenings
chmod -R 777 uploads static/uploads static/screenings logs

# Start with PM2
npm install -g pm2
pm2 start gunicorn --name smarthire --interpreter venv/bin/python -- -c gunicorn_config.py wsgi:app
pm2 save
pm2 startup
```

**That's it!** 🎉

Full instructions: [HOSTINGER_RENDER_DB_DEPLOYMENT.md](HOSTINGER_RENDER_DB_DEPLOYMENT.md)

---

## 🔑 Key Configuration

### Database Connection
- **Development**: `mysql+pymysql://root:@localhost/smarthire`
- **Production**: `postgresql://user:pass@host:5432/db` (from Render)

### Environment Variables (`.env`)
```env
SECRET_KEY=<random-key>
DATABASE_URL=postgresql://...
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Important Files
- `app.py` - Main application (updated for production)
- `wsgi.py` - WSGI entry point for Gunicorn
- `gunicorn_config.py` - Gunicorn server configuration
- `requirements.txt` - Python dependencies (includes PostgreSQL)
- `.env` - Environment variables (create on server)

---

## 🛠️ Management Commands

### Check App Status
```bash
pm2 list
pm2 logs smarthire
```

### Restart App
```bash
pm2 restart smarthire
```

### Update Code
```bash
cd ~/smarthire
git pull
source venv/bin/activate
pip install -r requirements.txt
pm2 restart smarthire
```

### View Logs
```bash
pm2 logs smarthire --lines 100
tail -f logs/error.log
```

---

## 🐛 Troubleshooting

### Database Connection Error
```bash
# Check .env file
cat .env

# Verify DATABASE_URL format
# Should be: postgresql://user:pass@host:5432/database
```

### Module Not Found
```bash
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Permission Denied
```bash
chmod -R 777 ~/smarthire/uploads
chmod -R 777 ~/smarthire/static/uploads
```

### App Not Loading
```bash
pm2 restart smarthire
sudo systemctl reload nginx
pm2 logs smarthire
```

---

## 📊 Application Architecture

```
┌─────────────────────────────────────────┐
│          User Browser                   │
│  (http://yourdomain.com)               │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│      Nginx (Reverse Proxy)             │
│      Port 80/443                        │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│      Gunicorn + Flask App              │
│      (Hostinger VPS)                    │
│      Port 8000                          │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│   PostgreSQL Database                   │
│   (Render Cloud)                        │
│   Port 5432                             │
└─────────────────────────────────────────┘
```

---

## 📞 Getting Help

1. **Full Deployment Guide**: [HOSTINGER_RENDER_DB_DEPLOYMENT.md](HOSTINGER_RENDER_DB_DEPLOYMENT.md)
2. **Checklist**: [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
3. **Check Logs**: `pm2 logs smarthire`
4. **Hostinger Support**: Live chat in hPanel (24/7)
5. **Render Support**: [render.com/docs](https://render.com/docs)

---

## 🎉 Ready to Deploy?

1. Read **[HOSTINGER_RENDER_DB_DEPLOYMENT.md](HOSTINGER_RENDER_DB_DEPLOYMENT.md)**
2. Follow **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)**
3. Deploy and enjoy!

**Good luck!** 🚀