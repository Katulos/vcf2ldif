.DEFAULT_GOAL := help
.PHONY: coverage deps help lint push test

coverage:  ## Run tests with coverage
	python -m coverage erase
	pytest

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage coverage.xml
	rm -fr htmlcov/
	rm -fr .pytest_cache


deps:  ## Install dependencies
	python -m pip install setuptools tox twine wheel
	python -m pip install -r requirements-test.txt

lint:  ## Lint and static-check
	black src
	flake8 src
	pylint src

publish:  ## Publish to PyPi
	cp .pypirc ~/
	python -m build
	python -m twine upload dist/*

publish-test:  ## Publish to Test PyPi
	cp .pypirc ~/
	python -m build
	python -m twine upload --repository testpypi dist/*

push:  ## Push code with tags
	git push && git push --tags

test:  ## Run tests
	pytest

tox:   ## Run tox
	python -m tox
