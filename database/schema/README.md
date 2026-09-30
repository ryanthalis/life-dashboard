# PostgreSQL Schema

The initial schema is split into numbered files and executed in dependency order
by `apply.sql`. The entrypoint stops at the first SQL error and wraps all included
files in one transaction so a failed application does not leave a partial schema.

Run the schema from the `docker` directory after the services are healthy:

```powershell
docker compose exec -T postgres psql `
  -U life_dashboard_app `
  -d life_dashboard `
  -f /schema/apply.sql
```

The schema directory is mounted read-only at `/schema` inside the PostgreSQL
container. Schema files can be read by `psql` but cannot be changed from inside
the container.
