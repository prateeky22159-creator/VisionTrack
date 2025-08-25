# VisionTrack – Project Cost, Time & Scope Analysis (Starter)

This is a **production-ready starter** for your Python + SQL project. It includes:
- FastAPI backend (REST)
- SQLAlchemy models & CRUD
- Simple API-key auth hook (easily replace with OAuth/JWT)
- ETL loader scaffold
- Basic analytics (forecast & alerts scaffolds)
- Power BI–friendly SQL views
- Docker & docker-compose for Postgres
- Pytests

## Quickstart (Dev with SQLite)
```bash
python -m venv .venv && source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn visiontrack.main:app --reload
```

Visit: http://127.0.0.1:8000/docs

## Quickstart (Docker + Postgres)
```bash
docker compose up -d --build
# API at http://localhost:8000
```

## Environment
See `.env.example` for variables. By default it uses SQLite for local dev.

## Power BI
Connect Power BI to your database and use the provided `visiontrack/sql/create_views.sql` to create views for dashboards.

## Tests
```bash
pytest -q
```
