# Vercel Deployment Guide

## Quick Deploy

1. **Connect GitHub Repository to Vercel**
   - Go to https://vercel.com
   - Sign in with GitHub
   - Click "Add New Project"
   - Select `stephenkarim-rgb/spinners-portal`
   - Click "Import"

2. **Configure Environment Variables**
   - In the Vercel dashboard, go to Settings → Environment Variables
   - Add these variables:
     ```
     DEBUG = False
     SECRET_KEY = (Vercel will generate a random one, or provide your own)
     ALLOWED_HOSTS = your-project.vercel.app
     CSRF_TRUSTED_ORIGINS = https://your-project.vercel.app
     ```

3. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete (5-10 minutes)
   - Your app will be live at: `https://spinners-portal.vercel.app`

## Important Notes

- **Database**: This setup uses SQLite which is NOT suitable for Vercel (ephemeral filesystem)
  - For production, consider using PostgreSQL with a managed service
  - Or use a cloud storage solution for the database file

- **Static Files**: WhiteNoise handles static file serving in production

- **Environment Variables**: Set all required variables in Vercel dashboard

## Troubleshooting

If deployment fails:
1. Check the Vercel logs in the dashboard
2. Verify all environment variables are set
3. Ensure requirements.txt is up to date

## For PostgreSQL (Recommended)

1. Add `psycopg2-binary` to requirements.txt
2. Set `DATABASE_URL` environment variable in Vercel
3. Update Django settings to use DATABASE_URL

Example:
```python
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}
```
