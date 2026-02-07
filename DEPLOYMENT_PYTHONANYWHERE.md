# House-Help Deployment Guide - PythonAnywhere

## Why PythonAnywhere?
✅ **Free** - Supports up to 3 free web apps  
✅ **Easy Updates** - Push to GitHub, pull on PythonAnywhere  
✅ **Django-Optimized** - Built specifically for Python/Django apps  
✅ **No Server Management** - Everything handled for you  
✅ **PostgreSQL Support** - Free PostgreSQL database included  

---

## Step-by-Step Deployment

### 1. Create a Git Repository

```bash
cd c:\Users\SLIZLER\Desktop\HOUSE-HELP
git init
git add .
git commit -m "Initial commit"
```

Create a new repository on GitHub (https://github.com/new) and push:

```bash
git remote add origin https://github.com/YOUR_USERNAME/house-help.git
git branch -M main
git push -u origin main
```

### 2. Create PythonAnywhere Account

1. Go to https://www.pythonanywhere.com
2. Click "Sign Up" and choose **Free account**
3. Verify your email

### 3. Create a Web App on PythonAnywhere

1. In Dashboard, click "Web" → "Add a new web app"
2. Choose **Manual configuration** (not Framework)
3. Select **Python 3.10** (or latest)
4. Note your app URL (e.g., `yourusername.pythonanywhere.com`)

### 4. Clone Your Repository

In PythonAnywhere **Bash Console**:

```bash
git clone https://github.com/YOUR_USERNAME/house-help.git
cd house-help
```

### 5. Create Virtual Environment

```bash
mkvirtualenv --python=/usr/bin/python3.10 househelp
pip install -r requirements.txt
```

### 6. Set Environment Variables

Click **Web** → **Edit configuration** → Add these to your WSGI file (see step 7):

```python
import os
os.environ['DEBUG'] = 'False'
os.environ['SECRET_KEY'] = 'generate-a-new-secret-key-here'
os.environ['ALLOWED_HOSTS'] = 'yourusername.pythonanywhere.com'
os.environ['DATABASE_URL'] = 'sqlite:////home/yourusername/house-help/db.sqlite3'
```

### 7. Configure WSGI File

1. Click **Web** → Edit your app
2. Under **Code**, click the WSGI file (usually `/var/www/...`)
3. Replace the Django section with:

```python
import os
import sys

# Add your project directory to the sys.path
project_home = '/home/yourusername/house-help'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# Set environment variables
os.environ['DEBUG'] = 'False'
os.environ['SECRET_KEY'] = 'your-random-secret-key-here'
os.environ['ALLOWED_HOSTS'] = 'yourusername.pythonanywhere.com'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 8. Collect Static Files

In Bash Console:

```bash
workon househelp
cd ~/house-help
python manage.py collectstatic --noinput
```

### 9. Run Migrations

```bash
python manage.py migrate
```

### 10. Create Superuser

```bash
python manage.py createsuperuser
# Follow prompts to create admin user
```

### 11. Reload Web App

Click **Web** dashboard and click the green **Reload** button

### 12. Visit Your Site

Go to: `https://yourusername.pythonanywhere.com`

---

## Making Updates (Easy!)

When you make changes locally:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

Then in PythonAnywhere **Bash Console**:

```bash
cd ~/house-help
git pull origin main
workon househelp
python manage.py migrate  # if database changes
python manage.py collectstatic --noinput
```

Click **Reload** button on Web dashboard. Done! ✅

---

## Troubleshooting

**500 Error?**
- Check **Error log** in Web dashboard
- Ensure `config.settings` is correct in WSGI file
- Make sure virtual environment path is correct

**Static files not loading?**
- Run: `python manage.py collectstatic --noinput`
- Click Reload

**Database not working?**
- Check `ALLOWED_HOSTS` in WSGI file
- Verify migrations: `python manage.py migrate`

---

## Setup with PostgreSQL (Free on PythonAnywhere)

1. Click **Databases** in PythonAnywhere
2. Create new PostgreSQL database
3. Note the connection string
4. Set in environment:
```
DATABASE_URL=postgresql://user:password@host/dbname
```

---

## Security Checklist

Before going live:
- [ ] Generate new `SECRET_KEY`
- [ ] Set `DEBUG = False`
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Create `.env` file (never commit it)
- [ ] Review firewall settings in Web app
- [ ] Add HTTPS enforcement in Web settings

**Your app is now live! 🚀**
