# Start Server locally

## First time

- pip install virtualenv
- pip install virtualenvwrapper-win
- mkvirtualenv qrgen
- pip install -r requirements.txt
- python manage.py runserver

## Every time

- workon qrgen
- python manage.py runserver

## Procfile Honcho for celery

web: gunicorn qrgen.wsgi --log-file
worker1: celery -A qrgen beat -l info
worker2: celery -A qrgen worker -l info
