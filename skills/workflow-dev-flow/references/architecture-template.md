# Architecture Template

## 1. Overview

- **Project Name**: {project-name}
- **Description**: {brief-description}
- **Tech Stack**: {frontend}/{backend}/{database}/{other}

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Client Layer                           │
│  (Web / Mobile / Desktop)                                   │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                      API Gateway                            │
│  (Authentication / Rate Limiting / Routing)                 │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                     Service Layer                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │ Service A│  │ Service B│  │ Service C│                  │
│  └──────────┘  └──────────┘  └──────────┘                  │
└───────────────────────────┬─────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                     Data Layer                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │  DB SQL  │  │   Redis  │  │   S3     │                  │
│  └──────────┘  └──────────┘  └──────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Module Structure

```
project-root/
├── src/
│   ├── modules/
│   │   ├── module-a/
│   │   │   ├── controllers/
│   │   │   ├── services/
│   │   │   ├── repositories/
│   │   │   └── models/
│   │   └── module-b/
│   ├── shared/
│   │   ├── utils/
│   │   ├── middleware/
│   │   └── types/
│   └── config/
├── tests/
├── docs/
└── scripts/
```

## 3. API Design

### 3.1 Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | `/api/resource` | List resources | Yes |
| POST | `/api/resource` | Create resource | Yes |
| GET | `/api/resource/:id` | Get resource by ID | Yes |
| PUT | `/api/resource/:id` | Update resource | Yes |
| DELETE | `/api/resource/:id` | Delete resource | Yes |

### 3.2 Request/Response Format

**Request**:
```json
{
  "field1": "value1",
  "field2": "value2"
}
```

**Response (Success)**:
```json
{
  "code": 200,
  "data": {
    "id": "uuid",
    "field1": "value1",
    "field2": "value2",
    "createdAt": "2026-04-02T12:00:00Z"
  },
  "message": "Success"
}
```

**Response (Error)**:
```json
{
  "code": 400,
  "error": {
    "message": "Validation failed",
    "details": ["field1 is required"]
  }
}
```

## 4. Data Model

### 4.1 Entity: {EntityName}

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | UUID | Yes | Primary key |
| name | String | Yes | Entity name |
| status | Enum | Yes | Status: active/inactive |
| createdAt | DateTime | Yes | Creation timestamp |
| updatedAt | DateTime | Yes | Last update timestamp |

### 4.2 Relationships

```
{EntityA} 1 ──── N {EntityB}
{EntityB} N ──── N {EntityC}
```

## 5. Security

- **Authentication**: JWT / OAuth2
- **Authorization**: RBAC (Role-Based Access Control)
- **Data Encryption**: TLS in transit, AES-256 at rest
- **Input Validation**: Schema validation on all endpoints

## 6. Deployment

### 6.1 Environment

| Environment | URL | Purpose |
|-------------|-----|---------|
| Development | localhost | Local development |
| Staging | staging.example.com | Pre-production testing |
| Production | api.example.com | Live environment |

### 6.2 CI/CD Pipeline

```
Code Push → Lint → Test → Build → Deploy Staging → Integration Test → Deploy Production
```

## 7. Task List

### Phase 1: Foundation
- [ ] Task 1.1: Setup project structure
- [ ] Task 1.2: Configure database
- [ ] Task 1.3: Setup authentication

### Phase 2: Core Features
- [ ] Task 2.1: Implement Module A
- [ ] Task 2.2: Implement Module B
- [ ] Task 2.3: Implement API endpoints

### Phase 3: Testing & Polish
- [ ] Task 3.1: Write unit tests
- [ ] Task 3.2: Write integration tests
- [ ] Task 3.3: Performance optimization

### Phase 4: Deployment
- [ ] Task 4.1: Setup CI/CD pipeline
- [ ] Task 4.2: Deploy to staging
- [ ] Task 4.3: Deploy to production
