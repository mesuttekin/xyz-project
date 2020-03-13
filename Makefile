.PHONY: clean system-packages python-packages install tests run all

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

venv:
	python3 -m venv env

source-activate:
	source env/bin/activate

python-packages:
	pip install -r requirements.txt

install: venv source-activate python-packages

tests:
	python manage.py test

run:
	python manage.py run

all: clean install tests run