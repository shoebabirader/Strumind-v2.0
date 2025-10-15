# 🏗️ StruMind Security Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT (Browser/App)                     │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                │ HTTPS/TLS
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                        API GATEWAY / NGINX                       │
│                    (SSL Termination, Load Balancing)             │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                         FASTAPI APPLICATION                      │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              MIDDLEWARE STACK (Ordered)                  │   │
│  │                                                           │   │
│  │  1. CORS Middleware                                      │   │
│  │     ├─ Allow Origins: Configurable                       │   │
│  │     ├─ Allow Credentials: True                           │   │
│  │     └─ Allow Methods: All                                │   │
│  │                                                           │   │
│  │  2. Rate Limiter Middleware                              │   │
│  │     ├─ 100 requests/minute per IP                        │   │
│  │     ├─ Automatic cleanup                                 │   │
│  │     ├─ Rate limit headers                                │   │
│  │     └─ 429 error when exceeded                           │   │
│  │                                                           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   ROUTING LAYER                          │   │
│  │                                                           │   │
│  │  PUBLIC ENDPOINTS (No Auth Required):                    │   │
│  │  ├─ GET  /                                               │   │
│  │  ├─ GET  /health                                         │   │
│  │  ├─ GET  /docs                                           │   │
│  │  ├─ POST /api/auth/register                              │   │
│  │  ├─ POST /api/auth/login                                 │   │
│  │  └─ GET  /api/auth/disclaimer                            │   │
│  │                                                           │   │
│  │  PROTECTED ENDPOINTS (Auth Required):                    │   │
│  │  ├─ GET  /api/auth/me                                    │   │
│  │  ├─ POST /api/auth/disclaimer/accept                     │   │
│  │  ├─ All /api/projects/*                                  │   │
│  │  ├─ All /api/analysis/*                                  │   │
│  │  ├─ All /api/design/*                                    │   │
│  │  └─ All /api/versions/*                                  │   │
│  │                                                           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              AUTHENTICATION LAYER                        │   │
│  │                                                           │   │
│  │  JWT Token Validation:                                   │   │
│  │  ├─ Extract Bearer token from header                     │   │
│  │  ├─ Verify signature (HS256)                             │   │
│  │  ├─ Check expiration (30 min)                            │   │
│  │  ├─ Extract user_id and username                         │   │
│  │  └─ Return 401 if invalid                                │   │
│  │                                                           │   │
│  │  Password Security:                                      │   │
│  │  ├─ Bcrypt hashing (cost factor 12)                      │   │
│  │  ├─ Salt automatically generated                         │   │
│  │  └─ No plaintext passwords stored                        │   │
│  │                                                           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                 BUSINESS LOGIC LAYER                     │   │
│  │                                                           │   │
│  │  ├─ Structural Analysis Engine                           │   │
│  │  ├─ Design Code Implementations                          │   │
│  │  ├─ ML/AI Features                                       │   │
│  │  ├─ Project Management                                   │   │
│  │  └─ Version Control                                      │   │
│  │                                                           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                      DATABASE LAYER                              │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │    Users     │  │   Projects   │  │   Versions   │          │
│  ├──────────────┤  ├──────────────┤  ├──────────────┤          │
│  │ id           │  │ id           │  │ id           │          │
│  │ username     │  │ name         │  │ project_id   │          │
│  │ email        │  │ user_id      │  │ version_num  │          │
│  │ hashed_pwd   │  │ data         │  │ data         │          │
│  │ is_active    │  │ created_at   │  │ created_at   │          │
│  │ accepted_dis │  └──────────────┘  │ created_by   │          │
│  └──────────────┘                    └──────────────┘          │
│                                                                   │
│  PostgreSQL / SQLite                                             │
└─────────────────────────────────────────────────────────────────┘
```

## Authentication Flow

```
┌──────────┐                                    ┌──────────┐
│  Client  │                                    │  Server  │
└────┬─────┘                                    └────┬─────┘
     │                                                │
     │  1. POST /api/auth/login                      │
     │     {username, password}                      │
     ├──────────────────────────────────────────────>│
     │                                                │
     │                                          2. Verify
     │                                          password
     │                                          (bcrypt)
     │                                                │
     │                                          3. Generate
     │                                          JWT token
     │                                          (30 min exp)
     │                                                │
     │  4. Return token                              │
     │     {access_token, token_type}                │
     │<──────────────────────────────────────────────┤
     │                                                │
     │  5. Store token in memory/storage             │
     │                                                │
     │  6. Make authenticated request                │
     │     Authorization: Bearer <token>             │
     ├──────────────────────────────────────────────>│
     │                                                │
     │                                          7. Validate
     │                                          token
     │                                          signature
     │                                                │
     │                                          8. Check
     │                                          expiration
     │                                                │
     │                                          9. Extract
     │                                          user info
     │                                                │
     │                                          10. Process
     │                                          request
     │                                                │
     │  11. Return response                          │
     │<──────────────────────────────────────────────┤
     │                                                │
```

## Rate Limiting Flow

```
┌──────────┐                                    ┌──────────┐
│  Client  │                                    │  Server  │
└────┬─────┘                                    └────┬─────┘
     │                                                │
     │  Request 1-100                                │
     ├──────────────────────────────────────────────>│
     │                                                │
     │                                          Check IP
     │                                          in rate
     │                                          limit map
     │                                                │
     │                                          Count: 1-100
     │                                          Status: OK
     │                                                │
     │  Response + Headers                           │
     │  X-RateLimit-Limit: 100                       │
     │  X-RateLimit-Remaining: 99-0                  │
     │<──────────────────────────────────────────────┤
     │                                                │
     │  Request 101                                  │
     ├──────────────────────────────────────────────>│
     │                                                │
     │                                          Check IP
     │                                          Count: 101
     │                                          Status: EXCEEDED
     │                                                │
     │  429 Too Many Requests                        │
     │  {detail: "Rate limit exceeded",              │
     │   retry_after: 60}                            │
     │<──────────────────────────────────────────────┤
     │                                                │
     │  Wait 60 seconds...                           │
     │                                                │
     │  Request (after reset)                        │
     ├──────────────────────────────────────────────>│
     │                                                │
     │                                          Count: 1
     │                                          Status: OK
     │                                                │
     │  Response                                     │
     │<──────────────────────────────────────────────┤
     │                                                │
```

## Version Control Flow

```
┌──────────┐                                    ┌──────────┐
│  Client  │                                    │  Server  │
└────┬─────┘                                    └────┬─────┘
     │                                                │
     │  1. User modifies project                     │
     │                                                │
     │  2. POST /api/versions                        │
     │     {project_id, commit_message, data}        │
     ├──────────────────────────────────────────────>│
     │                                                │
     │                                          3. Authenticate
     │                                          user
     │                                                │
     │                                          4. Get current
     │                                          version number
     │                                                │
     │                                          5. Create
     │                                          snapshot:
     │                                          - Project data
     │                                          - Model data
     │                                          - Analysis results
     │                                                │
     │                                          6. Store in DB
     │                                          with metadata
     │                                                │
     │  7. Return version info                       │
     │     {id, version_number, created_at}          │
     │<──────────────────────────────────────────────┤
     │                                                │
     │  8. Later: GET /api/projects/1/versions       │
     ├──────────────────────────────────────────────>│
     │                                                │
     │  9. Return version history                    │
     │     [{v1}, {v2}, {v3}...]                     │
     │<──────────────────────────────────────────────┤
     │                                                │
     │  10. Restore: POST /api/projects/1/restore/2  │
     ├──────────────────────────────────────────────>│
     │                                                │
     │                                          11. Load v2 data
     │                                          12. Create new
     │                                          version with
     │                                          restored data
     │                                                │
     │  13. Return success                           │
     │<──────────────────────────────────────────────┤
     │                                                │
```

## Security Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    Layer 7: Application                      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ - Input validation                                     │  │
│  │ - Business logic security                              │  │
│  │ - Legal disclaimers                                    │  │
│  │ - Version control                                      │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────┴───────────────────────────────┐
│                    Layer 6: Authentication                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ - JWT token validation                                 │  │
│  │ - User session management                              │  │
│  │ - Password verification                                │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────┴───────────────────────────────┐
│                    Layer 5: Rate Limiting                    │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ - Request counting per IP                              │  │
│  │ - Throttling enforcement                               │  │
│  │ - DDoS protection                                      │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────┴───────────────────────────────┐
│                    Layer 4: CORS                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ - Origin validation                                    │  │
│  │ - Credential handling                                  │  │
│  │ - Method restrictions                                  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────┴───────────────────────────────┐
│                    Layer 3: TLS/HTTPS                        │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ - Encryption in transit                                │  │
│  │ - Certificate validation                               │  │
│  │ - Secure protocols (TLS 1.2+)                          │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────┴───────────────────────────────┐
│                    Layer 2: Network                          │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ - Firewall rules                                       │  │
│  │ - VPC/Security groups                                  │  │
│  │ - IP whitelisting                                      │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────┴───────────────────────────────┐
│                    Layer 1: Infrastructure                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ - Physical security                                    │  │
│  │ - Cloud provider security                              │  │
│  │ - Backup systems                                       │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow Security

```
┌─────────────┐
│   Client    │
│  (Browser)  │
└──────┬──────┘
       │
       │ 1. User enters credentials
       │
       ▼
┌─────────────┐
│   HTTPS     │ ← Encrypted in transit
│  (TLS 1.2+) │
└──────┬──────┘
       │
       │ 2. Secure transmission
       │
       ▼
┌─────────────┐
│ Rate Limit  │ ← Check request count
│  Middleware │
└──────┬──────┘
       │
       │ 3. Within limits?
       │
       ▼
┌─────────────┐
│    Auth     │ ← Verify JWT token
│  Middleware │
└──────┬──────┘
       │
       │ 4. Valid token?
       │
       ▼
┌─────────────┐
│  Business   │ ← Process request
│   Logic     │
└──────┬──────┘
       │
       │ 5. Execute operation
       │
       ▼
┌─────────────┐
│  Database   │ ← Encrypted at rest
│  (Postgres) │    (optional)
└──────┬──────┘
       │
       │ 6. Return data
       │
       ▼
┌─────────────┐
│  Response   │ ← Add security headers
│  Formatter  │
└──────┬──────┘
       │
       │ 7. Format response
       │
       ▼
┌─────────────┐
│   HTTPS     │ ← Encrypted in transit
│  (TLS 1.2+) │
└──────┬──────┘
       │
       │ 8. Secure transmission
       │
       ▼
┌─────────────┐
│   Client    │
│  (Browser)  │
└─────────────┘
```

## Security Headers

All responses include:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1697123456
Access-Control-Allow-Origin: https://yourdomain.com
Access-Control-Allow-Credentials: true
Content-Type: application/json
```

## Token Structure

JWT Token Format:
```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "username",
    "user_id": 123,
    "exp": 1697123456
  },
  "signature": "..."
}
```

## Database Security

```
┌─────────────────────────────────────────┐
│           User Table                     │
├─────────────────────────────────────────┤
│ id: 1                                    │
│ username: "engineer1"                    │
│ email: "engineer@example.com"            │
│ hashed_password: "$2b$12$..."  ← Bcrypt │
│ is_active: true                          │
│ accepted_disclaimer: true                │
│ disclaimer_accepted_at: "2025-10-15"     │
└─────────────────────────────────────────┘
         │
         │ Foreign Key
         ▼
┌─────────────────────────────────────────┐
│         Project Table                    │
├─────────────────────────────────────────┤
│ id: 1                                    │
│ user_id: 1  ← Owner                      │
│ name: "Building A"                       │
│ data: {...}                              │
└─────────────────────────────────────────┘
         │
         │ Foreign Key
         ▼
┌─────────────────────────────────────────┐
│      Version Table                       │
├─────────────────────────────────────────┤
│ id: 1                                    │
│ project_id: 1                            │
│ version_number: 1                        │
│ created_by: 1  ← User who created        │
│ commit_message: "Initial version"        │
│ project_data: {...}  ← Full snapshot     │
│ created_at: "2025-10-15 10:00:00"        │
└─────────────────────────────────────────┘
```

## Threat Mitigation

| Threat | Mitigation | Status |
|--------|------------|--------|
| Unauthorized Access | JWT Authentication | ✅ |
| Brute Force | Rate Limiting | ✅ |
| DDoS | Rate Limiting + Load Balancer | ✅ |
| SQL Injection | SQLAlchemy ORM | ✅ |
| XSS | Input Validation | ✅ |
| CSRF | Token-based Auth | ✅ |
| Man-in-Middle | HTTPS/TLS | ✅ |
| Data Loss | Version Control | ✅ |
| Legal Liability | Disclaimers | ✅ |
| Password Theft | Bcrypt Hashing | ✅ |

## Monitoring Points

```
┌─────────────────────────────────────────┐
│         Monitoring Dashboard             │
├─────────────────────────────────────────┤
│                                          │
│  Authentication Metrics:                 │
│  ├─ Login attempts                       │
│  ├─ Failed logins                        │
│  ├─ Active sessions                      │
│  └─ Token expirations                    │
│                                          │
│  Rate Limiting Metrics:                  │
│  ├─ Requests per minute                  │
│  ├─ Rate limit violations                │
│  ├─ Top IPs by request count             │
│  └─ Blocked requests                     │
│                                          │
│  Legal Compliance:                       │
│  ├─ Disclaimer views                     │
│  ├─ Disclaimer acceptances               │
│  ├─ Acceptance rate                      │
│  └─ Pending acceptances                  │
│                                          │
│  Version Control:                        │
│  ├─ Versions created                     │
│  ├─ Restore operations                   │
│  ├─ Storage usage                        │
│  └─ Version age distribution             │
│                                          │
└─────────────────────────────────────────┘
```

---

**Architecture Version**: 1.0  
**Last Updated**: October 15, 2025  
**Status**: Production Ready
