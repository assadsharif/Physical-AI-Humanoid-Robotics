# Feature Specification: Auth Foundation (Iteration 1)

**Feature**: Authentication Infrastructure with Better-Auth
**Feature Branch**: `feature/auth-foundation`
**Created**: 2025-12-13
**Status**: In Development
**Phase**: 2 (Auth Foundation)
**Iteration**: 1 of 7
**Input**: User requirement: "Implement signup and signin using better-auth. Collect user background (software experience) at signup."

---

## Problem Statement

The Physical AI & Humanoid Robotics textbook currently has no user authentication. All users are anonymous, which prevents:
1. Personalization based on user background
2. Conversation history persistence
3. Tracking user progress through content
4. Delivering customized learning experiences

**Iteration 1 Focus**: Establish the authentication foundation using better-auth, enabling users to create accounts and log in via email/password. This iteration sets up the infrastructure for future personalization features.

---

## Goals

1. **Email/Password Registration**: Users can create accounts with email and password
2. **User Login**: Users can authenticate with email/password credentials
3. **Session Management**: Secure session tokens (JWT) issued and validated
4. **Database Setup**: Better-auth schema created in Neon Postgres
5. **Service Architecture**: Better-auth runs as separate Node.js service alongside FastAPI
6. **Health Monitoring**: Auth service health checks operational

---

## Non-Goals (Iteration 1)

- OAuth/social login (Phase 2 extension)
- Email verification (Phase 2 extension)
- Password reset flows (Phase 2 extension)
- User profile data collection (Iteration 4)
- Frontend UI (Iteration 3)
- JWT validation in FastAPI (Iteration 2)
- Personalization logic (Iteration 5+)

---

## Inputs

- **User Requirements**:
  - Email/password authentication only (no OAuth for now)
  - Use better-auth framework
  - Integrate with existing Neon Postgres database
  - Separate Node.js service (not integrated into FastAPI)

- **Technical Context**:
  - Backend: FastAPI (Python) running on port 8000
  - Auth Service: Node.js/Express (new) running on port 3001
  - Database: Neon Postgres (existing connection string in backend/.env)
  - Development Environment: Docker Compose for local orchestration

---

## Outputs

- **Better-Auth Service**: Node.js Express server handling authentication
- **Database Schema**: Auth tables (users, accounts, sessions) in Neon Postgres
- **Environment Setup**: .env configuration for auth service
- **API Endpoints**: Email/password signup, login, logout, token refresh
- **Health Checks**: Service availability monitoring
- **Docker Configuration**: docker-compose.yml for local development
- **Documentation**: Setup guide and API reference

---

## Dependencies

### Technology Stack

| Component | Technology | Version | Rationale |
|-----------|-----------|---------|-----------|
| **Runtime** | Node.js | 20+ | Standard for better-auth |
| **Web Framework** | Express.js | 4.18+ | Lightweight server for better-auth |
| **Auth Framework** | better-auth | Latest | User requirement, battle-tested |
| **Database Driver** | pg (node-postgres) | 8.8+ | Better-auth Postgres adapter support |
| **Database** | Neon Postgres | 15+ | Serverless, existing in project |
| **Environment** | dotenv | 16+ | Config management |
| **Logging** | winston or pino | Latest | Structured logging |

### External Services

- **Neon Postgres**: Serverless database (existing)
- **Better-Auth**: Hosted service (none, self-hosted via Express)

### File Dependencies

- `/backend/.env` - Database connection string (DATABASE_URL)
- `/backend/.env.example` - Environment template (will extend)
- `/backend/requirements.txt` - Python dependencies (unchanged in Iteration 1)

---

## User Scenarios & Testing *(mandatory)*

### User Story 1: Email/Password Signup (Priority: P1)

**Why P1**: Core authentication flow. Without signup, no users can be created.

**Scenario**:
A new user visits the platform and wants to create an account using email and password.

**Independent Test**:
- Can POST to `/api/auth/sign-up` with valid email/password
- Response includes JWT token and user object
- User record created in Postgres
- All required fields populated

**Acceptance Scenarios**:

1. **Given** a user with valid email (user@example.com) and strong password (Min8Char!)
   **When** they POST to `/api/auth/sign-up` with email, password, name
   **Then** they receive 200 OK response with JWT token and user object
   **And** user record exists in `users` table

