# FastAPI Student Management Starter

Teachable API featuring:
- Sign up (`POST /auth/signup`)
- Login with JWT (`POST /auth/login`)
- Protected Student CRUD (`/students/*`)
- **Auto-seeding on startup** (idempotent; runs only if DB is empty)
- SQLite by default, easy switch to **PostgreSQL**

## Run

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
# optional
copy .env.example .env    # Windows
# cp .env.example .env    # macOS/Linux

uvicorn app.main:app --reload
```

Docs: http://127.0.0.1:8000/docs

## PostgreSQL (Render)

1) Set `DATABASE_URL` like:
```
postgresql+psycopg2://USER:PASSWORD@HOST:5432/DBNAME
```
2) Add environment variables in Render Dashboard.
3) Start command:
```
uvicorn app.main:app --host=0.0.0.0 --port=10000
```
(Or use gunicorn+uvicorn worker if desired.)

Seeding is **idempotent** and will run on startup only when the DB is empty (no users).
