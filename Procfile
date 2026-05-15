web: python manage.py smart_migrate && python manage.py collectstatic --noinput && gunicorn crisishive.wsgi:application --bind 0.0.0.0:$PORT --log-file -
