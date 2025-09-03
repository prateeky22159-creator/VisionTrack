from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix="/powerbi", tags=["powerbi"])

@router.get("/kpis")
def get_project_kpis(db: Session = Depends(get_db)):
    result = db.execute("""
        SELECT
            p.id AS project_id,
            p.name AS project_name,
            COALESCE(SUM(c.cost), 0) AS total_cost
        FROM projects p
        LEFT JOIN costs c ON c.project_id = p.id
        GROUP BY p.id, p.name
    """)
    return [dict(row) for row in result]
