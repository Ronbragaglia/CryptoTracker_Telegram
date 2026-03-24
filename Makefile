.PHONY: help install install-dev test test-cov lint format clean run docs build upload

help:
	@echo "Comandos disponíveis:"
	@echo "  make install       - Instala dependências de produção"
	@echo "  make install-dev   - Instala dependências de desenvolvimento"
	@echo "  make test          - Executa testes"
	@echo "  make test-cov      - Executa testes com cobertura"
	@echo "  make lint          - Executa verificação de código (flake8, mypy)"
	@echo "  make format        - Formata código (black)"
	@echo "  make clean         - Remove arquivos gerados"
	@echo "  make run           - Executa o crypto tracker"
	@echo "  make docs          - Gera documentação"
	@echo "  make build         - Constrói o pacote"
	@echo "  make upload        - Faz upload do pacote para PyPI"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -e ".[dev]"

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=src/crypto_tracker --cov-report=html --cov-report=term-missing

lint:
	flake8 src/ tests/ --max-line-length=100
	mypy src/ --strict

format:
	black src/ tests/ --line-length=100

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	find . -type f -name '*.pyd' -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf data/*.db
	rm -rf data/charts/*.png
	rm -rf data/backups/*
	rm -rf logs/*.log

run:
	python -m crypto_tracker

docs:
	cd docs && make html

build:
	python -m build

upload:
	twine upload dist/*
