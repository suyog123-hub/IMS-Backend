#!/bin/bash
echo "Applying migration files and starting the server..."
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver