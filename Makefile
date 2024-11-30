format:
	poetry run isort .
	poetry run black . --diff --color
	poetry run black .

lint:
	poetry run pytest
	poetry run black --check .
	poetry run bandit -r peterpy
	poetry run mypy --no-strict-optional --ignore-missing-imports peterpy
	poetry run pylint peterpy

test:
	poetry run pytest
