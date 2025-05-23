#! /usr/bin/bash

cd ./src

flake8 *.py
flake8 gui/*.py
pylint *.py
mypy *.py
pyright *.py
isort *.py
pydocstyle *.py
pydocstyle gui/*.py
