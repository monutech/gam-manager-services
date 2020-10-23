worker: celery -A gam_services worker --concurrency=2
web: waitress-serve --port=${PORT:-8000} gam_services.wsgi:application