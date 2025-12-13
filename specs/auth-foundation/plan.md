# Implementation Plan: Auth Foundation (Iteration 1)

**Spec**: `specs/auth-foundation/spec.md`
**Phase**: 2 (Auth Foundation)
**Duration**: 1-2 sprints (human-paced spec-driven work)
**Status**: Ready for Implementation

---

## Executive Summary

Establish authentication infrastructure using better-auth. Users can sign up with email/password and log in. Better-auth service (Node.js) manages credentials and issues JWT tokens, while Neon Postgres stores user data and sessions. No frontend UI in this iteration—all testing is API-based.

---

## Technical Context

### Technology Stack

| Layer | Technology | Details |
|-------|-----------|---------|
| **Runtime** | Node.js 20+ | Better-auth requirement |
| **Framework** | Express.js 4.18+ | Minimal HTTP server |
| **Auth** | better-auth (latest) | Battle-tested, OAuth-ready |
| **Database** | Neon Postgres 15+ | Shared with FastAPI backend |
| **ORM** | Drizzle ORM (via better-auth) | Better-auth default adapter |
| **Testing** | Node.js HTTP tests + Playwright | API testing (no browser needed) |
| **Environment** | Docker Compose | Local dev orchestration |

### Constraints

- **Single Service**: Better-auth runs standalone (not in FastAPI)
- **Shared Database**: Uses same Neon Postgres as backend
- **No UI**: All interaction via REST API
- **JWT-Based**: Tokens used for session management (not cookies in Iteration 1)
- **Password Security**: Scrypt hashing (better-auth default)
- **No Email Verification**: Keep simple for Iteration 1

### Non-Functional Targets

- **Signup Latency**: <500ms p95 (password hashing cost)
- **Login Latency**: <300ms p95
- **Uptime**: 99.5% SLA
- **Rate Limiting**: 3 signup/hour/IP, 5 login/15min/IP
- **Security**: No email enumeration, HTTPS only (prod)

---

## Project Structure

### Directory Layout

```
/backend/
├── auth-service/                    # NEW: Better-auth Node.js service
│   ├── src/
│   │   ├── auth.ts                  # Better-auth config
│   │   ├── server.ts                # Express server setup
│   │   ├── middleware/
│   │   │   └── errorHandler.ts      # Error handling middleware
│   │   ├── routes/
│   │   │   ├── auth.ts              # Auth endpoints (sign-up, sign-in, etc.)
│   │   │   └── health.ts            # Health check endpoint
│   │   └── utils/
│   │       └── logger.ts            # Structured logging
│   ├── .env                         # Environment variables
│   ├── .env.example                 # Environment template
│   ├── .gitignore                   # Don't commit node_modules, .env
│   ├── package.json                 # Dependencies
│   ├── tsconfig.json                # TypeScript configuration
│   ├── Dockerfile                   # Docker build
│   └── docker-compose.yml           # Local dev orchestration
│
└── (existing FastAPI files unchanged in Iteration 1)
```

---

## Module Breakdown

### Module 1: Better-Auth Configuration (`src/auth.ts`)

**Purpose**: Initialize better-auth with Postgres adapter, JWT plugin, password rules

**Components**:
- Postgres database adapter (connection pooling)
- Email/password plugin (signup/login)
- JWT plugin (token generation, RS256 signing)
- Session configuration (24h expiry)
- Password validation rules (min 8 chars, complexity)
- Rate limiting setup

**Data Flow**:
```
User signup → Better-auth → Validate email/password → Hash password → Store in DB → Issue JWT
```

**Dependencies**:
- `better-auth` npm package
- `pg` driver for Postgres
- Environment variables (DATABASE_URL, JWT_SECRET)

**Key Configuration**:
```typescript
// Conceptual (NOT production code)
const auth = betterAuth({
  database: postgresAdapter({
    connectionString: process.env.DATABASE_URL,
  }),
  emailAndPassword: {
    enabled: true,
    minPasswordLength: 8,
    maxPasswordLength: 128,
  },
  session: {
    expiresIn: 86400, // 24 hours
  },
  plugins: [
    jwtPlugin({
      algorithm: "RS256",
      expiresIn: "15m", // Access token
    })
  ]
});
```

---

### Module 2: Express Server (`src/server.ts`)

**Purpose**: HTTP server setup, CORS, middleware, request routing

