from fastapi import FastAPI, Header, HTTPException, Depends
from .config import settings
from .database import Base, engine
from .routers import projects, tasks, costs, scope, reports

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

def verify_api_key(x_api_key: str | None = Header(default=None)):
    # Very basic API-key check; replace with JWT/OAuth for production
    if settings.api_key and x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
@app.get("/")
def root():
    return {"message": "Welcome to VisionTrack API. Visit /docs for usage."}
    
@app.get("/health")
def health():
    return {"status": "ok", "env": settings.env}

# ✅ Wrap all dependencies with Depends()
app.include_router(projects.router, dependencies=[Depends(verify_api_key)])
app.include_router(tasks.router, dependencies=[Depends(verify_api_key)])
app.include_router(costs.router, dependencies=[Depends(verify_api_key)])
app.include_router(scope.router, dependencies=[Depends(verify_api_key)])
app.include_router(reports.router, dependencies=[Depends(verify_api_key)])
