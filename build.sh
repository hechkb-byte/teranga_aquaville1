#!/usr/bin/env bash
# Script de build pour Render
set -o errexit

pip install -r requirements-prod.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Peuple la base avec les données du site (sans doublons si déjà présentes)
python manage.py loaddata services/fixtures/services.json
python manage.py seed_villas