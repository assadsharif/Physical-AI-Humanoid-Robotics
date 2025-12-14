# Vercel Deployment Setup - Manual Steps

## Prerequisites ✅
- Vercel account connected with GitHub (assadsharif) ✅
- Neon database created ✅
- Environment variables configured in `.env` ✅

## Step 1: Deploy Auth Service to Vercel (Web Interface)

### 1.1 Go to Vercel Dashboard
1. Visit https://vercel.com/dashboard
2. Click "Add New..." → "Project"

### 1.2 Import Repository
1. Select your repository: `Physical-AI-Humanoid-Robotics`
2. Click "Import"

### 1.3 Configure Project
1. **Project Name:** `physical-ai-auth`
2. **Framework Preset:** Select "Other" (Node.js)
3. **Root Directory:** Set to `backend/auth-service`

### 1.4 Environment Variables
Add these environment variables:

```
DATABASE_URL = postgresql://neondb_owner:npg_6DWLmMEO8gQC@ep-wandering-resonance-ahixh4sd-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require

JWT_SECRET = super-secret-jwt-key-physical-ai-2024-production

JWT_ALGORITHM = RS256

JWT_EXPIRATION = 86400

PORT = 3001

NODE_ENV = production

CORS_ORIGINS = http://localhost:3000,http://localhost:5000,https://assadsharif.github.io

LOG_LEVEL = info

RATE_LIMIT_WINDOW_MS = 900000

RATE_LIMIT_MAX_REQUESTS = 5
```

### 1.5 Deploy
1. Click "Deploy"
2. Wait for deployment to complete (~2-3 minutes)
3. Once done, you'll see a URL like: `https://physical-ai-auth.vercel.app`

**IMPORTANT: Copy this URL - you'll need it for the next step!**

---

## Step 2: Update Frontend with Auth Service URL

Once you have your Vercel URL from Step 1:

### 2.1 Edit `.env.production`
Open `my-project/.env.production` and update:

```bash
REACT_APP_AUTH_SERVICE_URL=https://physical-ai-auth.vercel.app
```

(Replace with your actual Vercel URL if different)

### 2.2 Commit and Push
```bash
cd /mnt/c/Users/ASSAD/Desktop/code/hackathon_01
git add backend/auth-service/.env my-project/.env.production backend/auth-service/.vercelignore
git commit -m "chore: Configure Vercel deployment with Neon database"
git push origin main
```

GitHub Actions will automatically rebuild and deploy your site!

---

## Step 3: Run Database Migrations

After the auth service is deployed, run migrations on Neon:

```bash
cd /mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend

# Install dependencies if needed
pip install alembic sqlalchemy psycopg2-binary python-dotenv

# Run migrations on production database
export DATABASE_URL="postgresql://neondb_owner:npg_6DWLmMEO8gQC@ep-wandering-resonance-ahixh4sd-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

alembic upgrade head
```

---

## Step 4: Test Production Signup/Signin

1. Wait ~2 minutes for GitHub Pages to rebuild
2. Visit: https://assadsharif.github.io/Physical-AI-Humanoid-Robotics/
3. Click "Sign Up"
4. Fill in the form:
   - Name: Test User
   - Email: test@example.com
   - Password: TestPass123!
   - Confirm: TestPass123!
5. Click "Create Account"
6. Should redirect to homepage ✅

---

## Troubleshooting

### "Failed to fetch" on GitHub Pages
- Check that `.env.production` has correct Vercel URL
- Verify auth service is deployed and running on Vercel
- Check Vercel logs for errors

### Auth service shows 500 error
- Check that DATABASE_URL is correct
- Run migrations: `alembic upgrade head`
- Check Vercel logs in dashboard

### CORS errors
- Verify CORS_ORIGINS includes `https://assadsharif.github.io`
- Redeploy to Vercel after updating

---

## What Was Done (Files Already Configured)

✅ `backend/auth-service/.env` - Configured with:
  - Neon database URL
  - Production JWT secret
  - CORS origins including GitHub Pages
  - NODE_ENV=production

✅ `backend/auth-service/vercel.json` - Vercel deployment config

✅ `backend/auth-service/.vercelignore` - Files to exclude from deployment

✅ `my-project/.env.production` - Will use Vercel auth URL at build time

✅ `my-project/src/pages/auth/signup.tsx` - Reads auth URL from environment variable

✅ `my-project/src/pages/auth/signin.tsx` - Reads auth URL from environment variable

---

## Summary

1. **Deploy to Vercel** (via web interface, ~5 minutes)
2. **Copy Vercel URL** and update `.env.production`
3. **Push to GitHub** (Actions auto-deploys, ~2 minutes)
4. **Run migrations** on Neon database
5. **Test signup/signin** on GitHub Pages

**Total time: ~15 minutes**

After this, signup/signin will work on your live GitHub Pages site! 🎉
