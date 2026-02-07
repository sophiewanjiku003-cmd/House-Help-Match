# House-Help 🏠

A Django web application connecting employers with domestic workers.

## Features

- 💼 Job posting and management
- 👤 User profiles (employers, house help workers)
- 💬 Messaging system
- ⭐ Review and rating system
- 📍 Location-based job search
- 🔐 User authentication with password reset
- 📊 Admin dashboard

## Quick Start (Local Development)

### Prerequisites
- Python 3.10+
- pip
- Virtual environment

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/house-help.git
cd house-help

# Create virtual environment
python -m venv .venv

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Activate virtual environment (Mac/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Run development server
python manage.py runserver
```

Visit: `http://localhost:8000/`  
Admin: `http://localhost:8000/admin/`

---

## 🚀 Deployment

The application is ready for production deployment on:

### Railway (Recommended)
- ⭐ Auto-deploys on git push
- Free $5/month credits
- Built-in PostgreSQL
- Takes ~10 minutes

[Read: DEPLOYMENT_RAILWAY.md](DEPLOYMENT_QUICKSTART.md#recommended-railway)

### PythonAnywhere
- Completely free
- No credits needed
- Django optimized
- Takes ~15 minutes

[Read: DEPLOYMENT_PYTHONANYWHERE.md](DEPLOYMENT_QUICKSTART.md#alternative-pythonanywhere)

**For specific instructions, see:**
- [DEPLOYMENT_QUICKSTART.md](DEPLOYMENT_QUICKSTART.md) - Start here!
- [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - Complete checklist
- [DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md) - What's been done

---

## 📧 Email Configuration (Password Reset)

The app is configured for Gmail-based password reset.

**Setup Required:**
1. Follow [GMAIL_SETUP_GUIDE.md](GMAIL_SETUP_GUIDE.md)
2. Generate Gmail App Password
3. Update `.env` file
4. Test with: `python test_email_config.py`

**Users can then:**
- Click "Forgot Password" on login
- Receive password reset link via email
- Set new password

---

## 📁 Project Structure

```
house-help/
├── config/                 # Django configuration
├── matchapp/              # Main app
│   ├── models.py          # Database models
│   ├── views.py           # Views and logic
│   ├── forms.py           # Django forms
│   ├── urls.py            # URL routing
│   └── migrations/        # Database migrations
├── templates/             # HTML templates
├── static/                # CSS, JavaScript, images
├── manage.py              # Django management
├── db.sqlite3             # SQLite database
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (local)
├── .env.example          # Template for .env
├── .gitignore            # Git exclusions
├── Procfile              # Production startup command
└── railway.json          # Railway deployment config
```

---

## 🔑 Key Commands

### Development
```bash
# Start development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell
```

### Deployment
```bash
# Collect static files
python manage.py collectstatic --noinput

# Test email config
python test_email_config.py

# Create test superuser
python create_test_superuser.py
```

### Git
```bash
# Initialize (already done)
git init

# Add all files
git add .

# Commit changes
git commit -m "Your message"

# Push to GitHub
git push origin main
```

---

## 🔐 Security

- ✅ Environment variables for secrets (`.env`)
- ✅ `.env` excluded from Git (in `.gitignore`)
- ✅ CSRF protection enabled
- ✅ SQL injection protection
- ✅ XSS prevention
- ✅ Secure password hashing
- ✅ HTTPS enforced in production

**Before Production:**
- Change `SECRET_KEY`
- Generate new `SECRET_KEY`: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- Set `DEBUG=False`
- Update `ALLOWED_HOSTS`

---

## 🗄️ Database

### Local Development
- SQLite (default)
- File: `db.sqlite3`

### Production
- PostgreSQL recommended
- MySQL supported
- Connection via `DATABASE_URL` environment variable

---

## 📧 Email Configuration

### Sender
- Email: `blaisengugi3@gmail.com`
- Type: Gmail SMTP

### Features
- Password reset emails
- User notifications
- Admin communications

### Setup
See [GMAIL_SETUP_GUIDE.md](GMAIL_SETUP_GUIDE.md)

---

## 🤝 Contributing

1. Create a new branch: `git checkout -b feature-name`
2. Make changes
3. Commit: `git commit -m "Feature description"`
4. Push: `git push origin feature-name`
5. Open Pull Request

---

## 📄 License

This project is open source.

---

## 📞 Support

### Documentation Files
- [DEPLOYMENT_QUICKSTART.md](DEPLOYMENT_QUICKSTART.md) - Start deployments
- [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - Complete checklist
- [DEPLOYMENT_SUMMARY.md](DEPLOYMENT_SUMMARY.md) - What's been completed
- [DEPLOYMENT_RAILWAY.md](DEPLOYMENT_RAILWAY.md) - Railway guide
- [DEPLOYMENT_PYTHONANYWHERE.md](DEPLOYMENT_PYTHONANYWHERE.md) - PythonAnywhere guide
- [GMAIL_SETUP_GUIDE.md](GMAIL_SETUP_GUIDE.md) - Email setup

### External Resources
- [Django Documentation](https://docs.djangoproject.com/en/4.2/)
- [Railway Docs](https://docs.railway.app/)
- [PythonAnywhere Help](https://help.pythonanywhere.com/)

---

## 📝 Environment Variables

### Required (Local Development)
```
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_HOST_PASSWORD=your-gmail-app-password
```

### Required (Production)
```
DEBUG=False
SECRET_KEY=generated-secret-key
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://...
EMAIL_HOST_PASSWORD=your-gmail-app-password
```

See `.env.example` for complete template.

---

## 🎯 Next Steps

1. **Local Testing**
   ```bash
   python manage.py runserver
   ```

2. **Gmail Setup**
   - Read [GMAIL_SETUP_GUIDE.md](GMAIL_SETUP_GUIDE.md)
   - Generate App Password
   - Update `.env`

3. **Deploy**
   - Push to GitHub
   - Follow [DEPLOYMENT_QUICKSTART.md](DEPLOYMENT_QUICKSTART.md)
   - Choose Railway or PythonAnywhere

4. **Go Live**
   - Visit your deployed app
   - Test all features
   - Monitor logs

---

**Status:** ✅ Ready for Production  
**Last Updated:** February 7, 2026  
**Version:** 1.0

---

Happy deploying! 🚀
