from fastapi import FastAPI, Header, HTTPException
from .config import settings
from .database import Base, engine
from .routers import projects, tasks, costs, scope, reports

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

def verify_api_key(x_api_key: str | None = Header(default=None)):
    if settings.api_key and x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

@app.get("/health")
def health():
    return {"status": "ok", "env": settings.env}

app.include_router(projects.router, dependencies=[verify_api_key])
app.include_router(tasks.router, dependencies=[verify_api_key])
app.include_router(costs.router, dependencies=[verify_api_key])
app.include_router(scope.router, dependencies=[verify_api_key])
app.include_router(reports.router, dependencies=[verify_api_key])
