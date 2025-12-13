# Atomic Tasks: Auth Foundation (Iteration 1)

**Spec**: `specs/auth-foundation/spec.md`
**Plan**: `specs/auth-foundation/plan.md`
**Status**: Ready for Execution

---

## Task Format

- **[ID]** - Task identifier
- **[P?]** - Can execute in parallel (P = yes, blank = sequential dependency)
- **[Story]** - Links to user story (US1-US5 from spec)
- **Description** - What needs to be done
- **Verification** - How to verify completion

All file paths are **absolute** paths.

---

## Phase 1: Project Setup

### [T1.1] [P] Create auth-service directory structure

**Story**: M1.1
**Description**:
Create the basic directory structure for the better-auth service:
- `/mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend/auth-service/`
- `/mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend/auth-service/src/`
- `/mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend/auth-service/src/routes/`
- `/mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend/auth-service/src/middleware/`
- `/mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend/auth-service/src/utils/`

**Verification**:
```bash
ls -la /mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend/auth-service/src/
# Should show: routes/, middleware/, utils/ directories
```

---

### [T1.2] [P] Create package.json for auth-service

**Story**: M1.1
**Description**:
Create `/mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend/auth-service/package.json` with:
- `"name": "auth-service"`
- `"version": "1.0.0"`
- `"type": "module"` (ESM)
- Dependencies:
  - `better-auth@latest`
  - `express@4.18.0+`
  - `pg@8.8.0+` (Postgres client)
  - `dotenv@16.0.0+`
  - `cors@2.8.5+`
  - `express-rate-limit@7.0.0+`
  - `winston@3.11.0+` or `pino@8.0.0+` (logger)
- DevDependencies:
  - `typescript@5.3.0+`
  - `@types/node@20.0.0+`
  - `@types/express@4.17.0+`
  - `tsx@4.0.0+` (TypeScript executor)
- Scripts:
  - `"dev"`: `tsx watch src/server.ts`
  - `"build"`: `tsc`
  - `"start"`: `node dist/server.js`
  - `"test"`: `playwright test` (later)

**Verification**:
```bash
cd /mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend/auth-service
npm install
npm list
# Should show all dependencies installed without errors
```

---

### [T1.3] [P] Create tsconfig.json

**Story**: M1.1
**Description**:
Create `/mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend/auth-service/tsconfig.json` with:
- `"target": "ES2020"`
- `"module": "ESNext"`
- `"moduleResolution": "node"`
- `"strict": true`
- `"esModuleInterop": true`
- `"skipLibCheck": true`
- `"forceConsistentCasingInFileNames": true`
- `"resolveJsonModule": true`
- `"outDir": "./dist"`
- `"rootDir": "./src"`

**Verification**:
```bash
cd /mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend/auth-service
npx tsc --version
# Should show TypeScript is installed and working
```

---

### [T1.4] [P] Create .env and .env.example

**Story**: M1.1
**Description**:
Create two files:

**`/mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend/auth-service/.env.example`**:
```bash
# Database Connection
DATABASE_URL=postgresql://user:password@neon-host/auth_db

# JWT Configuration
JWT_SECRET=your-jwt-secret-key
JWT_ALGORITHM=RS256
JWT_EXPIRATION=86400

# Service Configuration
PORT=3001
NODE_ENV=development
CORS_ORIGINS=http://localhost:3000,http://localhost:5000

# Rate Limiting
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=5

# Logging
LOG_LEVEL=info
```

**`/mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend/auth-service/.env`**:
```bash
# (Copy from .env.example and fill in actual values for local dev)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/auth_dev
JWT_SECRET=dev-secret-key-change-in-production
JWT_ALGORITHM=RS256
JWT_EXPIRATION=86400
PORT=3001
NODE_ENV=development
CORS_ORIGINS=http://localhost:3000,http://localhost:5000
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX_REQUESTS=5
LOG_LEVEL=debug
```

**Verification**:
```bash
ls -la /mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend/auth-service/.env*
# Should show both .env and .env.example
cat /mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend/auth-service/.env.example | head -5
# Should show DATABASE_URL and other vars
```

---

### [T1.5] [P] Create .gitignore

**Story**: M1.1
**Description**:
Create `/mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend/auth-service/.gitignore`:
```
node_modules/
dist/
.env
.env.local
.DS_Store
*.log
.vscode/
.idea/
```

**Verification**:
```bash
cat /mnt/c/Users/AJAX/Desktop/code/hackathon_01/backend/auth-service/.gitignore
# Should show node_modules, dist, .env excluded
```

---

### [T1.6] [P] Create Dockerfile

**Story**: M1.1
**Description**:
Create `/mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend/auth-service/Dockerfile`:
```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY dist ./dist

EXPOSE 3001

CMD ["node", "dist/server.js"]
```

