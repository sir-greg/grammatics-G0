#! /usr/bin/bash

cd ./src

autopep8 -i *.py
autopep8 -i gui/*.py
black *.py
black gui/*.py
yapf -i *.py
yapf -i gui/*.py
