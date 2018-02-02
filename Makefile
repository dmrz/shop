.PHONY: requirements frontend

PROJECT_NAME = shop
VIRTUALENV = .env

PIP = $(VIRTUALENV)/bin/pip
PYTHON = $(VIRTUALENV)/bin/python
PYTEST = $(VIRTUALENV)/bin/pytest

BS=\033[1m
BE=\033[0m
BSU=\033[1;4m
BLUE=\033[34m
CYAN=\033[36m
GREEN=\033[32m
MAGENTA=\033[35m
RED=\033[31m
WHITE=\033[37m
YELLOW=\033[33m
PREFIX=$(GREEN)$(BS)=>$(BE)$(WHITE)

default: requirements frontend migrate loaddata

requirements:
	@echo "$(PREFIX) Installing local $(PROJECT_NAME) requirements"
	@$(PIP) install -qr requirements/local.txt

requirements-frontend:
	@echo "$(PREFIX) Installing frontend requirements"
	@cd frontend ; yarn -s --no-progress --emoji false

frontend: requirements-frontend
	@echo "$(PREFIX) Building frontend"
	@cd frontend ; yarn -s build

migrate:
	@echo "$(PREFIX) Applying migrations"
	@$(PYTHON) $(PROJECT_NAME)/manage.py migrate -v 0 --noinput $(app)

loaddata:
	@echo "$(PREFIX) Loading initial data fixtures"
	@$(PYTHON) $(PROJECT_NAME)/manage.py loaddata -v0 fixtures/initial_users.json
	@$(PYTHON) $(PROJECT_NAME)/manage.py loaddata -v0 fixtures/initial_products.json

run:
	@$(PYTHON) $(PROJECT_NAME)/manage.py runserver

test:
	@$(PYTEST) -s $(PROJECT_NAME) || true
