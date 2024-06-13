env:
	cp .env.template .env

build:
	docker compose -f docker-compose.yaml -f docker-compose.otel.yaml build

up:
	docker compose -f docker-compose.yaml -f docker-compose.otel.yaml up -d

down:
	docker compose -f docker-compose.yaml -f docker-compose.otel.yaml down

rebuild:
	docker compose -f docker-compose.yaml -f docker-compose.otel.yaml down
	docker compose -f docker-compose.yaml -f docker-compose.otel.yaml build
	docker compose -f docker-compose.yaml -f docker-compose.otel.yaml up -d

build-dev:
	docker compose build

up-dev:
	docker compose up -d

down-dev:
	docker compose down

destroy-dev:
	docker compose down -v

.PHONY: tests
tests: unit-tests integration-tests functional-tests

unit-tests:
	poetry run pytest src/tests/unit

integration-tests:
	poetry run pytest src/tests/integration

functional-tests:
	poetry run pytest -W ignore::DeprecationWarning src/tests/functional

linter:
	poetry run pre-commit run --all-files

check:
	poetry run ruff check && poetry run ruff format --check && poetry run mypy .