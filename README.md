### Vue 3 + Django Monorepo Starter

A full‑stack starter that pairs a Vue 3 (Vite) frontend with a Django REST backend. The goal is to get you up and running quickly with a clean local dev workflow, JWT auth, and a simple blog API as a reference.

Repository layout:
- `frontend/` — Vue 3 app bootstrapped with Vite
- `backend/` — Django project with REST API under `/api/`

What you can do:
- Run the Django API locally with PostgreSQL
- Run the Vue dev server with proxy to the API
- Register/login using email + password (JWT via SimpleJWT)
- Query example endpoints (`/api/hello/`, blog list/detail, your blog posts)

---

### Quick Start

You can run this project in two ways: manually with local Node.js and Python environments, or with Docker.

#### Running with Docker (Recommended)

This is the easiest way to get started.

- Requirements
  - Docker
  - Docker Compose

- Steps
  1.  **Start the backend and database:**
      Navigate to the `backend` directory and run:
      ```bash
      cd backend
      docker-compose up --build
      ```
      This will build the Docker image for the backend, start the backend service, and start a PostgreSQL database service. The backend will be available at `http://localhost:9090`.

  2.  **Start the frontend:**
      In a separate terminal, navigate to the `frontend` directory and run:
      ```bash
      cd frontend
      docker-compose up --build
      ```
      This will build the Docker image for the frontend and start the frontend service. The frontend will be available at `http://localhost:5173`.

The two services communicate over a shared Docker network. The backend API will be available at `http://localhost:9090/api/`.

#### Manual Setup

- Requirements
  - Node.js 18+ (20+ recommended)
  - npm (or pnpm/yarn)
  - Python 3.11+ (3.10+ likely fine)
  - PostgreSQL 14+ (local instance)

- One‑time setup
  1) Backend
     - Create venv and install deps
       ```
       cd backend
       python -m venv .venv
       # Windows: .venv\\Scripts\\activate
       # macOS/Linux:
       source .venv/bin/activate
       pip install -r requirements.txt
       ```
     - Configure database (PostgreSQL). See the “Database setup” section for details.
     - Run initial migrations
       ```
       python manage.py migrate
       ```
     - (Optional) Create superuser
       ```
       python manage.py createsuperuser
       ```
  2) Frontend
     ```
     cd frontend
     npm install
     ```

- Start both servers
  - API: `cd backend && source .venv/bin/activate && python manage.py runserver` → http://127.0.0.1:8000
  - Web: `cd frontend && npm run dev` → http://127.0.0.1:5173

The Vite dev server proxies requests that start with `/api` to the Django server, so the frontend can call the backend without CORS issues during development.

---

### Backend (Django REST)

- Main settings: `backend/config/settings.py`
- Apps included:
  - `accounts` — custom user model (`AUTH_USER_MODEL = 'accounts.CustomUser'`)
  - `core` — sample endpoints (hello + blog)
  - `admin_api` — admin‑related API hooks (see code for details)
- Auth: JSON Web Tokens via `rest_framework_simplejwt` (login/refresh endpoints provided)

Run dev server:
```
cd backend
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python manage.py runserver  # http://127.0.0.1:8000
```

Common management commands:
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

### API Overview

Base path: `http://127.0.0.1:8000/api/`

- Health/hello
  - GET `/hello/`
    - Response example:
      ```json
      { "message": "Hello from Django!", "framework": "Django", "version": 5 }
      ```

- Auth (JWT)
  - POST `/auth/register/`
    - Body (example):
      ```json
      { "email": "user@example.com", "password": "StrongPass123", "first_name": "Ada", "last_name": "Lovelace" }
      ```
    - Returns the created user object.
  - POST `/auth/login/`
    - Body:
      ```json
      { "email": "user@example.com", "password": "StrongPass123" }
      ```
    - Returns JWT `access` and `refresh`.
  - POST `/auth/refresh/`
    - Body:
      ```json
      { "refresh": "<refresh_token>" }
      ```
    - Returns new `access`.
  - GET `/auth/user/` (requires Authorization: Bearer <access>)
    - Returns the current authenticated user.

- Blog
  - GET `/blog/` — list approved posts (public)
  - POST `/blog/` — create a post (authenticated; uses current user as author)
  - GET `/blog/my/` — list only your posts (authenticated)
  - GET `/blog/<id>/` — retrieve post
  - PUT/PATCH `/blog/<id>/` — update post (author or staff)

Note: The serializers and permissions ensure only approved posts are public and only authors/staff can edit or view unapproved posts.

---

### Database Setup (PostgreSQL)