**Verification**:
```bash
ls /mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend/auth-service/Dockerfile
# File should exist
```

---

### [T1.7] [P] Create docker-compose.yml

**Story**: M1.1
**Description**:
Create `/mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend/auth-service/docker-compose.yml`:
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: auth_dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  auth-service:
    build: .
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/auth_dev
      JWT_SECRET: dev-secret
      NODE_ENV: development
      PORT: 3001
      CORS_ORIGINS: http://localhost:3000,http://localhost:5000
    ports:
      - "3001:3001"
    depends_on:
      postgres:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3001/api/health"]
      interval: 10s
      timeout: 5s
      retries: 3

volumes:
  postgres_data:
```

**Verification**:
```bash
ls /mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend/auth-service/docker-compose.yml
# File should exist
```

---

### [T1.8] Create Checkpoint 1 Summary

**Story**: M1.1
**Description**:
Verify all Phase 1 (Setup) tasks completed:
- [ ] Directories created
- [ ] package.json installs without errors
- [ ] tsconfig.json valid
- [ ] .env files created
- [ ] Dockerfile builds
- [ ] docker-compose.yml syntax valid

**Verification**:
```bash
cd /mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend/auth-service
npm install
npm run build
docker-compose config  # Validates YAML syntax
```

**Checkpoint Approval**: Required before proceeding to Phase 2

---

## Phase 2: Better-Auth Configuration

### [T2.1] Create src/utils/logger.ts

**Story**: M1.2, M1.3
**Description**:
Create `/mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend/auth-service/src/utils/logger.ts`:

Implement structured JSON logging using winston:
```typescript
// Conceptual structure (NOT production code)
import winston from 'winston';

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.Console(),
    // Optionally: new winston.transports.File({ filename: 'error.log', level: 'error' })
  ],
});

export default logger;
```

**Verification**:
```bash
cd /mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend/auth-service
npm run build
# Should compile without errors
ls dist/utils/logger.js  # Should exist
```

---

### [T2.2] Create src/auth.ts

**Story**: M1.2, US1, US2, US3, US4
**Description**:
Create `/mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend/auth-service/src/auth.ts`:

Initialize better-auth with:
- Postgres database adapter (connection to Neon via DATABASE_URL)
- Email/password plugin (signup/login)
- JWT plugin (RS256, 24h expiration)
- Session configuration (24h expiry)
- Password validation (min 8 chars, complexity rules)
- Rate limiting setup (5 login per 15min, 3 signup per hour)

Key points:
- Use `betterAuth()` factory function
- Pass postgres connection string from DATABASE_URL
- Configure JWT algorithm and expiration
- Set password rules

**Verification**:
```bash
cd /mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend/auth-service
npm run build
# Should compile without errors
```

---

### [T2.3] Create src/middleware/errorHandler.ts

**Story**: M1.3
**Description**:
Create `/mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend/auth-service/src/middleware/errorHandler.ts`:

Implement Express error handling middleware:
```typescript
// Conceptual structure
export function errorHandler(err, req, res, next) {
  // Log error
  logger.error({
    message: err.message,
    stack: err.stack,
    endpoint: req.path,
    method: req.method
  });

  // Return user-friendly error (no stack traces, no email enumeration)
  if (err.code === 'EMAIL_EXISTS') {
    return res.status(400).json({ error: 'Email already registered' });
  }

  if (err.code === 'INVALID_CREDENTIALS') {
    return res.status(401).json({ error: 'Invalid email or password' });
  }

  // Generic error
  res.status(err.status || 500).json({
    error: process.env.NODE_ENV === 'production'
      ? 'Internal server error'
      : err.message
  });
}
```

**Verification**:
```bash
cd /mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend/auth-service
npm run build
ls dist/middleware/errorHandler.js
```

---

### [T2.4] Create src/routes/auth.ts

**Story**: M1.3, US1, US2, US3
**Description**:
Create `/mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend/auth-service/src/routes/auth.ts`:

Implement authentication routes:
- `POST /api/auth/sign-up` - Call better-auth signup
- `POST /api/auth/sign-in` - Call better-auth login
- `POST /api/auth/sign-out` - Call better-auth logout
- `GET /api/auth/session` - Get current session
- `POST /api/auth/refresh` - Refresh token
- `GET /.well-known/jwks.json` - Public JWT keys (for FastAPI validation in Iteration 2)

All endpoints should:
- Validate input (email format, password not empty)
- Call better-auth SDK methods
- Return proper JSON responses
- Handle errors via error middleware

**Verification**:
```bash
cd /mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend/auth-service
npm run build
# Should compile without errors
```

---

### [T2.5] Create src/routes/health.ts

**Story**: M1.3, US5
**Description**:
Create `/mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend/auth-service/src/routes/health.ts`:

Implement health check route:
```typescript
// Conceptual structure
export async function healthCheck(req, res) {
  try {
    // Check Postgres connection
    const result = await db.query('SELECT 1');

    res.status(200).json({
      status: 'healthy',
      database: 'connected',
      timestamp: new Date().toISOString()
    });
  } catch (err) {
    logger.error({ message: 'Health check failed', error: err });

    res.status(503).json({
      status: 'unhealthy',
      database: 'disconnected',
      error: 'Failed to connect to Postgres',
      timestamp: new Date().toISOString()
    });
  }
}
```

**Verification**:
```bash
cd /mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend/auth-service
npm run build
ls dist/routes/health.js
```

---

### [T2.6] Create src/server.ts

**Story**: M1.3
**Description**:
Create `/mnt/c/Users/않는SSAD/Desktop/code/hackathon_01/backend/auth-service/src/server.ts`:

Implement Express server:
```typescript
// Conceptual structure
import express from 'express';
import cors from 'cors';
import rateLimit from 'express-rate-limit';
import { auth } from './auth';
import authRoutes from './routes/auth';
import { healthCheck } from './routes/health';
import { errorHandler } from './middleware/errorHandler';

