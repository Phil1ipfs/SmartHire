# Deploy SmartHire to Hostinger VPS with Render Database

Your setup: **Flask app on Hostinger VPS** + **PostgreSQL database on Render**

---

## Prerequisites

✅ Hostinger VPS or Cloud Hosting (with SSH access)
✅ PostgreSQL database already deployed on Render
✅ Domain name (optional but recommended)

---

## Step 1: Get Render Database Connection String

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click on your PostgreSQL database
3. Copy the **External Database URL**
   - Format: `postgresql://user:password@host:5432/database`
   - Example: `postgresql://smarthire_user:abc123@dpg-xyz.oregon-postgres.render.com/smarthire_db`

**IMPORTANT**: Save this URL - you'll need it in Step 5!

---

## Step 2: Login to Hostinger

1. Go to [hPanel](https://hpanel.hostinger.com)
2. Login with your credentials
3. Select your VPS/Cloud hosting plan
4. Open **SSH Access** → **Open Terminal**

---

## Step 3: Upload Project Files

### Option A: Using Git (Recommended)

```bash
cd ~
git clone <your-github-repo-url> smarthire
cd smarthire
```

### Option B: Using File Manager/FTP

1. In hPanel → **File Manager**
2. Navigate to home directory (`/home/username/`)
3. Create folder: `smarthire`
4. Upload all files:
   - `app.py`
   - `wsgi.py`
   - `gunicorn_config.py`
   - `requirements.txt`
   - `templates/` folder
   - `static/` folder
   - All other Python files

---

## Step 4: Setup Python Environment

SSH into your server and run:

```bash
cd ~/smarthire

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

---

## Step 5: Set Environment Variables

Create a `.env` file with your credentials:

```bash
nano .env
```

Add these lines (replace with your actual values):

```env
# Secret Key (generate a random string)
SECRET_KEY=your-super-secret-random-key-here-change-this

# Render PostgreSQL Database URL (from Step 1)
DATABASE_URL=postgresql://user:password@host:5432/database

# Email Configuration (Gmail)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
```

**To generate a secure SECRET_KEY:**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Save the file: `Ctrl+X` → `Y` → `Enter`

---

## Step 6: Load Environment Variables

Install python-dotenv:

```bash
pip install python-dotenv
```

Update your `app.py` to load the `.env` file (already done in your updated code).

---

## Step 7: Create Required Directories

```bash
mkdir -p logs static/uploads static/screenings uploads resumes
chmod -R 755 static templates
chmod -R 777 uploads resumes static/uploads static/screenings logs
```

---

## Step 8: Test the Application

```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Test with Gunicorn
gunicorn -c gunicorn_config.py wsgi:app
```

If you see output like:
```
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://127.0.0.1:8000
```

✅ **Success!** Press `Ctrl+C` to stop.

---

## Step 9: Setup PM2 (Process Manager)

PM2 keeps your app running 24/7:

```bash
# Install Node.js and PM2 (if not already installed)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
sudo npm install -g pm2

# Start your app with PM2
cd ~/smarthire
source venv/bin/activate
pm2 start gunicorn --name smarthire --interpreter venv/bin/python -- -c gunicorn_config.py wsgi:app

# Save PM2 configuration
pm2 save

# Setup PM2 to start on server reboot
pm2 startup
# Copy and run the command it outputs
```

---

## Step 10: Configure Nginx (Reverse Proxy)

Create Nginx configuration:

```bash
sudo nano /etc/nginx/sites-available/smarthire
```

Add this configuration (replace `yourdomain.com` with your actual domain):

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Increase timeout for long-running requests
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
    }

    # Serve static files directly
    location /static {
        alias /home/username/smarthire/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    client_max_body_size 50M;  # Allow larger file uploads
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/smarthire /etc/nginx/sites-enabled/
sudo nginx -t  # Test configuration
sudo systemctl reload nginx
```

---

## Step 11: Setup SSL (HTTPS) - Optional but Recommended

```bash
sudo apt-get install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Follow the prompts to get a free SSL certificate from Let's Encrypt.

---

## Step 12: Verify Deployment

Visit your domain: `http://yourdomain.com` or `http://your-server-ip`

You should see the SmartHire login page!

---

## Managing Your Application

### Check App Status
```bash
pm2 list
pm2 logs smarthire
```

### Restart App
```bash
pm2 restart smarthire
```

### Stop App
```bash
pm2 stop smarthire
```

### Update Code (after pushing changes)
```bash
cd ~/smarthire
git pull origin main
source venv/bin/activate
pip install -r requirements.txt  # If requirements changed
pm2 restart smarthire
```

### Check Logs
```bash
pm2 logs smarthire --lines 100
# Or check gunicorn logs
tail -f logs/error.log
tail -f logs/access.log
```

---

## Troubleshooting

### Issue: "Connection refused" or database errors
**Solution**: Check your `DATABASE_URL` in `.env` file
```bash
cat .env  # Verify DATABASE_URL is correct
```

### Issue: "Module not found"
**Solution**: Reinstall dependencies
```bash
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Issue: "Permission denied" on uploads
**Solution**: Fix permissions
```bash
chmod -R 777 ~/smarthire/uploads
chmod -R 777 ~/smarthire/static/uploads
```

### Issue: App not accessible from browser
**Solution**: Check firewall and Nginx
```bash
sudo ufw status  # Check firewall
sudo systemctl status nginx  # Check Nginx
pm2 list  # Check if app is running
```

### Issue: 502 Bad Gateway
**Solution**: Check if Gunicorn is running
```bash
pm2 list
pm2 restart smarthire
```

---

## Environment Variables Reference

Your `.env` file should contain:

```env
SECRET_KEY=<random-secret-key>
DATABASE_URL=postgresql://user:pass@host:5432/db
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

---

## Security Checklist

- [ ] Changed `SECRET_KEY` from default
- [ ] `.env` file is NOT committed to Git
- [ ] Database URL uses strong password
- [ ] Email uses App Password (not regular password)
- [ ] SSL certificate installed
- [ ] Firewall configured (only ports 22, 80, 443 open)
- [ ] Debug mode is OFF in production

---

## Need Help?

1. **Check logs**: `pm2 logs smarthire`
2. **Check Nginx logs**: `sudo tail -f /var/log/nginx/error.log`
3. **Hostinger Support**: Live chat in hPanel (24/7)

---

**You're all set!** 🚀

Your SmartHire app is now running on Hostinger VPS with Render PostgreSQL database.