This project is configured to use PostgreSQL. By default, `backend/config/settings.py` contains a hard‑coded connection for local development:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':  'coredb',
        'USER': 'cadmin',
        'PASSWORD': 'supersecretcode2',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

You have two options:

1) Create the exact local DB and role to match the defaults above (fastest):
   - In `psql` as a superuser, run:
     ```sql
     CREATE ROLE cadmin WITH LOGIN PASSWORD 'supersecretcode2';
     CREATE DATABASE coredb OWNER cadmin;
     GRANT ALL PRIVILEGES ON DATABASE coredb TO cadmin;
     ```
   - Ensure PostgreSQL is running, then run migrations.

2) Customize your DB settings (recommended for teams):
   - Edit `backend/config/settings.py` `DATABASES['default']` to your local values; or
   - Replace the section with an environment‑variable driven config, e.g.:
     ```python
     import os
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': os.environ.get('DB_NAME', 'myproject'),
             'USER': os.environ.get('DB_USER', 'myproject'),
             'PASSWORD': os.environ.get('DB_PASSWORD', ''),
             'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
             'PORT': os.environ.get('DB_PORT', '5432'),
         }
     }
     ```
   - Then set env vars before running the server:
     - macOS/Linux (bash/zsh):
       ```
       export DB_NAME=myproject
       export DB_USER=myproject
       export DB_PASSWORD=strongpassword
       export DB_HOST=127.0.0.1
       export DB_PORT=5432
       ```
     - Windows (PowerShell):
       ```powershell
       $env:DB_NAME = "myproject"
       $env:DB_USER = "myproject"
       $env:DB_PASSWORD = "strongpassword"
       $env:DB_HOST = "127.0.0.1"
       $env:DB_PORT = "5432"
       ```

To create a role and database from scratch (generic):
```
# Linux (Debian/Ubuntu)
sudo -u postgres psql
# macOS (Homebrew)
brew services start postgresql
psql postgres
# Windows
psql -U postgres -h 127.0.0.1 -d postgres
```
Then in psql:
```sql
CREATE ROLE myproject WITH LOGIN PASSWORD 'strongpassword';
CREATE DATABASE myproject OWNER myproject;
GRANT ALL PRIVILEGES ON DATABASE myproject TO myproject;
-- Optional hardening
ALTER ROLE myproject NOCREATEDB NOCREATEROLE NOINHERIT;
```

Apply migrations:
```
cd backend
source .venv/bin/activate
python manage.py migrate
```

---

### Frontend (Vue 3 + Vite)

Install and run:
```
cd frontend
npm install
npm run dev  # http://127.0.0.1:5173
```

Dev proxy: `frontend/vite.config.js` proxies `/api` → `http://127.0.0.1:8000` so API calls like `fetch('/api/hello/')` work without extra CORS setup.

Build commands:
```
npm run build
npm run preview
```

Entry component: `frontend/src/App.vue`. Add pages under `frontend/src/views/` and routes under `frontend/src/router/`.

---

### Environment & Configuration

- Django
  - `DEBUG` is enabled by default in local settings; don’t use in production.
  - `SECRET_KEY` is currently hard‑coded for local dev. Replace and load via env var for production.
  - Static files are collected into `staticfiles/` when running `collectstatic`.
- Frontend
  - Use Vite env files (`.env`, `.env.local`) if you need custom variables; prefix with `VITE_` to expose to the client.

---

### Security Notes

- Do not commit real secrets or production database credentials.
- For production, always provide `SECRET_KEY` via env var, disable `DEBUG`, and restrict `ALLOWED_HOSTS`.
- Use a managed PostgreSQL service or a secured instance; configure SSL as appropriate.

---

### Troubleshooting

- “Connection refused” to Postgres: verify service is running and port 5432 is open; check `HOST`=`127.0.0.1` vs `localhost` on your OS.
- Migration errors after changing models: try `python manage.py makemigrations` then `migrate`.
- CORS issues in dev: ensure you are calling the API via `/api/...` so the Vite proxy applies; confirm both servers are running.
- JWT `401 Unauthorized`: ensure you include `Authorization: Bearer <access_token>` header and your token hasn’t expired. Use `/auth/refresh/` to refresh.

---

### Where to Extend

- Backend
  - Add endpoints in `backend/core/views.py` and wire them in `backend/core/urls.py` (included under `/api/`).
  - Add apps under `backend/` and register them in `INSTALLED_APPS` in `backend/config/settings.py`.
- Frontend
  - Add new views/components under `frontend/src/` and register routes.
  - Use a state manager like Pinia (already included via dependencies) if needed.

---

### License

This starter is provided as‑is. Use freely for learning or as a base for your project.
