# Makefile for projects_service CI/CD setup

.PHONY: build migrate up down restart

# Build and start containers in detached mode
up:
	docker-compose up -d --build

# Stop and remove containers, networks, and volumes
down:
	docker-compose down -v

# Run Django migrations inside the projects_service container
migrate:
	docker-compose exec projects_service python manage.py makemigrations
	docker-compose exec projects_service python manage.py migrate

# Wait for db then run migrations
wait-db:
	@echo "Waiting for PostgreSQL to be ready..."
	@until docker-compose exec db pg_isready -U admin; do sleep 1; done
	@echo "PostgreSQL is ready!"

# Run full CI/CD pipeline: build → wait → migrate → up
build:
	docker-compose build

ci:
	make build
	docker-compose up -d
	make wait-db
	make migrate

# Restart everything from scratch
restart:
	make down
	make ci