2. **Given** a user attempting signup with existing email
   **When** they POST to `/api/auth/sign-up`
   **Then** they receive 400 Bad Request with "Email already registered"

3. **Given** a user attempting signup with weak password (less than 8 chars)
   **When** they POST to `/api/auth/sign-up`
   **Then** they receive 400 Bad Request with password strength error

---

### User Story 2: Email/Password Login (Priority: P1)

**Why P1**: Core authentication flow. Without login, users cannot access their accounts.

**Scenario**:
An existing user wants to log in with their email and password.

**Independent Test**:
- Can POST to `/api/auth/sign-in` with valid email/password
- Response includes JWT token and user object
- Session created in database
- Token valid for subsequent authenticated requests

**Acceptance Scenarios**:

1. **Given** an existing user with correct email and password
   **When** they POST to `/api/auth/sign-in` with credentials
   **Then** they receive 200 OK with JWT token and user object
   **And** session record created in `sessions` table

2. **Given** a user with incorrect password
   **When** they POST to `/api/auth/sign-in`
   **Then** they receive 401 Unauthorized with "Invalid credentials"

3. **Given** a user with non-existent email
   **When** they POST to `/api/auth/sign-in`
   **Then** they receive 401 Unauthorized (no email enumeration)

---

### User Story 3: Session/Token Management (Priority: P1)

**Why P1**: Authentication is useless without secure session handling. Users must receive valid tokens and be able to refresh them.

**Scenario**:
A logged-in user's session expires and they need to refresh their token.

**Independent Test**:
- Token expires after configured time (24h default)
- User can refresh token with refresh token
- Old token invalidated, new token issued
- Session records stored securely

**Acceptance Scenarios**:

1. **Given** a valid JWT token with 24h expiration
   **When** 25 hours have passed
   **Then** token is no longer valid for API requests

2. **Given** a valid refresh token (from login)
   **When** user POSTs to `/api/auth/refresh` with refresh token
   **Then** they receive new JWT and new refresh token

3. **Given** a user POSTs to `/api/auth/sign-out` with valid token
   **When** they attempt to use old token
   **Then** it returns 401 Unauthorized

---

### User Story 4: Database Schema Creation (Priority: P1)

**Why P1**: Authentication is impossible without database tables. Better-auth schema must be properly created.

**Scenario**:
During service startup, better-auth initializes the database schema.

**Independent Test**:
- All required better-auth tables exist in Postgres
- Schema matches better-auth specifications
- Foreign key constraints enforced
- Indexes created for performance

**Acceptance Scenarios**:

1. **Given** fresh Postgres database
   **When** better-auth service starts
   **Then** the following tables exist: users, accounts, sessions, verification

2. **Given** the users table exists
   **When** attempting to insert two users with same email
   **Then** unique constraint violation (email is UNIQUE)

3. **Given** the sessions table exists
   **When** a user is deleted from users table
   **Then** related sessions are deleted (CASCADE FK constraint)

---

### User Story 5: Service Health & Monitoring (Priority: P2)

**Why P2**: Operations need to know if auth service is healthy. Enables graceful degradation if service down.

**Scenario**:
A monitoring system needs to check if the auth service is operational.

**Independent Test**:
- Can GET `/api/health` endpoint
- Returns JSON with service status
- Includes database connectivity info
- Proper HTTP status codes (200 = healthy, 503 = unhealthy)

**Acceptance Scenarios**:

1. **Given** a healthy auth service with database connection
   **When** they GET `/api/health`
   **Then** they receive 200 OK with `{"status": "healthy", "database": "connected"}`

2. **Given** auth service cannot connect to database
   **When** they GET `/api/health`
   **Then** they receive 503 Service Unavailable with `{"status": "unhealthy", "database": "disconnected"}`

---

## Edge Cases

### EC1: Rate Limiting on Signup
- **Scenario**: Attacker attempts rapid account creation
- **Expected**: After 3 signup attempts per hour per IP, return 429 Too Many Requests
- **Validation**: Implement express-rate-limit on signup endpoint

### EC2: Very Long Email/Password
- **Scenario**: User provides 10KB email address or password
- **Expected**: Request validation rejects, returns 400 Bad Request
- **Validation**: Set max length limits (email: 255 chars, password: 128 chars)

