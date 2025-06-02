# Makefile for projects_service CI/CD setup

.PHONY: build migrate up down restart

# Build and start containers in detached mode
up:
	docker-compose up -d --build

# Stop and remove containers, networks, and volumes
down:
	docker-compose down -v



# Wait for db then run migrations
wait-db:
	@echo "Waiting for PostgreSQL to be ready..."
	@docker-compose run --rm --entrypoint "" projects_service \
	sh -c 'until pg_isready -h db -U admin; do sleep 1; done'
	@echo "PostgreSQL is ready!"


# Run Django migrations inside the projects_service container
migrate:
	docker-compose exec projects_service python manage.py makemigrations
	docker-compose exec projects_service python manage.py migrate
	docker-compose exec links_service python manage.py makemigrations
	docker-compose exec links_service python manage.py migrate
# Run full CI/CD pipeline: build → wait → migrate → up
build:
	docker-compose build

ci:
	make build
	docker-compose up -d db
	make wait-db
	docker-compose up -d projects_service links_service
	make migrate

# Restart everything from scratch
restart:
	make down
	make ci