setup:
	python3 -m venv ~/.eye-message

env:
	which python3
	python3 --version
	which pip
	which pytest

install:
	pip install -r requirements.txt

test:
	PYTHONPATH=. && pytest -vv --cov=eyemessage tests/*.py

all: install env  test
