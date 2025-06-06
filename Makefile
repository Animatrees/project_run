run:
	python manage.py runserver --settings=project_run.settings.local

migrate:
	python manage.py migrate --settings=project_run.settings.local

migrations:
	python manage.py makemigrations --settings=project_run.settings.local

.PHONY: run migrate migrations