const app = express();

// Middleware
app.use(express.json());
app.use(cors({
  origin: process.env.CORS_ORIGINS?.split(','),
  credentials: true
}));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5 // 5 requests per IP per window
});
app.use('/api/auth/sign-in', limiter);

// Routes
app.use('/api/auth', authRoutes);
app.get('/api/health', healthCheck);

// Mount better-auth handler
app.all('/api/auth/*', toNodeHandler(auth));

// Error handling
app.use(errorHandler);

// Start server
const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  logger.info(`Auth service running on port ${PORT}`);
});
```

**Verification**:
```bash
cd /mnt/c/Users/ASSAD/Desktop/code/hackathon_01/backend/auth-service
npm run build
npm run start  # Should start without errors
curl http://localhost:3001/api/health  # Should return status
```

---

### [T2.7] Create Checkpoint 2 Summary

**Story**: M1.2
**Description**:
Verify all Phase 2 (Better-Auth Config) tasks completed:
- [ ] Logger utility working
- [ ] Better-auth initialized (auth.ts compiles)
- [ ] Error handler middleware functional
- [ ] Auth routes created
- [ ] Health check endpoint operational
- [ ] Server starts on port 3001

**Verification**:
```bash
cd /mnt/c/Users/ASSAД/Desktop/code/hackathon_01/backend/auth-service
npm run build
npm run start &
sleep 2
curl http://localhost:3001/api/health
# Should return: {"status": "healthy", "database": "connected"}
kill %1
```

**Checkpoint Approval**: Required before proceeding to Phase 3

---

## Phase 3: Database & Alembic Migrations

### [T3.1] Create Alembic migrations directory

**Story**: US4
**Description**:
Create `/mnt/c/Users/ASSAД/Desktop/code/hackathon_01/backend/alembic/` directory structure if not already present.

**Verification**:
```bash
ls -la /mnt/c/Users/ASSYAD/Desktop/code/hackathon_01/backend/alembic/
# Should show: versions/ subdirectory
```

---

### [T3.2] Create migration: 001_create_auth_tables.py

**Story**: US4
**Description**:
Create `/mnt/c/Users/ASSAد/Desktop/code/hackathon_01/backend/alembic/versions/001_create_auth_tables.py`:

Create better-auth database schema (users, accounts, sessions, verification tables):
```python
# Conceptual structure (NOT production code)
def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('email', sa.VARCHAR(255), unique=True, nullable=False),
        sa.Column('name', sa.VARCHAR(255), nullable=False),
        sa.Column('email_verified', sa.Boolean(), default=False),
        sa.Column('image', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False)
    )
    # ...create other tables...

def downgrade():
    op.drop_table('users')
    # ...drop other tables...