**Components**:
- Express app initialization
- CORS middleware (allow localhost:3000, localhost:5000)
- JSON body parser
- Error handling middleware
- Route mounting (/api/auth/*, /api/health)
- Server startup on port 3001

**Data Flow**:
```
HTTP Request → CORS check → Body parsing → Route handler → Response
```

**Dependencies**:
- `express` npm package
- Custom middleware (`errorHandler.ts`)

---

### Module 3: Auth Routes (`src/routes/auth.ts`)

**Purpose**: Handle authentication endpoints using better-auth

**Endpoints** (all in better-auth):
- `POST /api/auth/sign-up` - Create account
- `POST /api/auth/sign-in` - Login
- `POST /api/auth/sign-out` - Logout
- `POST /api/auth/refresh` - Refresh token
- `GET /api/auth/session` - Get session

**Key Logic**:
- Input validation (email format, password strength)
- Error handling (duplicate email, weak password)
- Rate limiting (express-rate-limit)
- Response formatting (consistent JSON)

**Dependencies**:
- `better-auth` SDK
- `express` routing
- `express-rate-limit` for throttling

---

### Module 4: Health Check Routes (`src/routes/health.ts`)

**Purpose**: Service health monitoring

**Endpoint**:
- `GET /api/health` - Returns status (healthy/unhealthy) + DB connection status

**Key Logic**:
- Check Postgres connectivity
- Return appropriate status code (200 = healthy, 503 = unhealthy)
- Include timestamp

**Dependencies**:
- Postgres connection pool

---

### Module 5: Error Handling Middleware (`src/middleware/errorHandler.ts`)

**Purpose**: Centralized error handling, logging, response formatting

**Key Logic**:
- Catch unexpected errors
- Log to structured logging system
- Return user-friendly error responses (no stack traces in production)
- No email enumeration (same error for invalid email/password)

**Dependencies**:
- Logger utility

---

### Module 6: Logging Utility (`src/utils/logger.ts`)

**Purpose**: Structured JSON logging for debugging and monitoring

**Key Logic**:
- Winston or Pino logger
- Timestamp, level, message, context fields
- Different levels: info, warn, error, debug

**Log Events**:
- Auth service startup
- Database connection success/failure
- Signup attempts (success/failure)
- Login attempts (success/failure, rate limiting)
- Errors and exceptions

---

## Milestones

### M1.1: Project Setup & Configuration
**Deliverables**:
- [ ] Create `/backend/auth-service/` directory structure
- [ ] `package.json` with all dependencies
- [ ] `tsconfig.json` configured
- [ ] `.env` and `.env.example` with required variables
- [ ] `Dockerfile` for containerization
- [ ] `docker-compose.yml` with postgres + auth-service

**Exit Criteria**:
- `npm install` completes without errors
- `npm run build` compiles TypeScript
- Docker image builds successfully

---

### M1.2: Better-Auth Configuration
**Deliverables**:
- [ ] `src/auth.ts` with better-auth initialization
- [ ] Postgres adapter connected to Neon
- [ ] JWT plugin configured (RS256, 24h expiry)
- [ ] Email/password plugin enabled
- [ ] Password validation rules (min 8, complexity)
- [ ] Session configuration

**Exit Criteria**:
- Database migration runs automatically on startup
- Auth tables created in Postgres (verify with `\dt` in psql)
- JWT keys generated and stored

---

### M1.3: Express Server & Routes
**Deliverables**:
- [ ] `src/server.ts` - Express app setup, CORS, middleware
- [ ] `src/routes/auth.ts` - Auth endpoints mounted
- [ ] `src/routes/health.ts` - Health check endpoint
- [ ] `src/middleware/errorHandler.ts` - Error handling
- [ ] `src/utils/logger.ts` - Structured logging

**Exit Criteria**:
- Server starts without errors (`npm run dev`)
- All endpoints respond to requests
- Error handling returns proper status codes

---

### M1.4: Testing & Validation
**Deliverables**:
- [ ] Playwright API tests for all 5 user stories
- [ ] 13 test cases from spec (T001-T013)
- [ ] Rate limiting validation
- [ ] Database schema verification
- [ ] Health check tests

**Exit Criteria**:
- All tests pass (`npm run test`)
- 100% of acceptance criteria met
- No sensitive data in logs

---

## Dependency Graph

```
┌─────────────────────────────────────┐
│ M1.1: Project Setup                 │
│ (package.json, Dockerfile)          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ M1.2: Better-Auth Configuration     │
│ (src/auth.ts, DB migration)         │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ M1.3: Express Server & Routes       │
│ (src/server.ts, src/routes/*)       │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ M1.4: Testing & Validation          │
│ (Playwright tests, verification)    │
└─────────────────────────────────────┘
```

---

## Human Review Checkpoints

### Checkpoint 1: After M1.1 (Project Setup)
**What to Verify**:
- Docker Compose starts all services without errors
- Database credentials work (can connect to Postgres)
- Node.js dependencies installed

**Approval Required**: Before proceeding to M1.2

---

### Checkpoint 2: After M1.2 (Better-Auth Config)
**What to Verify**:
- Better-auth initializes without errors
- Database tables exist (users, accounts, sessions, verification)
- JWT keys generated correctly
- Password validation works (try invalid inputs)

**Approval Required**: Before proceeding to M1.3

---

### Checkpoint 3: After M1.3 (Express Server)
**What to Verify**:
- Server starts on port 3001
- All endpoints respond (curl tests)
- CORS headers present
- Error responses properly formatted

**Approval Required**: Before proceeding to M1.4

---

### Checkpoint 4: After M1.4 (Testing)
**What to Verify**:
- All Playwright tests pass
- No errors in logs
- Rate limiting working
- Database schema correct
- Health check responds

**Approval Required**: Sign-off before moving to Iteration 2

---

## Risk Analysis

| Risk | Severity | Probability | Mitigation |
|------|----------|-------------|-----------|
| Neon Postgres connection issues | HIGH | MEDIUM | Use connection pooling, test connection before starting server |
| Better-auth schema mismatch | MEDIUM | LOW | Follow better-auth docs exactly, test on staging first |
| Password hashing too slow | MEDIUM | LOW | Use better-auth defaults, monitor latency in tests |
| Email enumeration vulnerability | HIGH | MEDIUM | Implement generic error messages, validate in tests |
| Rate limiting bypass | MEDIUM | MEDIUM | Use express-rate-limit, test with concurrent requests |
| JWT secret exposure | CRITICAL | LOW | Keep in .env, never in code, rotate regularly |

---

## Open Decisions (Require ADR)

### OD-1: JWT Algorithm (RS256 vs HS256)
**Decision**: Use RS256 (RSA with SHA-256)

**Rationale**:
- RS256 is asymmetric (public key validation in FastAPI, no secret needed)
- HS256 would require sharing secret between services (security risk)
- RS256 standard for OAuth/OpenID Connect

**Status**: ✅ Decided (documented in plan)

---

### OD-2: Token Expiration (24h vs Shorter)
**Decision**: 24-hour expiration for access tokens

**Rationale**:
- Longer expiry = fewer refresh requests (better performance)
- Shorter expiry = faster logout (security)
- 24h is reasonable compromise for textbook use case

**Status**: ✅ Decided (documented in plan)

---

### OD-3: Database Schema Customization
**Decision**: Use better-auth default schema (no customization)

**Rationale**:
- Simpler to maintain (follow upstream changes)
- User profile data in separate table (Iteration 4)
- Less chance of schema bugs

**Status**: ✅ Decided (documented in plan)

---

## Constitution Compliance

✅ **Principle I (Spec-Driven)**: This plan originates from approved spec
✅ **Principle II (No Vibe Coding)**: Plan provides architecture only, no code generation
✅ **Principle VII (Testability)**: All user stories have independent tests

**Compliance Status**: PASS

---

## Complexity Tracking

### Token Budget

| Component | Complexity | Notes |
|-----------|-----------|-------|
| Better-auth config | Low | Framework handles 90% |
| Express server | Low | Standard middleware setup |
| Error handling | Medium | Need to prevent email enumeration |
| Rate limiting | Low | Library does most work |
| Testing | Medium | Need proper API test setup |
| **Total** | **Low-Medium** | Standard backend auth work |

### Constitution Violations

None. This iteration follows:
- Spec-driven workflow (specification exists)
- No vibe coding (architecture planning only)
- Testable requirements (all scenarios have acceptance criteria)

---

## Performance & Scalability

### Performance Targets

| Operation | Target | Notes |
|-----------|--------|-------|
| Signup | <500ms p95 | Password hashing cost |
| Login | <300ms p95 | Lookup + verification |
| Refresh | <100ms p95 | Simple lookup + new token |
| Health check | <50ms | DB connection test |

### Scalability

- **Single Instance**: Handles 100 concurrent users (password hashing is bottleneck)
- **Horizontal Scaling**: Future: add nginx reverse proxy, share session store (Redis)
- **Database**: Connection pooling handles 20 connections from auth service

---

## Output Validation

### Code Quality

- TypeScript strict mode enabled
- No console.log (use logger utility)
- Error types properly thrown
- No hardcoded secrets

### Testing

- All 13 Playwright tests pass
- Acceptance criteria verified for all 5 user stories
- Edge cases validated (EC1-EC5)

### Deployment Readiness

- Docker image builds
- Environment variables documented
- Health check operational
- Logs in structured JSON

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Test Pass Rate | 100% | Run `npm run test` |
| Signup Success Rate | >99% | Monitor in logs |
| API Response Time (p95) | <500ms | Load testing |
| Error Messages | 0 emails leaked | Manual testing |
| Uptime | 99.5% | 24h continuous run |
| Schema Coverage | 100% | `SELECT * FROM users` after signup |

---

## Next Steps (Preview of Iteration 2)

After M1.4 approval:
1. Create spec for `auth-fastapi-integration` (JWT validation in FastAPI)
2. Implement FastAPI middleware for JWT validation
3. Create profile service and database models
4. Test token validation with tokens from auth-service

---

## References

- Better Auth Docs: https://www.better-auth.com/docs
- Express.js: https://expressjs.com
- Playwright API Testing: https://playwright.dev/docs/api/class-apirequestcontext
