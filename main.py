from fastapi import FastAPI, Header, HTTPException, Depends
from .config import settings
from .database import Base, engine
from .routers import projects, tasks, costs, scope, reports
from .routers import powerbi

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

@app.get("/")
def root():
    return {"message": "Welcome to VisionTrack API. Visit /docs for usage."}
    
@app.get("/health")
def health():
    return {"status": "ok", "env": settings.env}

# ✅ Wrap all dependencies with Depends()
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(costs.router)
app.include_router(scope.router)
app.include_router(reports.router)
app.include_router(powerbi.router)

# Run FastAPI server on port 8000 and host 0.0.0.0
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
