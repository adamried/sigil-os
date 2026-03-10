# Stack Detection Patterns

Reference material for **Step 2: Stack Detection** of the `codebase-assessment` skill.

## Per-Manifest Detection Patterns

### package.json (Node/TypeScript)

```
- Language: Check for `typescript` in dependencies/devDependencies → TypeScript, else JavaScript
- Framework:
  - `next` → Next.js
  - `react` (without next) → React
  - `vue` → Vue
  - `@angular/core` → Angular
  - `express` → Express
  - `fastify` → Fastify
- Database:
  - `prisma` or `@prisma/client` → check prisma/schema.prisma for provider
  - `pg` or `postgres` → PostgreSQL
  - `mysql2` → MySQL
  - `mongoose` or `mongodb` → MongoDB
  - `better-sqlite3` or `sqlite3` → SQLite
- ORM:
  - `@prisma/client` → Prisma
  - `sequelize` → Sequelize
  - `typeorm` → TypeORM
  - `drizzle-orm` → Drizzle
- Test Framework:
  - `jest` → Jest
  - `vitest` → Vitest
  - `mocha` → Mocha
  - `@playwright/test` → Playwright
  - `cypress` → Cypress
```

### go.mod

```
- Language: Go + version from `go X.XX` line
- Framework:
  - `github.com/gin-gonic/gin` → Gin
  - `github.com/labstack/echo` → Echo
  - `github.com/gofiber/fiber` → Fiber
  - `github.com/gorilla/mux` → Gorilla Mux
- Database:
  - `github.com/lib/pq` → PostgreSQL
  - `github.com/go-sql-driver/mysql` → MySQL
  - `github.com/mattn/go-sqlite3` → SQLite
- ORM:
  - `gorm.io/gorm` → GORM
  - `github.com/uptrace/bun` → Bun
  - `entgo.io/ent` → Ent
```

### pyproject.toml / requirements.txt

```
- Language: Python + version from requires-python or python_requires
- Framework:
  - `django` → Django
  - `fastapi` → FastAPI
  - `flask` → Flask
  - `starlette` → Starlette
- Database:
  - `psycopg2` or `psycopg` → PostgreSQL
  - `pymysql` or `mysqlclient` → MySQL
  - `pymongo` → MongoDB
- ORM:
  - `sqlalchemy` → SQLAlchemy
  - `django` (implies) → Django ORM
  - `tortoise-orm` → Tortoise ORM
  - `peewee` → Peewee
- Test Framework:
  - `pytest` → pytest
  - `unittest` (stdlib) → unittest
```

### Cargo.toml

```
- Language: Rust + edition from [package] section
- Framework:
  - `actix-web` → Actix Web
  - `axum` → Axum
  - `rocket` → Rocket
  - `warp` → Warp
- ORM:
  - `diesel` → Diesel
  - `sea-orm` → SeaORM
  - `sqlx` → SQLx
```

### Gemfile

```
- Language: Ruby + version from .ruby-version or Gemfile ruby directive
- Framework:
  - `rails` → Rails
  - `sinatra` → Sinatra
  - `hanami` → Hanami
- ORM:
  - Rails implies → ActiveRecord
  - `sequel` → Sequel
- Database:
  - `pg` → PostgreSQL
  - `mysql2` → MySQL
  - `sqlite3` → SQLite
- Test Framework:
  - `rspec` → RSpec
  - `minitest` → Minitest
```

## Confidence Rules

| Confidence | Criteria |
|------------|----------|
| `confident` | Found in manifest file with explicit declaration (dependency, config key, or version) |
| `uncertain` | File extensions only, OR conflicting signals (e.g., both jest and vitest), OR no version found |

## Stack Detection Output Schema

```json
{
  "detected_stack": {
    "language": { "name": "TypeScript", "version": "5.x", "confidence": "confident", "source": "package.json" },
    "framework": { "name": "Next.js", "version": "14.x", "confidence": "confident", "source": "package.json" },
    "database": { "name": "PostgreSQL", "confidence": "confident", "source": "prisma/schema.prisma" },
    "orm": { "name": "Prisma", "version": "5.x", "confidence": "confident", "source": "package.json" },
    "test_framework": { "name": "Jest", "confidence": "confident", "source": "package.json:devDependencies" }
  }
}
```
