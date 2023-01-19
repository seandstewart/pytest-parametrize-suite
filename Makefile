SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.ONESHELL:

MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules


# region: environment

bootstrap: install install-precommit
.PHONY: bootstrap

install:
	poetry install
.PHONY: install


install-precommit:
	poetry run pre-commit install && poetry run pre-commit install-hooks
.PHONY: install-precommit


# endregion
# region: dev

format:
	poetry run black $(target) --config=pyproject.toml
	poetry run isort $(target) --profile=black
.PHONY: format

# endregion
# region: ci

lint:
	poetry run black $(target) --check --config=pyproject.toml
	poetry run isort $(target) --check
	poetry run flake8 $(target) --config=.flake8
	poetry run mypy $(target) --config-file=pyproject.toml
.PHONY: lint

test:
	poetry run coverage run $(COV_ARGS) -m pytest $(target) $(TEST_ARGS)
	poetry run coverage report $(COV_ARGS)
	poetry run coverage xml $(COV_ARGS)
.PHONY: test

COV_ARGS ?= --rcfile=.coveragerc
TEST_ARGS ?= --junit-xml=junit.xml

coverage-report:
	poetry run coverage xml --rcfile=.coveragerc
	poetry run coverage html --rcfile=.coveragerc
.PHONY: coverage-report

target ?= .

# endregion
