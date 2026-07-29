.PHONY: install dev lint test docs docs-serve run format i18n-check

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

lint:
	ruff check .

test:
	pytest -q

i18n-check:
	pytest -q tests/test_i18n.py

docs:
	mkdocs build

docs-serve:
	mkdocs serve

run:
	streamlit run app/streamlit_app.py

format:
	ruff check . --fix
