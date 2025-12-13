# Production Deployment Guide

## Overview
This guide explains how to deploy both the frontend (GitHub Pages) and backend (Auth Service) to production so that signup/signin works on your live GitHub Pages website.

## Architecture
```
GitHub Pages (Frontend)          Vercel (Auth Service)        Neon PostgreSQL
my-project/build/ -----HTTP----> auth-service/ -----DB----> neon.tech
https://your-domain.io           https://auth.vercel.app      (cloud database)
```

## Step 1: Setup Production Database (Neon)

### 1a. Create Neon Account
1. Go to https://neon.tech
2. Sign up with GitHub
3. Create a new project (e.g., "physical-ai-auth")
4. Copy the connection string (looks like: `postgresql://user:password@neon.tech/dbname`)

### 1b. Update Environment Variables
Edit `backend/auth-service/.env`:
```bash
DATABASE_URL=postgresql://user:password@neon.tech/dbname
NODE_ENV=production
CORS_ORIGINS=https://your-github-pages-domain.io
JWT_SECRET=your-secure-random-secret-key-here
```

## Step 2: Deploy Auth Service to Vercel

### 2a. Create Vercel Account
1. Go to https://vercel.com
2. Sign up with GitHub
3. Connect your GitHub repository

### 2b. Deploy Backend
```bash
cd backend/auth-service
vercel --prod
```

When prompted:
- Project name: `physical-ai-auth`
- Framework: `Other`

### 2c. Configure Environment Variables in Vercel
In Vercel dashboard → Settings → Environment Variables:
```
DATABASE_URL = postgresql://user:password@neon.tech/dbname
JWT_SECRET = your-secure-random-secret-key
CORS_ORIGINS = https://your-github-pages-domain.io
NODE_ENV = production
```

### 2d. Note Your Vercel URL
After deployment, you'll get a URL like:
```
https://physical-ai-auth.vercel.app
```

## Step 3: Update Frontend Configuration

### 3a. Update .env.production
Edit `my-project/.env.production`:
```bash
REACT_APP_AUTH_SERVICE_URL=https://physical-ai-auth.vercel.app
```

### 3b. Verify docusaurus.config.ts
Make sure your base URL is correct for GitHub Pages:
```typescript
const baseUrl = process.env.GITHUB_ACTIONS ? '/Physical-AI-Humanoid-Robotics/' : '/';
```

## Step 4: Deploy Frontend to GitHub Pages

The GitHub Actions workflow will automatically:
1. Build Docusaurus
2. Deploy to GitHub Pages
3. Use `.env.production` for environment variables

Push your changes:
```bash
git add .
git commit -m "feat: Configure production auth service URL"
git push origin main
```

GitHub Actions will automatically deploy within a few seconds.

## Step 5: Test Production Signup/Signin

1. Go to your GitHub Pages URL: `https://your-domain.io/Physical-AI-Humanoid-Robotics/`
2. Click "Sign Up"
3. Fill in the form and submit
4. Should redirect to homepage (no more "Failed to fetch" error!)

## Troubleshooting

### "Failed to fetch" on GitHub Pages
- Check that `REACT_APP_AUTH_SERVICE_URL` in `.env.production` is correct
- Verify auth service is deployed on Vercel and running
- Check CORS settings in auth service `.env`

### Auth service returns 500 error
- Check that `DATABASE_URL` is set correctly in Vercel
- Run migrations on Neon: `alembic upgrade head` (from your local machine)
- Check Vercel logs for detailed error

### CORS errors
- Update `CORS_ORIGINS` in backend/.env to include your GitHub Pages domain
- Redeploy to Vercel

## Local Development (Still Works)

For local development, you don't need to change anything:
- Frontend uses default `http://localhost:3001`
- Auth service runs locally on port 3001
- Database uses local PostgreSQL

Just run:
```bash
# Terminal 1
cd backend/auth-service && npm run dev

# Terminal 2
cd my-project && npm run start
```

## Environment Variables Summary

### Frontend (.env.production)
```
REACT_APP_AUTH_SERVICE_URL = https://physical-ai-auth.vercel.app
```

### Backend (.env)
```
DATABASE_URL = postgresql://neon.tech connection
NODE_ENV = production
CORS_ORIGINS = https://your-github-pages-domain.io
JWT_SECRET = secure-random-key
```

## Next Steps

After successfully deploying:
1. Test signup/signin on production
2. Implement Iteration 3 (Frontend Auth UI - React contexts)
3. Add user profile management
4. Setup CI/CD for automated deployments

---

**Your production site will be live at:**
- Frontend: `https://your-github-pages-domain.io/Physical-AI-Humanoid-Robotics/`
- Auth API: `https://physical-ai-auth.vercel.app/api/auth/*`
