PYTHON = uv run python
SRC = src/main.py

.PHONY: run clean help

all: help

## run: Run the project
run:
	@$(PYTHON) $(SRC)

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
