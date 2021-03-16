#!/usr/bin/env make


all:

help:
	@printf "all commands available for make are:.\n"
	@printf "venv - creates a virtual enviroment.\n"
	@printf "install - installs all the needed packages.\n"
	@printf "clean - cleans all the generated documents.\n"
	@printf "unittest - runs the unit tests.\n"
	@printf "coverage - run and creates a coverage report.\n"
	@printf "pylint - runs pylint.\n"
	@printf "flake8 - runs flake8.\n"
	@printf "doc - creates documentation of the application.\n"

venv:
	[ -d .venv ] || $ python -m venv .venv
	@printf "To activate the virtual enviroment do:\n"
	@printf ". .venv/Scripts/activate\n"
	@printf "Type 'deactivate' to deactivate.\n"

install:
	$ python -m pip install -r requirements.txt

clean:
	rm -f .coverage *.pyc
	rm -rf __pycache__
	rm -rf htmlcov
	rm -rf doc
	rm -rf .venv

unittest:
	 $ python -m unittest discover . "*_test.py"

coverage:
	coverage run -m unittest discover . "*_test.py"
	coverage html
	coverage report -m

pylint:
	pylint *.py

flake8:
	flake8

pydoc:
	install -d doc/pydoc
	$ python -m pydoc -w "$(PWD)"
	mv *.html doc/pydoc

pdoc:
	rm -rf doc/pdoc
	pdoc --html -o doc/pdoc .

doc: pdoc pyreverse #pydoc sphinx

pyreverse:
	install -d doc/pyreverse
	pyreverse *.py
	dot -Tpng classes.dot -o doc/pyreverse/classes.png
	dot -Tpng packages.dot -o doc/pyreverse/packages.png
	rm -f classes.dot packages.dot
	ls -l doc/pyreverse

test: flake8 pylint coverage
