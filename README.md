# TaskFlow — Team Task & Project Management

TaskFlow is a small internal tool that lets teams organize work into projects,
break projects down into tasks, assign tasks to teammates, and discuss progress
via comments on each task. It was built as a straightforward 3-tier web
application:

- **Frontend:** React 18 + Vite (SPA, talks to the backend over a REST API)
- **Backend:** Python (Flask) REST API
- **Database:** PostgreSQL

> **Handover note (from Dev to DevOps):** This repository contains only
> application source code. There is intentionally no Dockerfile, no
> docker-compose file, no CI/CD pipeline, no Kubernetes manifests, and no
> infrastructure-as-code. Containerizing, orchestrating, deploying, and
> monitoring this application is the next phase of work.

---

## 1. Architecture Overview

```
┌──────────────────┐        HTTP/JSON        ┌──────────────────┐        SQL        ┌──────────────────┐
│   React + Vite   │  ───────────────────▶   │   Flask REST API │  ───────────────▶ │    PostgreSQL     │
│  (frontend/)     │  ◀───────────────────   │   (backend/)      │  ◀─────────────── │  (database/)      │
└──────────────────┘                         └──────────────────┘                    └──────────────────┘
```

The frontend never talks to the database directly — all data access goes
through the Flask API. Authentication is a simplified "fake login" (see
`backend/app/routes/auth.py`) — there is no real session/JWT framework, which
is intentional per project scope. This should be hardened before any real
production use.

---

## 2. Repository Layout

```
taskflow/
├── backend/                  # Flask REST API
│   ├── app/
│   │   ├── __init__.py       # application factory
│   │   ├── config.py         # env-driven configuration
│   │   ├── extensions.py     # shared extension instances (db, cors)
│   │   ├── models/           # SQLAlchemy models (User, Project, Task, TaskComment)
│   │   ├── routes/           # Flask blueprints (health, auth, projects, tasks, comments, users)
│   │   └── utils/            # logging setup, error handlers, auth decorator
│   ├── seed.py                # populates the DB with demo data via the ORM
│   ├── wsgi.py                # app entrypoint (`flask run` / gunicorn target)
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                  # React + Vite SPA
│   ├── src/
│   │   ├── api/               # axios client + one module per resource
│   │   ├── components/        # presentational + feature components
│   │   ├── context/            # AuthContext (fake login/session state)
│   │   ├── pages/              # Login, Dashboard, ProjectDetail, NotFound
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
│
├── database/
│   ├── schema.sql              # DDL for all 4 tables
│   ├── seed.sql                 # sample rows (equivalent to backend/seed.py)
│   └── README.md
│
├── .gitignore
└── README.md
```

---

## 3. Data Model

Four related tables:

| Table           | Purpose                                              |
|-----------------|-------------------------------------------------------|
| `users`         | People who can log in, own projects, be assigned tasks |
| `projects`      | A body of work, owned by a user                       |
| `tasks`         | Work items that belong to a project, optionally assigned to a user |
| `task_comments` | Discussion thread attached to a single task           |

Relationships: `users 1─N projects`, `projects 1─N tasks`, `users 1─N tasks (assignee)`, `tasks 1─N task_comments`, `users 1─N task_comments (author)`.

See `database/schema.sql` for full column definitions, constraints, and indexes.

---

## 4. Running the App Locally

These instructions assume a developer/DevOps engineer running everything
directly on a workstation (no containers yet).

### 4.1 Database

1. Install PostgreSQL locally (or point at any reachable instance).
2. Create a database and user:
   ```sql
   CREATE DATABASE taskflow_db;
   CREATE USER taskflow_user WITH PASSWORD 'taskflow_pass';
   GRANT ALL PRIVILEGES ON DATABASE taskflow_db TO taskflow_user;
   ```
3. Load the schema and seed data:
   ```bash
   psql -U taskflow_user -d taskflow_db -f database/schema.sql
   psql -U taskflow_user -d taskflow_db -f database/seed.sql
   ```

### 4.2 Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # then edit DATABASE_URL etc.
flask --app wsgi run --debug --port 5000
```

The API will be available at `http://localhost:5000`. Check it's alive:

```bash
curl http://localhost:5000/health
```

> Alternative to loading `database/seed.sql`: run `python seed.py` from the
> `backend/` folder (with the venv active and `.env` configured) to seed the
> same demo data through the ORM instead of raw SQL.

### 4.3 Frontend

```bash
cd frontend
npm install
cp .env.example .env               # then edit VITE_API_URL if needed
npm run dev
```

The app will be available at `http://localhost:5173`.

### 4.4 Demo login

The seed data creates these users (fake-login accepts any of them):

| Username | Password     |
|----------|--------------|
| jsmith    | password123  |
| agarcia   | password123  |
| mchen     | password123  |

---

## 5. Environment Variables

### Backend (`backend/.env`)

| Variable         | Description                                  | Example                                                        |
|------------------|-----------------------------------------------|-----------------------------------------------------------------|
| `FLASK_ENV`      | `development` or `production`                | `development`                                                    |
| `FLASK_DEBUG`    | `1` to enable debug mode                     | `1`                                                               |
| `SECRET_KEY`     | Flask secret key                             | `change-me-in-production`                                        |
| `DATABASE_URL`   | SQLAlchemy Postgres connection string        | `postgresql://taskflow_user:taskflow_pass@localhost:5432/taskflow_db` |
| `CORS_ORIGINS`   | Comma-separated allowed origins for the SPA  | `http://localhost:5173`                                          |
| `LOG_LEVEL`      | Python logging level                         | `INFO`                                                            |
| `PORT`           | Port the app listens on (used by wsgi.py)    | `5000`                                                            |

### Frontend (`frontend/.env`)

| Variable         | Description                        | Example                    |
|------------------|--------------------------------------|-----------------------------|
| `VITE_API_URL`   | Base URL of the backend API          | `http://localhost:5000`    |

---

## 6. API Overview

All endpoints (except `/health`) are prefixed with `/api`.

| Method | Path                              | Description                       |
|--------|------------------------------------|------------------------------------|
| GET    | `/health`                          | Liveness/readiness + DB connectivity check |
| POST   | `/api/auth/login`                  | Fake login, returns a token + user |
| GET    | `/api/users`                       | List users (for assignee dropdowns) |
| GET    | `/api/projects`                    | List all projects                  |
| POST   | `/api/projects`                    | Create a project                   |
| GET    | `/api/projects/<id>`                | Get one project                    |
| PUT    | `/api/projects/<id>`                | Update a project                   |
| DELETE | `/api/projects/<id>`                | Delete a project (cascades tasks)  |
| GET    | `/api/projects/<id>/tasks`           | List tasks for a project            |
| GET    | `/api/tasks`                        | List all tasks (supports `?status=`, `?project_id=`) |
| POST   | `/api/tasks`                        | Create a task                      |
| GET    | `/api/tasks/<id>`                    | Get one task                       |
| PUT    | `/api/tasks/<id>`                    | Update a task                      |
| DELETE | `/api/tasks/<id>`                    | Delete a task                      |
| GET    | `/api/tasks/<id>/comments`            | List comments for a task           |
| POST   | `/api/tasks/<id>/comments`            | Add a comment to a task            |

Errors are returned as JSON: `{ "error": "message" }` with an appropriate HTTP status code.

---

## 7. Known Limitations / TODOs (intentional, left for future iterations)

- Login is intentionally fake (no password reset, no real sessions/JWT, no RBAC).
- No pagination on list endpoints yet — fine for demo data volume, would need
  attention at scale.
- No automated test suite included in this version.
- No rate limiting / brute-force protection on the login endpoint.

These are marked with `# TODO` comments at the relevant place in the code.

---

## 8. What's Deliberately NOT Included

Per project scope, this repository contains **application code only**. It does
not include Dockerfiles, docker-compose, Kubernetes manifests, Helm charts,
Terraform, GitHub Actions/Jenkins pipelines, Nginx config, or any monitoring
setup — all of that is intentionally left for the DevOps phase of this
project.
