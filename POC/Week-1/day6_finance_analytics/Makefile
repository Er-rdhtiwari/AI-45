.PHONY: install test lint local seed run benchmark stats docker-up docker-down

install:
	python -m pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check .

local:
	DATABASE_URL=sqlite:///./finance.db REDIS_URL=memory:// AUTO_CREATE_SCHEMA=true python scripts/seed_db.py

seed:
	python scripts/seed_db.py

run:
	uvicorn app.main:app --reload

benchmark:
	python scripts/benchmark.py

stats:
	python scripts/run_statistics.py

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down -v
