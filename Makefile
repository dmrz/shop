.PHONY: requirements frontend

# Set the following variable to you project name
PROJECT_NAME = shop
DEFAULT_VIRTUALENV = .env
# Possible virtualenv if virtualenvwrapper is used
POSSIBLE_VIRTUALENV = $(VIRTUAL_ENV)
# Use possible virtualenv if it exists and virtualenvwrapper is used, otherwise use default one
VIRTUALENV = $(if $(wildcard $(POSSIBLE_VIRTUALENV)),$(POSSIBLE_VIRTUALENV),$(DEFAULT_VIRTUALENV))

PYVERSION=3.6
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

default: env requirements frontend migrate loaddata

env:
	@echo "$(PREFIX) Creating virtual environment within \"$(YELLOW)$(BS)$(VIRTUALENV)$(BE)$(WHITE)\" directory"
	@python$(PYVERSION) -m venv $(VIRTUALENV) || rm -rf $(VIRTUALENV) && virtualenv -p `which python$(PYVERSION)` $(VIRTUALENV)

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
