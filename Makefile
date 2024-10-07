PORT ?= 1624
FILES := main

install:
	poetry install

build:
	poetry build

lint:
	poetry run flake8 $(FILES)

test:
	poetry run pytest

test-vv:
	poetry run pytest -vv tests

check: test lint

run:
	poetry run flask --app main run --port $(PORT)

run-dev:
	poetry run flask --app main run --port $(PORT) --debug