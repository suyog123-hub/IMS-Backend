#!/usr/bin/env bash
#
# One-shot setup script for this Django REST API.
# Written for developers with NO Python experience (e.g. React devs).
#
# Usage:  ./setup.sh
# It installs Python if missing, creates a virtual environment,
# installs dependencies, creates your .env file, sets up the database
# and starts the local server at http://127.0.0.1:8000
#

set -euo pipefail

# ---------- pretty output ----------
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

step()    { echo -e "\n${BLUE}==> $1${NC}"; }
success() { echo -e "${GREEN}OK: $1${NC}"; }
warn()    { echo -e "${YELLOW}WARNING: $1${NC}"; }
fail()    { echo -e "${RED}ERROR: $1${NC}"; exit 1; }

echo "=============================================="
echo " IMS Inventory API - one-time local setup"
echo "=============================================="

# Run everything from the folder this script lives in
cd "$(dirname "$0")"

# ---------- 1. make sure python3 is available ----------
PYTHON=""
for candidate in python3.14 python3.13 python3.12 python3.11 python3; do
    if command -v "$candidate" >/dev/null 2>&1; then
        PYTHON="$candidate"
        break
    fi
done

if [ -z "$PYTHON" ]; then
    step "Python 3 not found - installing it for you"
    OS="$(uname -s)"
    if [ "$OS" = "Darwin" ]; then
        # macOS
        if command -v brew >/dev/null 2>&1; then
            brew install python
        else
            fail "Homebrew is required to auto-install Python on macOS.
       Install it first:  https://brew.sh   then re-run this script."
        fi
    elif [ "$OS" = "Linux" ]; then
        if command -v apt-get >/dev/null 2>&1; then
            sudo apt-get update && sudo apt-get install -y python3 python3-venv python3-pip
        elif command -v dnf >/dev/null 2>&1; then
            sudo dnf install -y python3 python3-pip
        elif command -v pacman >/dev/null 2>&1; then
            sudo pacman -S --noconfirm python python-pip
        else
            fail "No supported package manager found. Install Python 3 manually: https://www.python.org/downloads/"
        fi
    else
        fail "Unsupported OS ($OS). On Windows use WSL2 or install Python from https://www.python.org/downloads/"
    fi
    command -v python3 >/dev/null 2>&1 || fail "Python installation failed."
    PYTHON="python3"
fi

success "Using $($PYTHON --version) at $(command -v $PYTHON)"

# ---------- 2. virtual environment ----------
VENV_DIR="venv"

if [ ! -d "$VENV_DIR" ]; then
    step "Creating an isolated Python environment (./$VENV_DIR)"
    $PYTHON -m venv "$VENV_DIR" 2>/dev/null || {
        warn "venv module missing - installing python3-venv and retrying"
        if command -v apt-get >/dev/null 2>&1; then
            sudo apt-get install -y python3-venv
            $PYTHON -m venv "$VENV_DIR"
        else
            fail "Could not create a virtual environment. Install the 'venv' package for your Python."
        fi
    }
else
    success "Virtual environment already exists - reusing it"
fi

PIP="$VENV_DIR/bin/pip"
PYBIN="$VENV_DIR/bin/python"
[ -x "$PYBIN" ] || fail "Virtual environment is broken. Delete the '$VENV_DIR' folder and re-run."

# ---------- 3. dependencies ----------
step "Installing project dependencies (this can take a minute)"
"$PIP" install --upgrade pip --quiet
"$PIP" install -r requirements.txt --quiet
success "All packages installed"

# ---------- 4. .env configuration ----------
step "Configuring environment variables (.env)"
if [ ! -f .env ]; then
    SECRET_KEY=$("$PYBIN" -c "import secrets; print(secrets.token_urlsafe(50))")
    printf 'SECRET_KEY=%s\nDEBUG=True\n' "$SECRET_KEY" > .env
    success ".env created with a fresh random SECRET_KEY"
else
    success ".env already exists - keeping your current values"
fi

# ---------- 5. database ----------
step "Creating the database and applying migrations"
"$PYBIN" manage.py migrate --no-input
success "Database ready (db.sqlite3)"

# ---------- 6. sanity check ----------
step "Running Django system checks"
"$PYBIN" manage.py check
success "Everything looks good"

# ---------- done ----------
ADMIN_USER="admin"
if "$PYBIN" -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ims.settings')
django.setup()
from django.contrib.auth import get_user_model
exit(0 if get_user_model().objects.filter(username='$ADMIN_USER').exists() else 1)
" >/dev/null 2>&1; then
    success "Admin user '$ADMIN_USER' already exists"
else
    echo ""
    read -r -p "Create admin login for http://127.0.0.1:8000/admin? [Y/n] " answer
    if [[ ! "$answer" =~ ^[Nn]$ ]]; then
        DJANGO_SUPERUSER_USERNAME="$ADMIN_USER" \
        "$PYBIN" manage.py createsuperuser --no-input ||
        warn "Skipped superuser creation. Create one later with: $VENV_DIR/bin/python manage.py createsuperuser"
    fi
fi

echo ""
echo "=============================================="
success "Setup complete! Starting the server..."
echo "----------------------------------------------"
echo -e " API base      : ${GREEN}http://127.0.0.1:8000/product/${NC}"
echo -e " Admin panel   : ${GREEN}http://127.0.0.1:8000/admin/${NC}"
echo -e " Stop server   : press CTRL + C"
echo -e " Next time     : ${YELLOW}./$VENV_DIR/bin/python manage.py runserver${NC}"
echo "=============================================="
echo ""

exec "$PYBIN" manage.py runserver
