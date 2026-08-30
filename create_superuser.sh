#!/usr/bin/env bash
set -o errexit

USERNAME="${DJANGO_SUPERUSER_USERNAME:-admin}"
EMAIL="${DJANGO_SUPERUSER_EMAIL:-admin@example.com}"
PASSWORD="${DJANGO_SUPERUSER_PASSWORD:-}"

if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
else
    PYTHON=python
fi

"$PYTHON" - "$USERNAME" "$EMAIL" "$PASSWORD" <<'PY'
import os
import sys

import django

username, email, password = sys.argv[1], sys.argv[2], sys.argv[3]

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ims.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

user = User.objects.filter(username=username).first()
if user is None:
    if not password:
        raise SystemExit("DJANGO_SUPERUSER_PASSWORD is required to create a superuser.")
    user = User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Created superuser '{username}'.")
else:
    updated = []
    if password:
        user.set_password(password)
        updated.append("password")
    if email and user.email != email:
        user.email = email
        updated.append("email")
    user.is_superuser = True
    user.is_staff = True
    if updated:
        user.save()
        print(f"Updated superuser '{username}': {', '.join(updated)}.")
    else:
        print(f"Superuser '{username}' already exists and is up to date.")
PY
