# TaskFlow Database

Plain SQL files for setting up PostgreSQL by hand (e.g. against a local
Postgres instance, or later an RDS instance). These are independent of the
Flask ORM models — either this schema or the ORM's `db.create_all()` will
produce a compatible database, but for a real handover you should treat
`schema.sql` as the source of truth and manage changes to it deliberately
(e.g. with a migration tool) rather than relying on `create_all()`.

## Files

- `schema.sql` — creates the 4 tables (`users`, `projects`, `tasks`, `task_comments`), their foreign keys, check constraints, and indexes.
- `seed.sql` — truncates and repopulates the tables with demo data (3 users, 3 projects, 10 tasks, 6 comments). All seeded users share the password `password123`.

## Usage

```bash
psql -U taskflow_user -d taskflow_db -f schema.sql
psql -U taskflow_user -d taskflow_db -f seed.sql
```

## TODO

- Introduce a proper migration tool (e.g. Alembic) once the schema needs to
  evolve across environments instead of hand-running these files.
