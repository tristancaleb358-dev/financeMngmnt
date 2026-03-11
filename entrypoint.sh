#!/bin/bash
set -e

echo "⏳ Attente DB..."
# Attendre la DB (host.docker.internal pour standalone)
sleep 2

echo "🚀 Make migrations..."
python manage.py makemigrations --noinput

echo "🚀 Migrations..."
python manage.py migrate --noinput

echo "✅ Serveur..."
exec python manage.py runserver 0.0.0.0:8000
