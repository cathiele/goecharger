#!/usr/bin/env bash

rm -rf build && rm -rf dist
python3 setup.py sdist bdist_wheel --universal
python3 -m twine upload dist/*
