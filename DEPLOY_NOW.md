# 🚀 Deploy House-Help to Railway - LIVE GUIDE

## Step-by-Step Deployment (15 minutes)

Follow these steps exactly to deploy your app LIVE!

---

## 📝 STEP 1: Create GitHub Repository (2 minutes)

### On Your Computer (GitHub Web)

1. **Go to:** https://github.com/new
2. **Fill in the form:**
   - Repository name: `house-help`
   - Description: "House matching platform for employers and workers"
   - Public or Private: (your choice)
3. **Click:** "Create repository"
4. **Copy the HTTPS URL** (you'll need it in step 2)
   - It looks like: `https://github.com/YOUR_USERNAME/house-help.git`

---

## 💾 STEP 2: Push Code to GitHub (3 minutes)

### In Your Terminal (PowerShell)

Replace `YOUR_USERNAME` with your GitHub username:

```powershell
cd c:\Users\SLIZLER\Desktop\HOUSE-HELP
git remote add origin https://github.com/YOUR_USERNAME/house-help.git
git branch -M main
git push -u origin main
```

**Expected output:**
```
Enumerating objects: 86, done.
Counting objects: 100% (86/86), done.
...
To https://github.com/YOUR_USERNAME/house-help.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

✅ **Your code is now on GitHub!**

---

## 🚀 STEP 3: Create Railway Account (2 minutes)

1. **Go to:** https://railway.app
2. **Click:** "Start Free"
3. **Sign in with GitHub**
   - Click "Sign in with GitHub"
   - Authorize Railway
4. **Agree to terms**
5. **Done!** You're logged into Railway

---

## 📦 STEP 4: Create Railway Project (5 minutes)

### On Railway Dashboard:

1. **Click:** "+ New Project"
2. **Select:** "Deploy from GitHub repo"
3. **Choose the repository:** 
   - Search for "house-help"
   - Click it
4. **Railway auto-detects Django** ✅
5. **Wait for deployment** (it may fail - that's normal, see below)

### After First Deploy Attempt:

Railway will try to auto-deploy. It might show errors about environment variables. This is expected! We'll fix it in Step 5.

---

## 🔧 STEP 5: Set Environment Variables (3 minutes)

### In Railway Dashboard:

1. **Click your project** (house-help)
2. **Click "Variables" tab**
3. **Add these variables:**

| Variable | Value |
|----------|-------|
| `DEBUG` | `False` |
| `SECRET_KEY` | Generate new: run `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` and paste the output |
| `ALLOWED_HOSTS` | `yourapp.railway.app` (Railway will show your exact URL) |
| `EMAIL_HOST_USER` | `blaisengugi3@gmail.com` |
| `EMAIL_HOST_PASSWORD` | Your 16-char Gmail App Password (from GMAIL_SETUP_GUIDE.md) |

### How to Add Variables:

1. Click "New Variable"
2. Enter key name (e.g., `DEBUG`)
3. Enter value (e.g., `False`)
4. Click "Add"
5. Repeat for all variables

---

## ✅ STEP 6: Deploy! (1 minute)

### In Railway Dashboard:

1. **Click the "Deployments" tab**
2. **Click "Redeploy"** (or wait ~10 seconds for auto-redeploy after variable changes)
3. **Wait for deployment to complete**
   - Status changes from "Building" → "Deploying" → "Success"
   - This takes ~2-3 minutes

### How to Know It's Working:

- ✅ Deployment status shows "Success"
- ✅ Build log shows no major errors
- ✅ Your app URL appears at top (copy it!)

---

## 🌐 STEP 7: Visit Your Live App! (1 minute)

### Get Your App URL:

1. **In Railway Dashboard, top right:**
   - Click the URL (looks like: `house-help-production.up.railway.app`)
2. **Visit it in browser:** `https://yourapp.railway.app`

### Test Your App:

- ✅ Homepage loads
- ✅ Click **Admin** at bottom or `/admin/`
- ✅ Create a new superuser for production (important!)
- ✅ Login works
- ✅ Navigation works

---

## 🛑 TROUBLESHOOTING COMMON ERRORS

### Error: "500 Internal Server Error"

**Solution:**
1. Check Railway logs (Deployments tab → View logs)
2. Look for "No such table" errors
3. Run migrations from Railway CLI:
   ```bash
   railway run python manage.py migrate
   ```

### Error: "ModuleNotFoundError"

**Solution:**
1. Check `requirements.txt` is in root folder
2. Verify all dependencies listed
3. Redeploy from Railway dashboard

### Error: "Static files not found"

**Solution:**
1. Run in Railway CLI:
   ```bash
   railway run python manage.py collectstatic --noinput
   ```
2. Redeploy

### Error: "Email not sending"

**Solution:**
1. Check EMAIL_HOST_PASSWORD is correct (16 chars)
2. Make sure it's a Gmail App Password (not regular password)
3. See GMAIL_SETUP_GUIDE.md for help

### Email Password Issues?

⚠️ If you don't have the Gmail App Password yet:

1. Read: `GMAIL_SETUP_GUIDE.md`
2. Follow steps to enable 2FA and get app password
3. Update Railway variables
4. Redeploy

---

## 🎯 What Happens After Deploy

### Your App is Now:
- ✅ **Live and public** at `yourapp.railway.app`
- ✅ **Auto-updates** on every git push to main
- ✅ **Self-healing** - Railway monitors and restarts if needed
- ✅ **Secure** - HTTPS automatic
- ✅ **Scalable** - Can handle growing traffic

### Every Time You Update Code:

```bash
# Local machine
git add .
git commit -m "Your feature"
git push origin main

# ✅ Automatic! Railway auto-deploys in 30 seconds!
```

---

## 📊 Your Deployment Overview

```
GIT REPOSITORY:
  https://github.com/YOUR_USERNAME/house-help
  
LIVE APP:
  https://yourapp.railway.app
  
ADMIN PANEL:
  https://yourapp.railway.app/admin/
  
DEPLOYMENT PLATFORM:
  Railway.app
  
AUTO-DEPLOY:
  ✅ Active (on push to main branch)
```

---

## 🔐 Create Production Admin Account

### Important: Create New Admin on Production!

```bash
# In Railway CLI or visit /admin/ and create user
railway run python manage.py createsuperuser
# Follow prompts to create username/password
```

Or through Django admin web interface:
1. Visit `yourapp.railway.app/admin/`
2. Click admin username dropdown
3. Create new superuser

---

## ✨ Next: Optional Improvements

### Add Custom Domain (Free!)
1. In Railway: Settings → Domains
2. Add your domain
3. Follow DNS instructions

### Enable PostgreSQL (Optional)
1. In Railway: + Add Service
2. Select PostgreSQL
3. Railway auto-configures DATABASE_URL

### Monitor Performance
1. Watch build logs
2. Check resource usage
3. Monitor error rates

---

## 📱 Test Your Deployed App

After deployment, test these features:

- [ ] Homepage loads
- [ ] Admin login works
- [ ] Create test job posting
- [ ] Browse jobs
- [ ] Send message
- [ ] Password reset (sends email)
- [ ] Mobile responsive

---

## 🎓 Key Railway Features

### Auto-Deploy
- Push to GitHub → Auto-deploys in 30 seconds

### Environment Variables
- Secrets never in code
- Update anytime, redeploy on save

### Monitoring
- Real-time logs
- Error tracking
- Performance metrics

### Database
- Add PostgreSQL with one click
- Automatic backups
- Connection pooling

### Domains
- Free subdomains
- Custom domains supported
- HTTPS automatic

---

## 📞 While Deploying

### If things go wrong:
1. **Check logs** - Deployments tab → View logs
2. **Restart** - Click Redeploy button
3. **Update variables** - Add missing env vars
4. **Check code** - Ensure no Python errors locally first

### Common Questions:
- **"Where's my URL?"** - Top right of project, blue text
- **"How long to deploy?"** - 2-3 minutes typically
- **"Can I delete a deployment?"** - Yes, but app goes down
- **"Is my .env protected?"** - Yes, stored securely in Railway

---

## 🚀 You're Live!

Your **House-Help** app is now deployed and accessible to the world!

### Share Your App:
```
https://yourapp.railway.app
```

### Make Updates:
```bash
git push origin main
# ✅ Auto-deployed in 30 seconds!
```

### Monitor Performance:
- Check Railway dashboard regularly
- Watch for error spikes
- Monitor database usage

---

## 📖 Next Steps

1. ✅ **Get your app working live** (this guide)
2. ⏳ Add custom domain (optional)
3. ⏳ Set up PostgreSQL database (optional)
4. ⏳ Enable monitoring and alerts (optional)
5. ⏳ Set up CI/CD pipeline (optional)

---

## 🎉 Success Checklist

- [ ] GitHub repo created
- [ ] Code pushed to main branch
- [ ] Railway project created
- [ ] Environment variables set
- [ ] Deployment successful (green status)
- [ ] App accessible at yourapp.railway.app
- [ ] Admin login works
- [ ] Password reset email configured
- [ ] All features tested

---

**Deployment Time: ~15 minutes**  
**Your App Status: LIVE! 🚀**  
**Auto-Updates: ENABLED ✅**

---

**Questions? Check:**
- Railway Docs: https://docs.railway.app/
- Django Docs: https://docs.djangoproject.com/
- This directory: See other .md files

Good luck! Your House-Help app is going live! 🎊
