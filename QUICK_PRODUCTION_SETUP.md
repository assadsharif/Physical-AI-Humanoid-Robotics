# Quick Production Setup for GitHub Pages Signup/Signin

## The Real Issue
Your GitHub Pages site couldn't call signup/signin because:
- Frontend was hardcoded to `http://localhost:3001`
- Auth service wasn't deployed anywhere
- GitHub Pages runs in a browser, can't access your local machine

## The Solution (3 Simple Steps)

### Step 1: Create Free Neon Database (2 minutes)
```bash
1. Go to https://neon.tech
2. Sign up with GitHub
3. Create project → Copy connection string
4. Save it for later
```

### Step 2: Deploy Auth Service to Vercel (5 minutes)
```bash
1. Go to https://vercel.com
2. Sign up with GitHub
3. Click "Add new project" → select your repo
4. Select `backend/auth-service` directory
5. Add Environment Variables:
   - DATABASE_URL = (paste from Neon)
   - JWT_SECRET = (create secure random string)
   - CORS_ORIGINS = https://assadsharif.github.io/Physical-AI-Humanoid-Robotics/
   - NODE_ENV = production
6. Deploy
7. Copy your Vercel URL (e.g., https://physical-ai-auth.vercel.app)
```

### Step 3: Update Frontend (1 minute)
Edit `my-project/.env.production`:
```bash
REACT_APP_AUTH_SERVICE_URL=https://physical-ai-auth.vercel.app
```
Then:
```bash
git add my-project/.env.production
git commit -m "Update production auth URL"
git push origin main
```

## That's It! 🚀

After ~1 minute, GitHub Actions will rebuild and deploy. Your signup/signin will work on GitHub Pages!

## Test It
1. Go to your GitHub Pages: https://assadsharif.github.io/Physical-AI-Humanoid-Robotics/
2. Click "Sign Up"
3. Fill form → Click "Create Account"
4. Should redirect to homepage (no "Failed to fetch" error!)

## Local Development (Still Works)
No changes needed. Continue using:
```bash
cd backend/auth-service && npm run dev
cd my-project && npm run start
```

---

**Read `PRODUCTION_DEPLOYMENT.md` for detailed instructions and troubleshooting.**
