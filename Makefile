.PHONY: all setup run-all test lint clean help

all: test run-all

setup:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

build-notebooks:
	python scripts/build_day_notebooks.py

run-all:
	python run_all.py

test:
	pytest tests/ -v

test-cov:
	pytest --cov=src --cov-report=term-missing tests/

lint:
	ruff check src/ tests/ scripts/

clean:
	python -c "import shutil, pathlib; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('__pycache__')]"
	python -c "import shutil, pathlib; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('.pytest_cache')]"

help:
	@echo "AquaGuard AI Engineering Automation:"
	@echo "  make setup           - Install dependencies from requirements.txt"
	@echo "  make build-notebooks - Re-generate all 17 day-aligned notebooks"
	@echo "  make run-all         - Execute all day notebooks sequentially via run_all.py"
	@echo "  make test            - Run full pytest test suite (54+ tests)"
	@echo "  make test-cov        - Run pytest with module coverage analysis"
	@echo "  make lint            - Check code style and PEP 8 conformity via ruff"
	@echo "  make clean           - Clear pycache and test caches"
