import pandas as pd
from sqlalchemy.orm import Session
from database import SessionLocal
import models

def import_costs_from_csv(csv_path: str = "CostTimeDataset.csv"):
    df = pd.read_csv(csv_path)
    session: Session = SessionLocal()
    for _, row in df.iterrows():
        # You may need to adjust the mapping based on your actual model fields
        cost = models.Cost(
            project_id=1,  # Set a valid project_id or map from CSV if available
            category=row.get("Category", "Unknown"),
            amount=float(row.get("ActualCost", 0)),
            incurred_on=pd.to_datetime(row.get("Date")).date()
        )
        session.add(cost)
    session.commit()
    session.close()
    print(f"Imported {len(df)} cost records.")

if __name__ == "__main__":
    import_costs_from_csv()
