# 🚨 FIX: Add Environment Variables to Vercel Dashboard

## Why Deployments Are Failing

Your auth service deployments are failing because **Vercel doesn't have the required environment variables set**. The `.env` file is in `.gitignore` for security, so it's not on GitHub, which means Vercel doesn't see it.

**Fix: Add environment variables in Vercel Dashboard (2 minutes)**

---

## Step 1: Go to Your Vercel Project Settings

```
Open: https://vercel.com/dashboard
```

**Click:** Your project: `physical_ai_auth`

---

## Step 2: Open Settings Tab

**You'll see these tabs at the top:**
```
Deployments | Preview Deployments | Settings | Monitoring
                                     ↑
                                  Click here
```

---

## Step 3: Find Environment Variables Section

**In Settings tab, scroll down to find:**
```
Environment Variables
(or Search for "Environment Variables" on the page)
```

---

## Step 4: Add ALL 8 Variables

**Click:** "Add New..." for each variable

**Add these exactly (copy-paste the values):**

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

---

## Step 5: Save and Redeploy

**After adding all 8 variables:**

1. Scroll up to "Deployments" tab
2. Find the latest failed deployment (the red one)
3. Click the three dots `...` and select "Redeploy"
4. Wait 2-3 minutes for deployment
5. Should show ✅ Success!

---

## Verification Checklist

After successful deployment, you should see:
- ✅ Green "Success" badge on the deployment
- ✅ A URL like: `https://physical-ai-auth.vercel.app`
- ✅ Endpoint works: Visit `https://physical-ai-auth.vercel.app/api/health` → shows `{"status":"healthy"}`

---

## Then Update Frontend (One Last Step)

Once deployment succeeds, edit:

**File:** `/my-project/.env.production`

**Confirm it has:**
```
REACT_APP_AUTH_SERVICE_URL=https://physical-ai-auth.vercel.app
```

(Or update with your actual Vercel URL if different)

Then:
```bash
git add my-project/.env.production
git commit -m "Fix: Update production auth URL"
git push origin main
```

GitHub Actions will automatically rebuild and redeploy GitHub Pages.

---

## After ~2 minutes, test:

1. Visit: https://assadsharif.github.io/Physical-AI-Humanoid-Robotics/
2. Click "Sign Up"
3. Fill in:
   - Name: Test User
   - Email: test@example.com
   - Password: TestPass123!
   - Confirm: TestPass123!
4. Click "Create Account"
5. Should redirect to homepage ✅

---

## Need Help?

If you get stuck on any of these steps, let me know and I can walk you through it or help diagnose errors.

The key thing is: **You must set the 8 environment variables in Vercel Dashboard before the deployment will work.**
