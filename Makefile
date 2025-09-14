SHELL := /bin/bash
PROJECT := occupancy-platform

.PHONY: dev up down logs rebuild seed ingest test unit int load e2e fmt

dev: up
up:
	docker compose up -d --build

down:
	docker compose down -v

logs:
	docker compose logs -f gateway forecast

rebuild:
	docker compose build --no-cache

seed:
	docker run --rm --network host -v $$PWD/dbt_occupancy:/usr/app -w /usr/app \
		-e DBT_HOST=localhost -e DBT_USER=postgres -e DBT_PASSWORD=postgres -e DBT_DB=occupancy \
		ghcr.io/dbt-labs/dbt-postgres:1.7.4 dbt seed --profiles-dir . && \
	docker run --rm --network host -v $$PWD/dbt_occupancy:/usr/app -w /usr/app \
		-e DBT_HOST=localhost -e DBT_USER=postgres -e DBT_PASSWORD=postgres -e DBT_DB=occupancy \
		ghcr.io/dbt-labs/dbt-postgres:1.7.4 dbt run --profiles-dir .

ingest:
	docker compose run --rm ingest

test: unit int
unit:
	python -m pytest -q tests/unit

int:
	python -m pytest -q tests/integration

load:
	k6 run tests/load/k6_forecast.js --env FORECAST_URL=http://localhost:8000 --vus 20 --duration 45s

e2e:
	cd apps/dashboard && pnpm i && pnpm exec playwright install --with-deps && pnpm exec playwright test

fmt:
	gofmt -w services/gateway services/ingest || true
