# SmartHire Deployment Checklist

## ✅ Pre-Deployment Checklist

### 1. Code Changes ✅ (Already Done)
- [x] Updated `app.py` to use environment variables
- [x] Added `psycopg2-binary` to requirements.txt
- [x] Created `.env.example` file
- [x] Ensured `.env` is in `.gitignore`

### 2. Render Database Setup
- [ ] PostgreSQL database is running on Render
- [ ] Copy External Database URL from Render Dashboard
- [ ] Test database connection (optional)

### 3. Hostinger VPS Setup
- [ ] VPS/Cloud hosting plan active
- [ ] SSH access enabled
- [ ] Domain name configured (optional)

---

## 🚀 Deployment Steps

Follow the guide: **[HOSTINGER_RENDER_DB_DEPLOYMENT.md](HOSTINGER_RENDER_DB_DEPLOYMENT.md)**

### Quick Steps Summary:

1. **Upload Files to Hostinger**
   - [ ] Via Git clone OR File Manager/FTP

2. **Setup Python Environment**
   - [ ] Create virtual environment: `python3 -m venv venv`
   - [ ] Activate: `source venv/bin/activate`
   - [ ] Install dependencies: `pip install -r requirements.txt`
   - [ ] Download spaCy model: `python -m spacy download en_core_web_sm`

3. **Configure Environment Variables**
   - [ ] Create `.env` file on server
   - [ ] Add `SECRET_KEY` (generate random key)
   - [ ] Add `DATABASE_URL` (from Render)
   - [ ] Add `MAIL_USERNAME` and `MAIL_PASSWORD`

4. **Create Directories**
   - [ ] Run: `mkdir -p logs static/uploads static/screenings`
   - [ ] Set permissions: `chmod -R 777 uploads static/uploads`

5. **Test Application**
   - [ ] Test with: `gunicorn -c gunicorn_config.py wsgi:app`
   - [ ] Verify app starts without errors

6. **Setup PM2**
   - [ ] Install PM2: `npm install -g pm2`
   - [ ] Start app: `pm2 start gunicorn --name smarthire ...`
   - [ ] Save config: `pm2 save`
   - [ ] Setup startup: `pm2 startup`

7. **Configure Nginx**
   - [ ] Create Nginx config file
   - [ ] Enable site
   - [ ] Test: `sudo nginx -t`
   - [ ] Reload: `sudo systemctl reload nginx`

8. **Setup SSL (Optional)**
   - [ ] Install certbot
   - [ ] Run: `sudo certbot --nginx -d yourdomain.com`

9. **Verify Deployment**
   - [ ] Visit `http://yourdomain.com` or `http://server-ip`
   - [ ] Test login functionality
   - [ ] Test file uploads
   - [ ] Test resume screening

---

## 🔒 Security Checklist

- [ ] Changed `SECRET_KEY` from default value
- [ ] `.env` file is NOT committed to Git
- [ ] Database password is strong
- [ ] Email uses App Password (not regular password)
- [ ] SSL certificate installed (HTTPS)
- [ ] Debug mode is OFF (`debug=False` in app.py line 1566)
- [ ] Firewall configured (only ports 22, 80, 443 open)

---

## 📋 Environment Variables Required

Your `.env` file should contain:

```env
SECRET_KEY=<generate-random-key>
DATABASE_URL=postgresql://user:pass@host:5432/db
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
```

**Generate SECRET_KEY:**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

---

## 🐛 Post-Deployment Testing

### Test User Authentication
- [ ] Signup with email verification works
- [ ] Login works for all user types (admin, applicant, employer)
- [ ] Logout works

### Test Applicant Features
- [ ] Upload resume (PDF)
- [ ] Update profile
- [ ] Apply for jobs
- [ ] View application history

### Test Employer Features
- [ ] Create job postings
- [ ] Upload resume for screening
- [ ] Screen existing resumes
- [ ] View screening results

### Test Admin Features
- [ ] Approve job postings
- [ ] Manage users
- [ ] View all resumes

---

## 🔍 Common Issues & Solutions

### Database Connection Error
**Solution**: Check `DATABASE_URL` in `.env` file

### Module Not Found Error
**Solution**:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Permission Denied on Uploads
**Solution**:
```bash
chmod -R 777 ~/smarthire/uploads
chmod -R 777 ~/smarthire/static/uploads
```

### 502 Bad Gateway
**Solution**:
```bash
pm2 restart smarthire
sudo systemctl reload nginx
```

---

## 📞 Support Resources

1. **Deployment Guide**: [HOSTINGER_RENDER_DB_DEPLOYMENT.md](HOSTINGER_RENDER_DB_DEPLOYMENT.md)
2. **Check Logs**: `pm2 logs smarthire`
3. **Nginx Logs**: `sudo tail -f /var/log/nginx/error.log`
4. **Hostinger Support**: Live chat in hPanel (24/7)
5. **Render Support**: [Render Documentation](https://render.com/docs)

---

## ✅ Deployment Complete!

Once all items are checked, your SmartHire application is live! 🎉

**App URL**: `https://yourdomain.com` or `http://your-server-ip`
