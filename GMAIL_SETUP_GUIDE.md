# Gmail Password Reset - Setup Instructions

## ⚠️ Important Setup Required

Your House-Help app is configured for Gmail password reset, but **Gmail requires additional setup** for the current configuration to work.

### The Issue

Gmail rejected the password. This is normal - Google no longer allows regular account passwords for third-party apps for security reasons.

### Solution: Use Gmail App Password (Recommended)

**Step 1: Enable 2-Factor Authentication on Gmail**
1. Go to https://myaccount.google.com/
2. Click **Security** (left menu)
3. Scroll to "2-Step Verification"
4. Click it → **Get Started**
5. Follow steps to verify your phone
6. Confirm 2FA is enabled

**Step 2: Generate App Password**
1. Go back to Security: https://myaccount.google.com/security
2. Scroll down to "App passwords" (appears after 2FA is enabled)
3. Select:
   - App: **Mail**
   - Device: **Windows Computer** (or your device)
4. Click **Generate**
5. Google will show a 16-character password

**Step 3: Update .env File**
Edit `.env` and replace the password:

```
EMAIL_HOST_USER=blaisengugi3@gmail.com
EMAIL_HOST_PASSWORD=<paste-16-char-app-password-here>
# Example: EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
```

**Step 4: Test Again**
```bash
python test_email_config.py
```

You should see: ✅ SUCCESS! Test email sent successfully!

---

## Alternative: Enable Less Secure Apps (Not Recommended)

If you don't want to use App Password, you can enable Less Secure Apps:

1. Go to https://myaccount.google.com/security
2. Scroll to "Less secure app access"
3. Turn it **ON**

⚠️ **Warning:** This reduces your account security. Using App Password is better.

---

## How Password Reset Works (Once Configured)

### For Your Users:
1. User visits login page → clicks "Forgot Password?"
2. User enters their email
3. Django sends password reset email via Gmail
4. Email comes from: `blaisengugi3@gmail.com`
5. User clicks link in email
6. User sets new password

### The Email Template
You can customize the password reset email:

File: `templates/registration/password_reset_email.html`

Current template sends:
- Password reset link
- Link expiration time (usually 1-3 days)
- Instructions to set new password

---

## Testing the Setup

### Option 1: Via Shell (Manual)
```bash
python manage.py shell

# In Python shell:
from django.core.mail import send_mail
from django.conf import settings

send_mail(
    'Test Subject',
    'Test Message Body',
    settings.DEFAULT_FROM_EMAIL,
    ['blaisengugi3@gmail.com'],
    fail_silently=False,
)
```

### Option 2: Via Script
```bash
python test_email_config.py
```

### Option 3: Via Django Admin
1. Run: `python manage.py runserver`
2. Visit: `http://localhost:8000/admin/auth/user/`
3. Click admin user
4. Click "Password Reset" link at bottom
5. Check if email is sent

---

## Production Deployment

Once you've set up the App Password:

### With Railway:
1. Add environment variable in Railway dashboard:
   - Key: `EMAIL_HOST_PASSWORD`
   - Value: (your 16-char app password)

### With PythonAnywhere:
1. In `.env` file (on server):
   - Update with app password
2. Restart web app

---

## Security Notes

✅ **Good:**
- Gmail credentials are in `.env` file (not in code)
- `.env` is in `.gitignore` (not committed to Git)
- Different password for this app (App Password)
- HTTPS enabled automatically on Railway/PythonAnywhere

⚠️ **Remember:**
- Never commit `.env` to Git
- Rotate app password every 6 months
- If password is exposed: delete and create new one
- Never share your password in emails/chat

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Username and Password not accepted" | Use 16-char app password, not Gmail password |
| "2-Step Verification not enabled" | Enable 2FA first, then app password appears |
| "Less secure apps access turned off" | Enable in Gmail security settings |
| Emails still not sending | Check internet connection, restart app |
| Email goes to spam | Add reply filter in Gmail, whitelist sender |

---

## Next Steps

1. **Set up Gmail App Password** (follow steps above)
2. **Update .env file** with the app password
3. **Test email** with: `python test_email_config.py`
4. **Deploy to Railway/PythonAnywhere** (see [DEPLOYMENT_QUICKSTART.md](DEPLOYMENT_QUICKSTART.md))

Once done, your password reset feature will work perfectly! ✅

Need help? Check Django's official email documentation:
https://docs.djangoproject.com/en/4.2/topics/email/
