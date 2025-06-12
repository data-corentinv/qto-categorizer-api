format-sources: ## Format the project sources.
	poetry run ruff format src/qto_categorizer_api/ tests/

formatters: format-sources ## Run all the formatters.