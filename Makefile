SHELL=/bin/bash
PYTHON=python3.11
PYTHON_ENV=env

.PHONY: clean dist _release


# python env ##################################################################
clean:
	rm -rf $(PYTHON_ENV)

$(PYTHON_ENV): pyproject.toml
	rm -rf $(PYTHON_ENV) && \
	$(PYTHON) -m venv $(PYTHON_ENV) && \
	. $(PYTHON_ENV)/bin/activate && \
	pip install pip --upgrade && \
	pip install -e .[dev]

# packaging ###################################################################
dist: | $(PYTHON_ENV)
	. $(PYTHON_ENV)/bin/activate && \
	rm -rf dist *.egg-info && \
	$(PYTHON) -m build

_release: dist
	. $(PYTHON_ENV)/bin/activate && \
	twine upload --config-file ~/.pypirc dist/*
