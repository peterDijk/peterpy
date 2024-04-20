# .PHONY: test
# if a file test exists in the same directory as the Makefile, the make command will not work
# by adding .PHONY: test, we are telling make that test is not a file, but a command
format:
	poetry run isort .
	poetry run black . --diff --color
	poetry run black .

lint:
	poetry run isort --check .
	poetry run black --check .
	poetry run bandit -r peterpy
	poetry run mypy --no-strict-optional --ignore-missing-imports peterpy
	poetry run pylint peterpy
