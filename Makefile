NAME := bare-necessities
VENV := $(shell echo $${VIRTUAL_ENV-.venv})
VERSION_FILE := $(shell echo $${VERSION_FILE-src/version.json})
SOURCE := $(shell git config remote.origin.url | sed -e 's|git@|https://|g' | sed -e 's|github.com:|github.com/|g')
VERSION := $(shell git describe --always --tag)
COMMIT := $(shell git log --pretty=format:'%H' -n 1)
PYTHON := $(VENV)/bin/python3
VIRTUALENV := virtualenv --python=python3.8
PIP_INSTALL := $(VENV)/bin/pip install --progress-bar=off
INSTALL_STAMP := $(VENV)/.install.stamp

all: check-types check-format test

$(PYTHON):	
	$(VIRTUALENV) $(VENV)

$(VERSION_FILE):
	echo '{"name":"$(NAME)","version":"$(VERSION)","source":"$(SOURCE)","commit":"$(COMMIT)"}' > $(VERSION_FILE)

install: $(INSTALL_STAMP) $(COMMIT_HOOK)
$(INSTALL_STAMP): $(PYTHON) requirements/dev.txt requirements/defaults.txt
	$(PIP_INSTALL) -U -r requirements/defaults.txt -r requirements/dev.txt
	touch $(INSTALL_STAMP)

test: $(INSTALL_STAMP) $(VERSION_FILE)
	SQLALCHEMY_DATABASE_URI=sqlite:///:memory: PYTHONPATH=. $(VENV)/bin/pytest

check-types: $(INSTALL_STAMP)
	$(VENV)/bin/mypy --config setup.cfg

check-format: $(INSTALL_STAMP)
	$(VENV)/bin/black --config pyproject.toml --diff --check .

clean:
	find . -type d -name "__pycache__" | xargs rm -rf {};
	rm -rf $(VENV)

.PHONY: clean test check-types src/version.json