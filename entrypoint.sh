#!/bin/sh
set -e

#wait for Postgres to be ready
if [ -n "$POSTGRES_HOST" ]; then
    echo "Waiting for Postgres at $POSTGRES_HOST:$POSTGRES_PORT..."
    until nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
        >&2 echo "Postgres is unavailable - sleeping"
        sleep 1
    done
    >&2 echo "Postgres is up - continuing"
fi

# Apply migrations and collect static
python manage.py migrate --noinput
python manage.py collectstatic --noinput --clear

echo "=================================================="
echo " 🚀 TastyRoad API is starting!"
if [ "$DJANGO_DEBUG" = "1" ]; then
    echo " 🛠 Mode       : DEVELOPMENT (Localhost)"
    echo " 🌐 Nginx      : http://localhost"
    echo " ⚙️ API        : http://localhost:${APP_PORT:-8000}"
    echo " 🐘 PostGIS DB    : localhost:${POSTGRES_PORT:-5432} (DB: $POSTGRES_DB, User: $POSTGRES_USER)"
else
    echo " 🌍 Mode       : PRODUCTION (Render)"
    echo " ⚙️ API Port   : ${PORT:-8000}"
    echo " 🐘 PostGIS DB    : Connected via DATABASE_URL"
fi
echo "=================================================="

# Run default command (gunicorn)
exec "$@"
