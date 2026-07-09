#!/usr/bin/env bash
# Script de build pour Render
set -o errexit

pip install -r requirements-prod.txt

python manage.py collectstatic --no-input
python manage.py migrate