### EC3: SQL Injection via Email
- **Scenario**: User provides email like `user@example.com'; DROP TABLE users; --`
- **Expected**: Better-auth parameterized queries prevent injection
- **Validation**: Attempt injection, verify data integrity

### EC4: Concurrent Signup Attempts
- **Scenario**: Two requests arrive simultaneously for same email
- **Expected**: One succeeds, other fails with "Email already registered"
- **Validation**: Database unique constraint enforces atomicity

### EC5: Database Connection Loss
- **Scenario**: Postgres connection drops mid-request
- **Expected**: Service returns 503 error, not 500, and reconnects
- **Validation**: Check error handling and connection pooling

---

## Requirements

### Functional Requirements

| ID | Requirement | Acceptance Criteria |
|----|-------------|-------------------|
| FR-001 | Email/Password Signup | User can create account, JWT token returned, password securely hashed |
| FR-002 | Email/Password Login | User can authenticate, valid JWT returned, session persisted |
| FR-003 | Token Refresh | User can refresh expired token using refresh token, new session created |
| FR-004 | Logout | User can invalidate session, token no longer valid |
| FR-005 | Database Schema | All better-auth tables created automatically on startup |
| FR-006 | Password Hashing | Passwords hashed with scrypt (OWASP approved, memory-hard) |
| FR-007 | Session Tracking | Sessions tracked in database with expiry, IP, user agent |
| FR-008 | Health Checks | Service exposes /api/health endpoint with DB status |
| FR-009 | Rate Limiting | 5 signup attempts per hour per IP, 5 login attempts per 15min per IP |
| FR-010 | Input Validation | Email format validation, password complexity rules enforced |

### Non-Functional Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-001 | Signup Latency | <500ms p95 (includes password hashing) |
| NFR-002 | Login Latency | <300ms p95 (password verification) |
| NFR-003 | Service Uptime | 99.5% SLA (max 3.6h downtime/month) |
| NFR-004 | Database Connections | Connection pooling, max 20 connections per auth service |
| NFR-005 | Password Security | Min 8 chars, scrypt hashing, random salt per password |
| NFR-006 | Token Security | RS256 (RSA) signature, 24h expiration (configurable) |
| NFR-007 | HTTPS Required | TLS 1.2+ in production, HTTP redirects to HTTPS |
| NFR-008 | CORS Enabled | Allow requests from localhost:3000 (frontend), configured per environment |
| NFR-009 | Error Messages | No email enumeration (same error for non-existent email + wrong password) |
| NFR-010 | Logging | Structured JSON logs for all auth events (signup, login, errors) |

### Key Entities

**User**
```typescript
{
  id: UUID,
  email: string,       // Unique, lowercase
  name: string,
  emailVerified: boolean,  // False initially (can add email verification later)
  image: string | null,
  createdAt: Date,
  updatedAt: Date
}
```

**Account**
```typescript
{
  id: UUID,
  userId: UUID,        // FK → User
  providerId: string,  // 'credential' for email/password
  accountId: string,   // Email address
  passwordHash: string, // Scrypt hash
  createdAt: Date,
  updatedAt: Date
}
```

**Session**
```typescript
{
  id: UUID,
  userId: UUID,        // FK → User
  token: string,       // JWT token
  expiresAt: Date,
  ipAddress: string | null,
  userAgent: string | null,
  createdAt: Date,
  updatedAt: Date
}
```

**Verification** (for future email verification)
```typescript
{
  id: UUID,
  identifier: string,  // Email
  value: string,       // Verification code
  expiresAt: Date,
  createdAt: Date
}
```

---

## Success Criteria

