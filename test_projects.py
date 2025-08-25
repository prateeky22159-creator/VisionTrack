from fastapi.testclient import TestClient
from visiontrack.main import app
from visiontrack.config import settings

client = TestClient(app)
headers = {"X-API-Key": settings.api_key}

def test_create_and_get_project():
    payload = {
        "name": "Demo Project",
        "owner": "Jyoti",
        "start_date": "2025-01-01",
        "end_date": "2025-12-31",
        "budget": 100000,
        "description": "Demo"
    }
    r = client.post("/projects", json=payload, headers=headers)
    assert r.status_code == 200, r.text
    proj = r.json()
    r2 = client.get(f"/projects/{proj['id']}", headers=headers)
    assert r2.status_code == 200
    assert r2.json()["name"] == "Demo Project"
