# Local Docker Environment

This folder contains the local PostgreSQL and pgAdmin development environment.
Run the Docker Compose commands from this directory so Compose automatically
loads the adjacent `.env` file.

## Files

- `compose.yaml` defines the services, ports, health check, network behavior,
  and persistent volumes.
- `.env.example` documents the required environment variables using placeholder
  passwords and is safe to commit.
- `.env` contains working local credentials and is intentionally ignored by Git.

## Commands

```powershell
Set-Location docker
docker compose up --detach --wait
docker compose ps
docker compose logs postgres
docker compose logs pgadmin
docker compose down
```

`docker compose down` removes the containers and Compose network but retains the
named volumes. Do not add `--volumes` unless deleting the local database and
pgAdmin state is intentional.

## Local endpoints

- PostgreSQL: `127.0.0.1:5432`
- pgAdmin: <http://127.0.0.1:5050>

From pgAdmin, use `postgres` as the database server hostname because pgAdmin and
PostgreSQL communicate over the Compose network. `localhost` inside the pgAdmin
container refers to pgAdmin's own container, not the PostgreSQL container.
