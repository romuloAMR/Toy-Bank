.PHONY: run dev test check clean help install

all: help

## install: Install all project dependencies using uv
install:
	uv sync

## run: Run the project
run:
	uv run uvicorn src.main:app

## dev: Run the project in development mode
dev:
	uv run uvicorn src.main:app --reload

## test: Run unit tests
test:
	uv run pytest tests/ -v

## check: Check all code base
check:
	uv run ruff check . --fix
	uv run ruff format .
	uv run mypy .

## clean: Clears the caches for Python, Pytest and Ruff
clean:
	@echo "Clearing caches..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type d -name ".ruff_cache" -exec rm -rf {} +
	@echo "Cleaning completed."

## help: Show help menu
help:
	@echo "Available commands:"
	@sed -n 's/^##//p' $(MAKEFILE_LIST) | column -t -s ':' |  sed -e 's/^/ /'
