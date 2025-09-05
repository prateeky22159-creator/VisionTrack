from fastapi import APIRouter
from config import settings
import requests

router = APIRouter(prefix="/jira", tags=["Jira"])

# Jira API Authentication
JIRA_BASE_URL = settings.jira_url
JIRA_USER = settings.jira_user
JIRA_API_TOKEN = settings.jira_api_token

@router.get("/issues/{project_key}")
def get_jira_issues(project_key: str, max_results: int = 10):
    """
    Fetch issues from a given Jira project (public, no API key required).
    """
    url = f"{JIRA_BASE_URL}/rest/api/3/search"
    auth = (JIRA_USER, JIRA_API_TOKEN)
    params = {
        "jql": f"project={project_key}",
        "maxResults": max_results
    }

    response = requests.get(url, auth=auth, params=params)

    if response.status_code != 200:
        return {"error": response.text}

    return response.json()

@router.get("/projects")
def get_jira_projects():
    """
    List all Jira projects (public, no API key required).
    """
    url = f"{JIRA_BASE_URL}/rest/api/3/project/search"
    auth = (JIRA_USER, JIRA_API_TOKEN)

    response = requests.get(url, auth=auth)

    if response.status_code != 200:
        return {"error": response.text}

    return response.json()
