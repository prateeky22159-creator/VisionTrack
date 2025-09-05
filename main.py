from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Header, HTTPException, Depends
from config import settings
from database import Base, engine
from routers import projects, tasks, costs, scope, reports, jira
import pandas as pd
import os
from apscheduler.schedulers.background import BackgroundScheduler
from utils.jira_sync import export_cost_time, export_timeschedule
from utils.dummy_projects import generate_dummy_projects

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

# 🔐 API key verification (only for Jira routes)
def verify_api_key(x_api_key: str | None = Header(default=None)):
    if settings.api_key and x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

@app.get("/")
def root():
    return {"message": "Welcome to VisionTrack API. Visit /docs for usage."}

@app.get("/health")
def health():
    return {"status": "ok", "env": settings.env}

# 🔹 Public endpoint for costs
@app.get("/public/costs")
def public_costs():
    try:
        df = pd.read_csv("CostTimeDataset.csv")
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}

# 🔹 Public endpoint for timeschedule
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
        df = df.fillna('')
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": f"Failed to load timeschedule: {str(e)}"}

# 🔹 Public routers (no API key)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(costs.router)
app.include_router(scope.router)
app.include_router(reports.router)

# 🔐 Secure only Jira endpoints
app.include_router(jira.router, dependencies=[Depends(verify_api_key)])

# 🔹 Scheduler to auto-sync Jira data every 24h
@app.on_event("startup")
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(export_cost_time, "interval", args=["PROJ"], hours=24)
    scheduler.add_job(export_timeschedule, "interval", args=["PROJ"], hours=24)
    scheduler.start()
    print("📅 Jira auto-sync started (every 24h)")

# 🔹 Manual sync endpoint
@app.post("/sync/jira/{project_key}")
def manual_jira_sync(project_key: str):
    try:
        export_cost_time(project_key)
        export_timeschedule(project_key)
        return {"message": f"✅ Jira data synced for {project_key}"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/public/jira/dummy")
def get_dummy_jira_projects():
    """
    Return dummy Jira-like projects for testing Power BI dashboards.
    """
    try:
        df = generate_dummy_projects()
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}
