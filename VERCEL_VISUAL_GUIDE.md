# 🚀 Visual Guide: Deploy Auth Service to Vercel (5 Minutes)

## Step 1: Open Vercel Dashboard
```
Go to: https://vercel.com/dashboard
```

**Click:** "Add New..." → "Project"

---

## Step 2: Import Your Repository

**You'll see this screen:**
```
┌─────────────────────────────────┐
│ Import Git Repository           │
│                                 │
│ Your repositories:              │
│ ✓ Physical-AI-Humanoid-Robotics │
│                                 │
│ [Import] ←── Click here         │
└─────────────────────────────────┘
```

**Click:** The repository name → "Import"

---

## Step 3: Configure Project

**You'll see this form:**
```
┌─────────────────────────────────────────┐
│ Configure Project                       │
│                                         │
│ Project Name: physical-ai-auth          │
│ Framework: Other (Node.js)              │
│ Root Directory: backend/auth-service ←─ CHANGE THIS
│                                         │
│ [Deploy] ←── Click after setup          │
└─────────────────────────────────────────┘
```

**Change Root Directory to:** `backend/auth-service`

---

## Step 4: Add Environment Variables

**Click:** "Environment Variables" (bottom of form)

**Add these 9 variables** (click "Add New" for each):

| Key | Value |
|-----|-------|
| `DATABASE_URL` | `postgresql://neondb_owner:npg_6DWLmMEO8gQC@ep-wandering-resonance-ahixh4sd-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require` |
| `JWT_SECRET` | `super-secret-jwt-key-physical-ai-2024-production` |
| `JWT_ALGORITHM` | `RS256` |
| `JWT_EXPIRATION` | `86400` |
| `PORT` | `3001` |
| `NODE_ENV` | `production` |
| `CORS_ORIGINS` | `http://localhost:3000,http://localhost:5000,https://assadsharif.github.io` |
| `LOG_LEVEL` | `info` |
| `RATE_LIMIT_WINDOW_MS` | `900000` |

**Form looks like:**
```
┌────────────────────────────────────┐
│ Environment Variables              │
│                                    │
│ DATABASE_URL ────────────────────  │
│ (paste Neon URL here)              │
│                                    │
│ JWT_SECRET ────────────────────    │
│ super-secret-jwt-key-...           │
│                                    │
│ JWT_ALGORITHM ────────────────     │
│ RS256                              │
│ ... (add all 9 variables)          │
│                                    │
└────────────────────────────────────┘
```

---

## Step 5: Deploy!

**Click:** The big blue "Deploy" button

```
You'll see:
┌─────────────────────────┐
│ ⏳ Uploading...        │
│ ⏳ Building...         │
│ ⏳ Finalizing...       │
│ ✅ DEPLOYMENT SUCCESS! │
│                         │
│ Visit:                  │
│ https://physical-ai-... │
│   ↑                     │
│   COPY THIS URL         │
└─────────────────────────┘
```

---

## Step 6: Copy Your Vercel URL

**Your deployed auth service URL will be:**
```
https://physical-ai-auth.vercel.app
```

(The exact URL is shown at the top of the deployment page)

---

## Step 7: Update Frontend

Edit the file: `my-project/.env.production`

**Change this line to match your Vercel URL:**
```bash
REACT_APP_AUTH_SERVICE_URL=https://physical-ai-auth.vercel.app
```

---

## Step 8: Push to GitHub

**In terminal:**
```bash
cd /mnt/c/Users/ASSAD/Desktop/code/hackathon_01

git add my-project/.env.production
git commit -m "Update production auth URL to Vercel"
git push origin main
```

**GitHub Actions will automatically:**
- ✅ Build your site
- ✅ Deploy to GitHub Pages
- ✅ Use the production auth URL

---

## Step 9: Test It! 🎉

**Wait 2 minutes, then visit:**
```
https://assadsharif.github.io/Physical-AI-Humanoid-Robotics/
```

**Click "Sign Up"**
```
Fill in:
- Name: Test User
- Email: test@example.com
- Password: TestPass123!
- Confirm: TestPass123!

Click "Create Account"

Should redirect to homepage ✅
(No more "Failed to fetch" error!)
```

---

## ✅ Done!

Your signup/signin now works on GitHub Pages! 🚀

**What happened:**
- Auth service deployed to Vercel (scalable, fast)
- Uses Neon database (cloud PostgreSQL)
- Frontend talks to Vercel auth service
- GitHub Pages doesn't need backend

---

## If Something Goes Wrong

**Check Vercel Dashboard:**
1. Click your project
2. Deployments tab
3. Click the latest deployment
4. Check logs for errors

**Common issues:**
- DATABASE_URL wrong → Copy from Neon again
- CORS_ORIGINS missing GitHub Pages → Add it
- ENV vars not set → Redeploy after setting them

See `VERCEL_DEPLOYMENT_SETUP.md` for detailed troubleshooting.
