# pipenv run gunicorn --config gunicorn_config.py app:app
pipenv run gunicorn --workers 15 --worker-class gthread --timeout 30 --keep-alive 5 app:app --bind 0.0.0.0:8080
