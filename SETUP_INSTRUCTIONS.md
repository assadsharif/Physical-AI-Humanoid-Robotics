# Setup Instructions - Physical AI & Humanoid Robotics Project

## Prerequisites

- Node.js 20+ (LTS)
- npm 10+
- PostgreSQL 15+ running locally OR Docker
- Git

## Quick Start

### 1. Start PostgreSQL (if not running)

**Option A: Using Docker (Recommended)**
```bash
docker run --name postgres-auth \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=auth_dev \
  -p 5432:5432 \
  -d postgres:15-alpine
```

**Option B: Using existing PostgreSQL**
```bash
# Make sure PostgreSQL is running on localhost:5432
psql -U postgres -c "CREATE DATABASE auth_dev;"
```

### 2. Setup Better-Auth Service

```bash
# Navigate to auth service
cd backend/auth-service

# Install dependencies
npm install

# Build TypeScript
npm run build

# Start the service (development with hot reload)
npm run dev

# OR run compiled version
npm start
```

**Expected output:**
```
Auth service listening on port 3001
Environment: development
CORS origins: http://localhost:3000, http://localhost:5000
Ready to accept requests
```

If you see database connection errors, make sure PostgreSQL is running on `localhost:5432`.

### 3. Run Database Migrations

**In a new terminal:**
```bash
cd backend

# Install Python dependencies (if needed)
pip install alembic sqlalchemy psycopg2-binary python-dotenv

# Create .env file for Alembic (optional, uses DATABASE_URL from backend/auth-service/.env)
# or set environment variable:
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/auth_dev"

# Run migrations
alembic upgrade head
```

**Expected output:**
```
INFO  [alembic.runtime.migration] Running upgrade  -> 001_create_better_auth_tables.py
...
```

### 4. Start Docusaurus Frontend

**In another terminal:**
```bash
cd my-project

# Install dependencies
npm install

# Start development server
npm run start
```

**Expected output:**
```
Docusaurus site running at: http://localhost:3000
```

## Verify Everything Works

### 1. Check Auth Service
```bash
curl http://localhost:3001/
```

Expected response:
```json
{
  "name": "Better-Auth Service",
  "version": "1.0.0",
  "status": "running",
  "endpoints": {...}
}
```

### 2. Check Health Endpoint
```bash
curl http://localhost:3001/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-12-14T..."
}
```

### 3. Test in Browser
1. Open http://localhost:3000 (Docusaurus site)
2. Click "Sign Up" button (top-right navbar)
3. Fill form:
   - Name: Test User
   - Email: test@example.com
   - Password: TestPass123!
   - Confirm: TestPass123!
   - Experience: Beginner
4. Click "Create Account"
5. Should redirect to homepage

## Troubleshooting

### "Failed to fetch" error on signup
**Problem:** Auth service not running
**Solution:**
- Check terminal 1: `npm run dev` in `backend/auth-service`
- Verify it's on port 3001
- Check for database connection errors

### "404 error" on signin
**Problem:** Auth endpoints not responding
**Solution:**
- Verify auth service started correctly (see above)
- Check logs for errors
- Make sure better-auth routes are mounted

### "Connection refused" on migrations
**Problem:** PostgreSQL not running
**Solution:**
```bash
# Check if PostgreSQL is running
psql -U postgres -c "SELECT 1;"

# If not, start Docker container (if using Docker)
docker start postgres-auth

# Or install/start local PostgreSQL
# macOS: brew services start postgresql
# Linux: sudo systemctl start postgresql
# Windows: Services -> PostgreSQL
```

### Database already exists error
**Problem:** Migration tries to create tables that exist
**Solution:**
```bash
# Drop and recreate (caution: destroys data)
psql -U postgres -c "DROP DATABASE auth_dev; CREATE DATABASE auth_dev;"

# Then rerun migrations
alembic upgrade head
```

### Port 3001 already in use
**Problem:** Another service using port 3001
**Solution:**
```bash
# Find process using port 3001
lsof -i :3001

# Kill it
kill -9 <PID>

# Or change port in .env
PORT=3002
```

## Environment Variables

### Backend (.env)
Located in `backend/auth-service/.env`:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/auth_dev
PORT=3001
NODE_ENV=development
CORS_ORIGINS=http://localhost:3000,http://localhost:5000
LOG_LEVEL=debug
```

### Frontend
No special env vars needed for local development.

## File Structure

```
project/
├── backend/
│   ├── auth-service/          # Better-Auth service (TypeScript/Express)
│   │   ├── src/
│   │   │   ├── auth.ts        # Better-Auth configuration
│   │   │   ├── server.ts      # Express server
│   │   │   ├── routes/        # API routes
│   │   │   ├── middleware/    # Error handling, auth middleware
│   │   │   └── utils/         # Logger
│   │   ├── dist/              # Compiled JavaScript
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   └── .env
│   ├── alembic/               # Database migrations
│   │   ├── versions/          # Migration files
│   │   └── env.py             # Alembic config
│   └── alembic.ini
│
└── my-project/                 # Docusaurus frontend
    ├── src/
    │   ├── pages/
    │   │   ├── auth/          # Auth pages (signin, signup)
    │   │   └── index.tsx      # Home page
    │   └── components/        # React components
    └── package.json
```

## Common Commands

```bash
# Auth Service
cd backend/auth-service
npm install                    # Install dependencies
npm run build                  # Build TypeScript
npm run dev                    # Start with hot reload
npm start                      # Start compiled version
npm test                       # Run tests (Playwright)

# Database
cd backend
alembic upgrade head          # Run migrations
alembic downgrade -1          # Rollback last migration
alembic current               # Check current version

# Frontend
cd my-project
npm install                   # Install dependencies
npm run start                 # Start dev server
npm run build                 # Build for production
npm run serve                 # Serve production build
```

## Next Steps

1. ✅ Start auth service: `npm run dev` in `backend/auth-service`
2. ✅ Run migrations: `alembic upgrade head` in `backend`
3. ✅ Start frontend: `npm run start` in `my-project`
4. ✅ Test signup/signin in browser
5. **Coming next:**
   - Connect ChatWidget to use JWT token
   - Add logout functionality
   - Show user profile in navbar

## Support

For detailed documentation:
- Better-Auth: https://www.better-auth.com/docs
- Docusaurus: https://docusaurus.io
- Alembic: https://alembic.sqlalchemy.org
