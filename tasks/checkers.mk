check-types: ## Check the project code types with mypy.
	poetry run mypy src/qto_categorizer_api/ tests/ --config-file .mypy.ini

check-tests: ## Check the project unit tests with pytest.
	poetry run pytest --numprocesses="auto" tests/

check-format: ## Check the project source format with ruff.
	poetry run ruff format --check src/qto_categorizer_api/ tests/

check-poetry: ## Check the project pyproject.toml with poetry.
	poetry check --lock

check-quality: ## Check the project code quality with ruff.
	poetry run ruff check src/qto_categorizer_api/ tests/

check-security: ## Check the project code security with bandit.
	poetry run bandit --recursive --configfile=pyproject.toml src/qto_categorizer_api/

check-coverage: ## Check the project test coverage with coverage.
	poetry run pytest --cov=src/qto_categorizer_api/ --cov-fail-under=80 --numprocesses="auto" tests/

checkers: check-format check-quality check-security ## Run all the checkers. (TODO: add check-coverage)