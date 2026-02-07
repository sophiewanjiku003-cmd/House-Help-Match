# House-Help Deployment Guide - Railway (Alternative)

## Why Railway?
✅ **Free Trial** - $5/month free credits (more than enough for testing)  
✅ **Git Integration** - Auto-deploys on every push to main  
✅ **Easy Updates** - Just push to GitHub, Railway deploys automatically  
✅ **Databases Included** - PostgreSQL, MySQL included  
✅ **Modern Interface** - Better than many paid platforms  

---

## Step-by-Step Deployment

### 1. Create GitHub Repository

```bash
cd c:\Users\SLIZLER\Desktop\HOUSE-HELP
git init
git add .
git commit -m "Initial commit"
```

Push to GitHub:
```bash
git remote add origin https://github.com/YOUR_USERNAME/house-help.git
git branch -M main
git push -u origin main
```

### 2. Create Railway Account

1. Go to https://railway.app
2. Click "Start Free" 
3. Sign up with GitHub
4. Authorize Railway to access your repositories

### 3. Create New Project

1. Click **+ New Project**
2. Select **Deploy from GitHub repo**
3. Select your `house-help` repository
4. **Important**: Don't connect yet, let's prepare the setup

### 4. Create `railway.json`

Create this file in project root:

```json
{
  "buildCommand": "pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate",
  "startCommand": "gunicorn config.wsgi"
}
```

### 5. Create `Procfile`

```
web: gunicorn config.wsgi --log-file -
```

### 6. Update Requirements.txt

Already done - includes `gunicorn` and `whitenoise`

### 7. Commit These Files

```bash
git add railway.json Procfile
git commit -m "Add Railway deployment configuration"
git push origin main
```

### 8. Connect Railway Project

Back in Railway:
1. Click **+ New Service**
2. **GitHub Repo**
3. Select your `house-help` repository
4. Click **Deploy**

### 9. Set Environment Variables in Railway

1. In your deployment, click **Variables**
2. Add these:

```
DEBUG=False
SECRET_KEY=django-insecure-your-new-random-secret-key-here
ALLOWED_HOSTS=your-app.railway.app
DATABASE_URL=postgresql://... (Railway will generate this)
```

### 10. Add PostgreSQL Database

1. Click **+ Add Service**
2. Search for **PostgreSQL**
3. Click **Add**
4. Railway automatically sets `DATABASE_URL`

### 11. Deploy

Railway automatically deploys when you push!

```bash
git push origin main  # Railway will auto-deploy
```

---

## Making Updates (Super Easy!)

Just push your changes:

```bash
git add .
git commit -m "Your feature"
git push origin main
```

**That's it!** Railway automatically:
- Pulls your code
- Runs migrations
- Collects static files
- Deploys your app

---

## Custom Domain (Free!)

1. In Railway dashboard, go to **Settings**
2. Scroll to **Domains**
3. Add your custom domain
4. Update DNS records with Railway's instructions

---

## Monitoring & Logs

- Click **Logs** tab to see real-time output
- Automatic error notifications
- Performance metrics included

---

## Cost Comparison

| Feature | Railway | PythonAnywhere |
|---------|---------|---|
| **Free Tier** | $5/month credits | 3 free apps |
| **Auto-Deploy** | Yes (on push) | Manual pull |
| **Database** | Included | Included |
| **Updates** | One commit = live | 5-10 min process |
| **Domains** | Free custom domain | Free subdomain |

---

## Security Before Launch

- [ ] Change `SECRET_KEY` to a new random string
- [ ] Set `DEBUG=False`  
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Create strong superuser password
- [ ] Enable Railway's built-in security

**Your app is live and auto-updating! 🚀**
