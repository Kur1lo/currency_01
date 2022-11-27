SHELL := /bin/bash

manage_py := docker exec -it backend python app/manage.py

manage:
	$(manage_py) $(COMMAND)

run:
	$(manage_py) runserver 0:8000

show_urls:
	$(manage_py) show_urls

migrate:
	$(manage_py) migrate

makemigrations:
	$(manage_py) makemigrations

shell:
	$(manage_py) shell_plus --print-sql

celery:
	cd app && celery -A settings worker --loglevel=INFO

celerybeat:
	cd app && celery -A settings beat --loglevel=INFO

build_and_run: makemigrations \
	migrate \
	run

pytest:
	pytest app/tests/

coverage:
	pytest --cov=app app/tests/ --cov-report html && coverage report --fail-under=70.0000

show-coverage:  ## open coverage HTML report in default browser
	python3 -c "import webbrowser; webbrowser.open('.pytest_cache/coverage/index.html')"

parse_privatbank_archive:
	$(manage_py) parse_privatbank_archive

gunicorn1:
	cd app && gunicorn settings.wsgi:application --bind 0.0.0.0:8001 --workers 10 --threads 2 --log-level info --max-requests 1000 --timeout 10

gunicorn2:
	cd app && gunicorn settings.wsgi:application --bind 0.0.0.0:8002 --workers 10 --threads 2 --log-level info --max-requests 1000 --timeout 10

uwsgi_01:
	cd app && uwsgi --ini uwsgi_conf_01.ini

uwsgi_02:
	cd app && uwsgi --ini uwsgi_conf_02.ini