.PHONY: all virtualenv install-poetry install-dev clean dist-clean

PYTHON_VERSION=python3.8
VIRTUALENV_DIR=${PWD}/env
PIP=${VIRTUALENV_DIR}/bin/pip
PIP_INSTALL=${VIRTUALENV_DIR}/bin/pip install
POETRY=${VIRTUALENV_DIR}/bin/poetry
SPHINXBUILD=${VIRTUALENV_DIR}/bin/sphinx-build

# the `all` target will install everything necessary
all: install-dev

virtualenv:
	if [ ! -e ${PIP} ]; then ${PYTHON_VERSION} -m venv ${VIRTUALENV_DIR}; fi
	${PIP_INSTALL} --upgrade pip==20.1.1

install-poetry: virtualenv
	${PIP_INSTALL} poetry==1.0.9
	${POETRY} config virtualenvs.create false
	${POETRY} config virtualenvs.in-project true

install-dev: install-poetry
	${POETRY} install -vvv

clean:
	rm -f .DS_Store .coverage
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;
	find . -depth -name '__pycache__' -exec rm -rf {} \;

dist-clean: clean
	rm -rf ${VIRTUALENV_DIR}
	find . -depth -name '*.egg-info' -exec rm -rf {} \;
