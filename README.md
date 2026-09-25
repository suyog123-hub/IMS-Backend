# IMS — Inventory Management System API

A REST API for managing inventory, built with **Django** + **Django REST Framework**.
It handles **products, categories, units and product variants** out of the box.

> You don't need to know Python to run this. One script does everything.


---
## live at -- https://ims-r9e5.onrender.com/swagger/
## Manual Setup (if you prefer)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # then edit SECRET_KEY
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```



## Quick Start

```bash
git clone https://github.com/suyog123-hub/IMS-Backend.git
cd IMS-Backend
cp .env.example .env          # then edit SECRET_KEY
./build.sh                    # install deps + run migrations + collect static
./create_superuser.sh         # create/update the admin user
./run.sh                      # apply migrations and start the server
```

When it finishes you'll see:

```
API base    : http://127.0.0.1:8000/product/
Admin panel : http://127.0.0.1:8000/admin/
Stop server : press CTRL + C
```

### Windows?

Use [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) (Ubuntu), then run the same commands above.

---

## Running it again later

```bash
./venv/bin/python manage.py runserver
```

---

## What your React app needs to know

| Thing | Value |
|---|---|
| API base URL | `http://127.0.0.1:8000` |
| Products endpoint | `http://127.0.0.1:8000/product/products/` |
| Auth for admin | session-based via `/admin/` |
| CORS | `http://localhost:3000` and `http://localhost:8080` are already allowed |
| Interactive API docs | `http://127.0.0.1:8000/swagger/` |

### Example endpoints

| Method | URL | Action |
|---|---|---|
| GET | `/product/products/` | list products |
| POST | `/product/products/` | create product |
| GET | `/product/products/1/` | product detail (includes variants) |
| PATCH | `/product/products/1/` | partial update |
| DELETE | `/product/products/1/` | delete |

Same pattern works for `/product/categories/`, `/product/units/`, `/product/variants/`.

Search & sort any list endpoint:

```bash
curl "http://127.0.0.1:8000/product/products/?search=sugar&ordering=-quantity"
```

### Example: create a product

```bash
curl -X POST http://127.0.0.1:8000/product/products/ \
  -H "Content-Type: application/json" \
  -d '{"category": 1, "unit": 1, "name": "Sugar", "quantity": 10.5}'
```

---

## Tech Stack

- Python 3 / Django 6
- Django REST Framework
- SQLite (dev database, zero config)
- CKEditor 5 (rich text descriptions)
- drf-yasg (Swagger docs)

## Project Structure

```
ims/
├── apps/
│   ├── product/          # Product domain (API lives here)
│   │   ├── models/       # Category, Unit, Product, ProductVariant
│   │   ├── serializer/
│   │   ├── views/
│   │   └── urls.py
│   └── inventory/        # Reserved for future stock logic
├── ims/                  # Project settings
├── build.sh               # Dependency install, migrations, static files
├── run.sh                 # Starts the development server
├── create_superuser.sh    # Creates/updates the admin user
├── requirements.txt      # Python dependencies
├── .env.example          # Env variable template
└── manage.py             # Django CLI entry point
```



## Environment Variables

Copy `.env.example` to `.env` (build.sh uses it):

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | Django secret key | set it in `.env` |
| `DEBUG` | Enable debug mode | `False` |

---

## Contributors

Thanks to our contributors — this project is built collaboratively:

- [@suyog123-hub](https://github.com/suyog123-hub) — maintainer
- [@rojete](https://github.com/rojete) — co-author & pair-programming partner

> This section was added via a **co-authored commit** to earn the [Pair Extraordinaire](https://docs.github.com/en/account-and-profile/reference/github-achievements#pair-extraordinaire) achievement. See commit trailer: `Co-authored-by: rojete <152104789+rojete@users.noreply.github.com>`.

---

*Last updated: 2026-09-19 — docs: correct clone URL to IMS-Backend*
