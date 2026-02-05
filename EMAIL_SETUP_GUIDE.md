# Email Notification Setup Guide

## Overview
The system now automatically sends email notifications to users when they:
- ⚠️ Receive a warning for violating community guidelines
- ⛔ Get suspended after multiple violations

## Email Configuration

### Step 1: Choose Your Email Provider

#### Option A: Gmail (Recommended)
1. **Enable 2-Factor Authentication** on your Google account
2. **Generate an App Password:**
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Name it "Hate Speech Detection System"
   - Copy the 16-character password

3. **Update `.env` file:**
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-16-char-app-password
```

#### Option B: Outlook/Hotmail
```env
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SENDER_EMAIL=your-email@outlook.com
SENDER_PASSWORD=your-password
```

#### Option C: Yahoo Mail
```env
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
SENDER_EMAIL=your-email@yahoo.com
SENDER_PASSWORD=your-app-password
```

#### Option D: Custom SMTP Server
```env
SMTP_SERVER=smtp.yourserver.com
SMTP_PORT=587
SENDER_EMAIL=noreply@yourdomain.com
SENDER_PASSWORD=your-password
```

### Step 2: Edit Configuration File

1. Open `C:\Users\nakka\Desktop\pp1\.env`
2. Find the Email Configuration section
3. Uncomment and fill in your SMTP details:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
```

4. Save the file

### Step 3: Restart Backend

Restart the backend server for changes to take effect:

```powershell
# Stop current backend
taskkill /F /IM python.exe

# Start backend again
C:/Users/nakka/Desktop/pp1/.venv/Scripts/python.exe run_backend.py
```

---

## Testing Email Configuration

### Method 1: API Endpoint

Test if email is working:

```powershell
# Test email
$body = @{ email = "test@example.com" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5000/api/admin/email/test" -Method POST -Body $body -ContentType "application/json"
```

### Method 2: Check Status

Check if email is configured:

```powershell
Invoke-RestMethod -Uri "http://localhost:5000/api/admin/email/status"
```

---

## Email Templates

### Warning Email
Sent when a user violates community guidelines:
- Shows warning count (e.g., "Warning 1 of 3")
- Displays the violating content
- Lists violation category (hate speech type)
- Warns about potential suspension

### Suspension Email
Sent when a user is suspended:
- Notifies of account suspension
- Shows final violation that triggered suspension
- Lists total violation count
- Provides appeal information

---

## Email Triggers

Emails are automatically sent in these scenarios:

### 1. Automated Detection
When a user posts hate speech content:
```
User posts → AI detects hate speech → Violation logged → Warning email sent
```

### 2. Manual Warning (Admin)
When an admin manually warns a user:
```
Admin dashboard → Warn user → Warning email sent
```

### 3. Manual Suspension (Admin)
When an admin manually suspends a user:
```
Admin dashboard → Suspend user → Suspension email sent
```

### 4. Automatic Suspension
When a user reaches maximum warnings:
```
3rd violation → Auto-suspension → Suspension email sent
```

---

## API Endpoints

### Test Email
```
POST /api/admin/email/test
Body: { "email": "test@example.com" }
```

### Check Email Status
```
GET /api/admin/email/status
```

### Warn User (with email)
```
POST /api/users/{user_id}/warn
Body: { 
  "reason": "hate speech",
  "content": "The violating content"
}
```

### Suspend User (with email)
```
POST /api/users/{user_id}/suspend
Body: {
  "reason": "repeated violations",
  "content": "Final violation content"
}
```

---

## Disabling Email Notifications

To disable email notifications, leave the SMTP settings blank in `.env`:

```env
SMTP_SERVER=
SMTP_PORT=
SENDER_EMAIL=
SENDER_PASSWORD=
```

The system will continue to work normally, but won't send emails. Console logs will show:
```
📧 [EMAIL DISABLED] Would send to user@example.com: Warning notification
```

---

## Troubleshooting

### Issue: "Email service not configured"
**Solution:** Fill in SMTP settings in `.env` and restart backend

### Issue: "Authentication failed"
**Solution:** 
- For Gmail: Use App Password, not regular password
- For other providers: Check username/password
- Verify 2FA is enabled (Gmail/Yahoo)

### Issue: "Connection refused"
**Solution:**
- Check SMTP server address
- Verify port (usually 587 for TLS)
- Check firewall settings

### Issue: "Emails not being received"
**Solution:**
- Check spam/junk folder
- Verify recipient email is correct
- Test with the `/api/admin/email/test` endpoint

---

## Security Best Practices

1. ✅ **Use App-Specific Passwords** (not your main password)
2. ✅ **Enable 2-Factor Authentication** on email account
3. ✅ **Never commit `.env` file** to version control
4. ✅ **Use a dedicated email account** for the system
5. ✅ **Rotate passwords regularly**

---

## Example: Complete Setup with Gmail

1. **Create App Password:**
   - Visit: https://myaccount.google.com/apppasswords
   - Generate password: `abcd efgh ijkl mnop`

2. **Edit `.env`:**
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=myproject@gmail.com
SENDER_PASSWORD=abcdefghijklmnop
```

3. **Restart Backend:**
```powershell
C:/Users/nakka/Desktop/pp1/.venv/Scripts/python.exe run_backend.py
```

4. **Test:**
```powershell
# Test with your email
$test = @{ email = "your-email@gmail.com" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5000/api/admin/email/test" -Method POST -Body $test -ContentType "application/json"
```

5. **Check your inbox** for the test email!

---

## Summary

✅ Email service created: `backend/utils/email_service.py`
✅ Warning emails: Sent automatically when users get warnings
✅ Suspension emails: Sent when users are suspended
✅ Configuration: Add SMTP details to `.env` file
✅ Testing: Use `/api/admin/email/test` endpoint
✅ Disable: Leave SMTP settings blank in `.env`

**Ready to use!** Just configure your SMTP settings and restart the backend.