- [ ] SC-001: Better-auth service runs successfully on port 3001
- [ ] SC-002: POST /api/auth/sign-up creates user and returns JWT (US1 acceptance scenarios pass)
- [ ] SC-003: POST /api/auth/sign-in authenticates user and returns JWT (US2 acceptance scenarios pass)
- [ ] SC-004: POST /api/auth/refresh issues new token (US3 acceptance scenarios pass)
- [ ] SC-005: POST /api/auth/sign-out invalidates session (US3 acceptance scenarios pass)
- [ ] SC-006: All better-auth tables exist in Neon Postgres (US4 acceptance scenarios pass)
- [ ] SC-007: GET /api/health returns 200 with status (US5 acceptance scenarios pass)
- [ ] SC-008: Rate limiting prevents abuse (EC1 validated)
- [ ] SC-009: Input validation rejects invalid data (EC2, EC3 validated)
- [ ] SC-010: Concurrent signup requests handled atomically (EC4 validated)
- [ ] SC-011: Error handling for database issues (EC5 validated)
- [ ] SC-012: No sensitive info in error messages (email enumeration prevented)
- [ ] SC-013: Password validation enforced (min 8 chars, complexity)
- [ ] SC-014: JWT tokens valid and verifiable via JWKS endpoint
- [ ] SC-015: Environment variables properly configured (.env exists)

---

## API Contract Specifications

### POST /api/auth/sign-up

**Description**: Create new user account with email and password

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe"
}
```

**Response (200 Created)**:
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe",
    "emailVerified": false,
    "image": null,
    "createdAt": "2025-12-13T10:00:00Z",
    "updatedAt": "2025-12-13T10:00:00Z"
  },
  "token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refreshToken": "refresh-token-here"
}
```

**Error Responses**:
- **400 Bad Request**:
  ```json
  {
    "code": "INVALID_INPUT",
    "message": "Email already registered" | "Password too weak" | "Invalid email format"
  }
  ```
- **429 Too Many Requests**: After 3 attempts/hour/IP
- **500 Internal Server Error**: Database error

**Headers**:
```
Content-Type: application/json
```

---

### POST /api/auth/sign-in

**Description**: Authenticate user with email and password

**Request**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (200 OK)**:
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe",
    "emailVerified": false,
    "image": null,
    "createdAt": "2025-12-13T10:00:00Z",
    "updatedAt": "2025-12-13T10:00:00Z"
  },
  "token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refreshToken": "refresh-token-here"
}
```

**Error Responses**:
- **401 Unauthorized**: Invalid email or password (generic message, no enumeration)
- **429 Too Many Requests**: After 5 attempts per 15 minutes per IP
- **500 Internal Server Error**: Database error

---

### POST /api/auth/sign-out

**Description**: Invalidate user session

**Request Headers**:
```
Authorization: Bearer <jwt-token>
```

**Response (200 OK)**:
```json
{
  "success": true
}
```

**Error Responses**:
- **401 Unauthorized**: Invalid or missing token
- **500 Internal Server Error**: Database error

---

### POST /api/auth/refresh

**Description**: Refresh expired token using refresh token

**Request**:
```json
{
  "refreshToken": "refresh-token-here"
}
```

**Response (200 OK)**:
```json
{
  "token": "new-jwt-token",
  "refreshToken": "new-refresh-token"
}
```

**Error Responses**:
- **401 Unauthorized**: Invalid or expired refresh token
- **500 Internal Server Error**: Database error

---

### GET /api/auth/session

**Description**: Get current user session info

**Request Headers**:
```
Authorization: Bearer <jwt-token>
```

**Response (200 OK)**:
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe",
    "emailVerified": false,
    "image": null,
    "createdAt": "2025-12-13T10:00:00Z",
    "updatedAt": "2025-12-13T10:00:00Z"
  },
  "session": {
    "id": "session-uuid",
    "expiresAt": "2025-12-14T10:00:00Z",
    "createdAt": "2025-12-13T10:00:00Z"
  }
}
```

**Error Responses**:
- **401 Unauthorized**: Invalid token

---

### GET /.well-known/jwks.json

**Description**: Public keys for JWT validation (used by FastAPI in Iteration 2)

**Response (200 OK)**:
```json
{
  "keys": [
    {
      "kty": "RSA",
      "use": "sig",
      "kid": "key-id-1",
      "n": "modulus-value",
      "e": "exponent-value",
      "alg": "RS256"
    }
  ]
}
```

---

### GET /api/health

**Description**: Service health check

