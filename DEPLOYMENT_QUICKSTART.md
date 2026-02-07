# 🚀 House-Help Deployment Checklist

## Pre-Deployment Setup (Do This First)

### 1. Generate a New Secret Key
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Copy this key - you'll need it for deployment.

### 2. Create `.env` File (NEVER commit this)
```
DEBUG=False
SECRET_KEY=<paste-your-new-secret-key-here>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@host/dbname  # Only if using PostgreSQL
```

### 3. Test Locally
```bash
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py runserver
```

### 4. Verify All Files Created
- ✅ `requirements.txt` - Python dependencies
- ✅ `Procfile` - App startup command  
- ✅ `railway.json` - Railway configuration
- ✅ `.env.example` - Template for environment variables
- ✅ `.gitignore` - Files to exclude from Git
- ✅ `DEPLOYMENT_RAILWAY.md` - Railway guide
- ✅ `DEPLOYMENT_PYTHONANYWHERE.md` - PythonAnywhere guide

---

## Choose Your Platform

### **RECOMMENDED: Railway** ⭐
**Best for:** Easy auto-deployment on every git push

**What you get:**
- $5/month free credits (more than enough)
- Automatic deployment on push to main
- Free PostgreSQL database
- Free custom domain
- Modern interface

**Time to deploy:** ~10 minutes

👉 [Follow Railway Guide](DEPLOYMENT_RAILWAY.md)

---

### **ALTERNATIVE: PythonAnywhere**
**Best for:** Maximum free tier without credits

**What you get:**
- Completely free (up to 3 apps)
- Free PostgreSQL database
- Django-optimized platform
- Manual pulling of updates (5-10 min per update)

**Time to deploy:** ~15 minutes

👉 [Follow PythonAnywhere Guide](DEPLOYMENT_PYTHONANYWHERE.md)

---

## Quick Summary

| Step | Railway | PythonAnywhere |
|------|---------|---|
| 1. Create Git repo | `git init` + push to GitHub | Same |
| 2. Create account | Sign up with GitHub | Sign up free |
| 3. Connect app | Connect GitHub repo | Clone from GitHub |
| 4. Set variables | In Railway dashboard | In WSGI file |
| 5. Add database | Click "Add PostgreSQL" | Built-in |
| 6. Deploy | Auto on push | Manual `git pull` |
| 7. Time per update | Seconds | 5-10 minutes |

---

## After Deployment

### Test Your Site
1. Visit your app URL
2. Create admin account: `/admin/`
3. Test login/logout
4. Verify static files load

### Set Up HTTPS
- **Railway:** Automatic
- **PythonAnywhere:** Enable in Web tab

### Monitor Performance
- Check logs regularly
- Monitor database size
- Clean old image files in `/media/`

---

## Making Updates (Easy!)

### Local Development
```bash
git add .
git commit -m "Feature description"
git push origin main
```

### With Railway 
✅ **Automatic!** Your site updates in ~30 seconds

### With PythonAnywhere
```bash
# In PythonAnywhere Bash Console
cd ~/house-help
git pull origin main
workon househelp
python manage.py migrate
python manage.py collectstatic --noinput
# Then click Reload in Web dashboard
```

---

## Troubleshooting

**"ImportError" or "ModuleNotFoundError"**
→ Check if all packages in requirements.txt are correct

**"Database does not exist"**
→ Run migrations: `python manage.py migrate`

**Static files not loading**
→ Run: `python manage.py collectstatic --noinput`

**Site shows "500 Error"**
→ Check deployment logs in Railway/PythonAnywhere dashboard

---

## Security Checklist Before Going Live

- [ ] `DEBUG = False` in settings
- [ ] Generated new `SECRET_KEY`
- [ ] Updated `ALLOWED_HOSTS` with your domain
- [ ] `.env` file is in `.gitignore` (never commit secrets!)
- [ ] Database password is strong
- [ ] HTTPS is enabled
- [ ] Superuser password is secure

---

## Need Help?

- **Railway Docs:** https://docs.railway.app/
- **PythonAnywhere Docs:** https://help.pythonanywhere.com/
- **Django Deployment:** https://docs.djangoproject.com/en/4.2/howto/deployment/

---

## Summary

Your House-Help app is **ready to deploy**! 

**Quick start:**
1. Read the guide for your chosen platform above
2. Follow the steps
3. Push to GitHub
4. Visit your live site! 🎉

Good luck! 🚀
