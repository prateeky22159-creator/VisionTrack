from fastapi import FastAPI, Header, HTTPException, Depends
from config import settings
from database import Base, engine
from routers import projects, tasks, costs, scope, reports
import pandas as pd
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

def verify_api_key(x_api_key: str | None = Header(default=None)):
    if settings.api_key and x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

@app.get("/")
def root():
    return {"message": "Welcome to VisionTrack API. Visit /docs for usage."}

@app.get("/health")
def health():
    return {"status": "ok", "env": settings.env}

# 🔹 Public endpoint for costs (no API key required)
@app.get("/public/costs")
def public_costs():
    try:
        df = pd.read_csv("CostTimeDataset.csv")
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}

# 🔹 Public endpoint for timeschedule (no API key required)
@app.get("/public/timeschedule")
def public_timeschedule():
    try:
        file_path = os.path.join(os.path.dirname(__file__), "TimescheduleDataset.csv")
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}

        try:
            df = pd.read_csv(file_path, encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding="ISO-8859-1")
        
        # Fill NaN values to prevent JSON serialization errors
        df = df.fillna('')
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": f"Failed to load timeschedule: {str(e)}"}


# Routers with API key protection
app.include_router(projects.router, dependencies=[Depends(verify_api_key)])
app.include_router(tasks.router, dependencies=[Depends(verify_api_key)])
app.include_router(costs.router, dependencies=[Depends(verify_api_key)])
app.include_router(scope.router, dependencies=[Depends(verify_api_key)])
app.include_router(reports.router, dependencies=[Depends(verify_api_key)])