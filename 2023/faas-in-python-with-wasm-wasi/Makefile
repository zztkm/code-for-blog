.PHONY: run
run:
	@echo "Running..."
	rye run uvicorn main:app --reload

.PHONY: fmt
fmt:
	rye run ruff format .

.PHONY: lint
lint:
	rye run ruff check .

.PHONY: fix
fix:
	rye run ruff check --fix .