```

**Verification**:
```bash
cd /mnt/c/Users/ASSAД/Desktop/code/hackathon_01/backend
alembic upgrade head
# Should apply migration without errors
psql -d auth_db -c "\dt"  # List tables
# Should show: users, accounts, sessions, verification
```

---

### [T3.3] Create Checkpoint 3 Summary

**Story**: US4
**Description**:
Verify all Phase 3 (Migrations) tasks completed:
- [ ] Alembic migration created
- [ ] Migration applies successfully (alembic upgrade head)
- [ ] All auth tables exist in Postgres
- [ ] Schema matches better-auth specification

**Verification**:
```bash
cd /mnt/c/Users/ASSAД/Desktop/code/hackathon_01/backend
alembic upgrade head
psql -d auth_db -c "SELECT count(*) FROM users;"
# Should return: 0 (empty table, no error)
```

**Checkpoint Approval**: Required before proceeding to Phase 4

---

## Phase 4: Testing & Validation

### [T4.1] Create Playwright test file

**Story**: All 5 US + 13 test cases
**Description**:
Create `/mnt/c/Users/ASSAД/Desktop/code/hackathon_01/backend/auth-service/tests/auth.spec.ts`:

Implement 13 API tests covering all acceptance scenarios:
- T001: Signup with valid data (US1.AC1)
- T002: Signup with existing email (US1.AC2)
- T003: Signup with weak password (US1.AC3)
- T004: Login with correct credentials (US2.AC1)
- T005: Login with incorrect password (US2.AC2)
- T006: Login with non-existent email (US2.AC3)
- T007: Refresh token (US3.AC2)
- T008: Logout invalidates token (US3.AC3)
- T009: Database schema exists (US4.AC1)
- T010: Unique constraint on email (US4.AC2)
- T011: Cascading delete (US4.AC3)
- T012: Health check when healthy (US5.AC1)
- T013: Health check when DB down (US5.AC2)

**Verification**:
```bash
cd /mnt/c/Users/ASSAД/Desktop/code/hackathon_01/backend/auth-service
npm run test
# Should pass 13/13 tests
```

---

### [T4.2] Run all tests and verify passing

**Story**: All US
**Description**:
Execute test suite to verify all acceptance criteria met:
```bash
cd /mnt/c/Users/ASSAД/Desktop/code/hackathon_01/backend/auth-service
npm run test -- --reporter=json > test-results.json
```

Requirements:
- 100% of 13 tests pass
- Zero errors in console
- All acceptance scenarios verified

**Verification**:
```bash
cd /mnt/c/Users/ASSAД/Desktop/code/hackathon_01/backend/auth-service
npm run test
# Output should show: 13 passed, 0 failed
```

---

### [T4.3] Verify no sensitive data in logs

**Story**: NFR-010
**Description**:
Check logs do not contain:
- Passwords
- Email addresses (in error paths)
- JWT tokens
- Database connection strings

Manual verification:
```bash
cd /mnt/c/Users/ASSAД/Desktop/code/hackathon_01/backend/auth-service
npm run dev &
# Make signup request
curl -X POST http://localhost:3001/api/auth/sign-up \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!","name":"Test"}'
# Check logs - should NOT show password or email
kill %1
```

---

### [T4.4] Verify database schema via psql

**Story**: US4
**Description**:
Connect to Postgres and verify tables exist:
```bash
psql postgresql://user:password@localhost:5432/auth_dev

# Run queries:
\dt  -- List all tables
SELECT * FROM users;  -- Should be empty
SELECT column_name, data_type FROM information_schema.columns WHERE table_name='users';
```

Verify columns exist for:
- users: id (UUID), email (VARCHAR), name (VARCHAR), emailVerified (BOOLEAN), createdAt, updatedAt
- accounts: id, userId, providerId, accountId, passwordHash
- sessions: id, userId, token, expiresAt, createdAt

**Verification**:
```bash
psql postgresql://user:password@localhost:5432/auth_dev -c "\dt"
# Should show: accounts, sessions, users, verification tables
```

---

### [T4.5] Create Checkpoint 4 Summary

**Story**: All
**Description**:
Final verification before signing off Iteration 1:
- [ ] All 13 Playwright tests pass
- [ ] No sensitive data in logs
- [ ] Database schema complete and correct
- [ ] Health check works (200 OK when healthy, 503 when DB down)
- [ ] All 5 user stories acceptance scenarios validated
- [ ] Rate limiting confirmed working
- [ ] Server runs without errors
- [ ] Environment variables properly configured

**Verification Checklist**:
```bash
# 1. Run tests
cd /mnt/c/Users/ASSAД/Desktop/code/hackathon_01/backend/auth-service
npm run test
# Expected: 13 passed

# 2. Start server
npm run start &
sleep 2

# 3. Test health check
curl http://localhost:3001/api/health
# Expected: 200 OK with status=healthy

# 4. Test signup
curl -X POST http://localhost:3001/api/auth/sign-up \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"Alice123!","name":"Alice"}'
# Expected: 200 OK with JWT token

# 5. Test login
curl -X POST http://localhost:3001/api/auth/sign-in \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"Alice123!"}'
# Expected: 200 OK with JWT token

# 6. Stop server
kill %1
```

**Checkpoint Approval**: Required before moving to Iteration 2

---

## Summary

| Phase | Tasks | Status |
|-------|-------|--------|
| Phase 1: Setup | T1.1-T1.8 | Ready |
| Phase 2: Config | T2.1-T2.7 | Ready |
| Phase 3: Migrations | T3.1-T3.3 | Ready |
| Phase 4: Testing | T4.1-T4.5 | Ready |

**Total Tasks**: 20
**Critical Checkpoints**: 4
**Manual Testing Required**: Yes (final checkpoint)
