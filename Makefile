.PHONY: develop deps bump push clean

VIRTUAL_ENV ?= $(PWD)/env

PY = $(VIRTUAL_ENV)/bin/python
PIP = $(VIRTUAL_ENV)/bin/pip

current_version = $(shell $(PY) setup.py --version)
package_name = $(shell $(PY) setup.py --name)
init_py_file = $(package_name)/__init__.py


$(PY):
	virtualenv env
	$(eval VIRTUAL_ENV = $(PWD)/env)


# Prepare the environment for development
develop: $(PY) deps
	$(PY) setup.py develop


# install development dependencies
deps: $(PY)
	if [ -f requirements.txt ]; then $(PIP) install -r requirements.txt; fi


# bump the version number
bump: $(PY)
	@test ! -z "$(version)" || ( echo "specify a version number: make bump version=$(current_version)" && exit 1 )
	@! git status --porcelain 2> /dev/null | grep -v "^??" || ( echo 'uncommited changes. commit them first' && exit 1 )
	@echo "Bumping current version $(current_version) to $(version)"
	sed -i '.bak' -e "/^__version__ = .*$$/s/'[^']*'/'$(version)'/" $(init_py_file)
	rm -f $(init_py_file).bak
	git add $(init_py_file)
	git commit -m 'Bumped version number to $(version)'
	git tag -m 'Mark stable release version $(version)' -a $(version)
	@echo "Version $(version) commited and tagged. You can 'make push' now :)"


# Push to github but run tests first
push: test
	git push origin HEAD
	git push origin --tags


# Clean all build artifacts
clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '._*' -exec rm -f {} +
	find . -name '.coverage*' -exec rm -f {} +
	rm -rf build/ dist/ MANIFEST docs/_build/* 2>/dev/null || true
