#!/bin/bash

docker compose exec web python manage.py init_db
docker compose exec web python manage.py import_books_via_api