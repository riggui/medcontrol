    #!/bin/sh
    set -e
    echo "Applying migrations..."
    python manage.py makemigrations --noinput || true
    python manage.py migrate --noinput
    if [ -n "${DJANGO_SUPERUSER_USERNAME}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD}" ] && [ -n "${DJANGO_SUPERUSER_EMAIL}" ]; then
      python manage.py createsuperuser --noinput --username "${DJANGO_SUPERUSER_USERNAME}" --email "${DJANGO_SUPERUSER_EMAIL}" || true
      python - <<PY
from django.contrib.auth import get_user_model
User = get_user_model()
try:
    u = User.objects.get(username='${DJANGO_SUPERUSER_USERNAME}')
    u.set_password('${DJANGO_SUPERUSER_PASSWORD}')
    u.save()
    print('Superuser ensured.')
except Exception as e:
    print('Could not ensure superuser:', e)
PY
    fi
    exec "$@"
