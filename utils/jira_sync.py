import requests
import pandas as pd
from config import settings

auth = (settings.jira_user, settings.jira_token)
base_url = settings.jira_url

def fetch_jira_issues(project_key: str, max_results: int = 100):
    url = f"{base_url}/rest/api/3/search"
    params = {"jql": f"project={project_key}", "maxResults": max_results}
    response = requests.get(url, auth=auth, params=params)

    if response.status_code != 200:
        raise Exception(f"Jira fetch failed: {response.text}")

    issues = response.json().get("issues", [])
    data = []
    for issue in issues:
        fields = issue["fields"]

        planned = fields.get("timeoriginalestimate")
        actual = fields.get("timespent")

        data.append({
            "task_id": issue["key"],
            "task_name": fields.get("summary"),
            "status": fields["status"]["name"] if fields.get("status") else None,
            "assigned_to": fields["assignee"]["displayName"] if fields.get("assignee") else None,
            "start_date": fields.get("created"),
            "end_date": fields.get("updated"),
            "planned_time": round(planned / 3600, 2) if planned else 0,   # hrs
            "actual_time": round(actual / 3600, 2) if actual else 0       # hrs
        })

    return pd.DataFrame(data)

def export_cost_time(project_key: str, file_name: str = "CostTimeDataset.csv"):
    df = fetch_jira_issues(project_key)
    df = df[["task_id", "task_name", "assigned_to", "planned_time", "actual_time", "status"]]
    df.to_csv(file_name, index=False)
    print(f"✅ Exported cost/time data to {file_name}")

def export_timeschedule(project_key: str, file_name: str = "TimescheduleDataset.csv"):
    df = fetch_jira_issues(project_key)
    df = df[["task_id", "task_name", "start_date", "end_date", "status"]]
    df.to_csv(file_name, index=False)
    print(f"✅ Exported timeschedule data to {file_name}")