**Response (200 OK)**:
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-12-13T10:00:00Z"
}
```

**Response (503 Service Unavailable)**:
```json
{
  "status": "unhealthy",
  "database": "disconnected",
  "error": "Failed to connect to Postgres",
  "timestamp": "2025-12-13T10:00:00Z"
}
```

---

## Playwright Test-Spec Summary

Tests will verify acceptance criteria for all 5 user stories. Since this is backend-only (Iteration 1), tests use HTTP API calls (Playwright API testing, not browser automation).

| Test ID | Test Name | Endpoint | Acceptance Criteria Verified |
|---------|-----------|----------|------------------------------|
| T001 | Signup with valid data | POST /api/auth/sign-up | US1.AC1 |
| T002 | Signup with existing email | POST /api/auth/sign-up | US1.AC2 |
| T003 | Signup with weak password | POST /api/auth/sign-up | US1.AC3 |
| T004 | Login with correct credentials | POST /api/auth/sign-in | US2.AC1 |
| T005 | Login with incorrect password | POST /api/auth/sign-in | US2.AC2 |
| T006 | Login with non-existent email | POST /api/auth/sign-in | US2.AC3 |
| T007 | Refresh token | POST /api/auth/refresh | US3.AC2 |
| T008 | Logout invalidates token | POST /api/auth/sign-out | US3.AC3 |
| T009 | Database schema exists | Schema query | US4.AC1 |
| T010 | Unique constraint on email | INSERT duplicate email | US4.AC2 |
| T011 | Cascading delete | DELETE user | US4.AC3 |
| T012 | Health check when healthy | GET /api/health | US5.AC1 |
| T013 | Health check when DB down | GET /api/health (DB offline) | US5.AC2 |

---

## Deployment & Operations

### Local Development (Docker Compose)

```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: devuser
      POSTGRES_PASSWORD: devpass
      POSTGRES_DB: auth_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  auth-service:
    build: ./backend/auth-service
    environment:
      DATABASE_URL: postgresql://devuser:devpass@postgres:5432/auth_db
      JWT_SECRET: dev-secret-key
      ENVIRONMENT: development
    ports:
      - "3001:3001"
    depends_on:
      - postgres
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3001/api/health"]
      interval: 10s
      timeout: 5s
      retries: 3

volumes:
  postgres_data:
```

### Environment Configuration

**.env** (auth-service):
```bash
# Database
DATABASE_URL=postgresql://user:password@neon-host/auth_db

# JWT
JWT_SECRET=your-secret-key
JWT_ALGORITHM=RS256
JWT_EXPIRATION=86400  # 24 hours

# Service
PORT=3001
NODE_ENV=development
CORS_ORIGINS=http://localhost:3000,http://localhost:5000

# Rate Limiting
RATE_LIMIT_WINDOW_MS=900000  # 15 minutes
RATE_LIMIT_MAX_REQUESTS=5    # Per IP

# Logging
LOG_LEVEL=info
```

---

## Risks & Mitigation

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|-----------|
| Database connection issues | HIGH | LOW | Connection pooling, retry logic, health checks |
| Password hashing too slow | MEDIUM | LOW | Use better-auth defaults, test on target hardware |
| JWT secret exposure | HIGH | LOW | Use .env, rotate secret periodically, audit logs |
| Email enumeration vulnerability | MEDIUM | MEDIUM | Generic error messages, no email in errors |
| Concurrent signup race condition | MEDIUM | MEDIUM | Database unique constraint enforces atomicity |
| Service downtime | HIGH | LOW | Load balancing, horizontal scaling (future) |

---

## Success Checklist

Before moving to Iteration 2 (FastAPI Integration), verify:

- [ ] Better-auth service runs without errors
- [ ] All 5 user stories' acceptance scenarios pass
- [ ] All edge cases (EC1-EC5) validated
- [ ] All 13 Playwright tests pass
- [ ] Rate limiting working (429 responses)
- [ ] No sensitive data in logs or error messages
- [ ] Database schema verified via psql queries
- [ ] Health check endpoint responds correctly
- [ ] .env properly configured, secrets not in code
- [ ] docker-compose.yml works for local development
- [ ] Documentation complete (API reference, setup guide)

---

## References

Sources for better-auth specifications:
- [PostgreSQL | Better Auth](https://www.better-auth.com/docs/adapters/postgresql)
- [Database | Better Auth](https://www.better-auth.com/docs/concepts/database)
- [Installation | Better Auth](https://www.better-auth.com/docs/installation)
