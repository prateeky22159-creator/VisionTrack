import pandas as pd
from sqlalchemy.orm import Session
from database import SessionLocal
import models

def import_tasks_from_csv(csv_path: str = "TimescheduleDataset.csv"):
    df = pd.read_csv(csv_path)
    session: Session = SessionLocal()
    for _, row in df.iterrows():
        # You may need to adjust the mapping based on your actual model fields
        task = models.Task(
            project_id=1,  # Set a valid project_id or map from CSV if available
            name=row.get("Task", "Unnamed Task"),
            assignee=row.get("AssignedTeam", None),
            planned_hours=float(row.get("PlannedDurationDays", 0)),
            actual_hours=float(row.get("ActualDurationDays", 0)),
            status=row.get("Status", "planned"),
            due_date=pd.to_datetime(row.get("PlannedEnd")).date() if pd.notnull(row.get("PlannedEnd")) else None
        )
        session.add(task)
    session.commit()
    session.close()
    print(f"Imported {len(df)} task records.")

if __name__ == "__main__":
    import_tasks_from_csv()
