.PHONY: install dev lint test docs docs-serve run format i18n-check doctor

install:
	python -m pip install -e .

dev:
	python -m pip install -e ".[dev]"

remove:
	python -m pip uninstall -y plastmorph

lint:
	python -m ruff check .

test:
	python -m pytest -q

i18n-check:
	python -m pytest -q tests/test_i18n.py

docs:
	python -m mkdocs build

docs-serve:
	python -m mkdocs serve

run:
	python -m streamlit run app/streamlit_app.py

format:
	python -m ruff check . --fix

doctor:
	@echo "PWD=$$(pwd)"
	@echo "python path: $$(command -v python || echo 'not found')"
# 	@echo "pip path: $$(command -v pip || echo 'not found')"
# 	@python -V || true
# 	@python -m pip -V || true
# 	@pip -V || true
	@python -c "import sys; print('python executable:', sys.executable); print('sys.prefix:', sys.prefix)" || true
# 	@python -m pip list | grep -i '^plastmorph ' || true
	@pip list | grep -i '^plastmorph ' || true
	@python -c "import plastmorph; print('python import: OK from', plastmorph.__file__)" || true
	@python -m streamlit --version || true
