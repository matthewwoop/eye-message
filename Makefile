setup:
	python3 -m venv ~/.eye-message

env:
	which python3
	python3 --version
	which pip

install:
	pip install --upgrade pip
	pip install -r requirements.txt

all: install
