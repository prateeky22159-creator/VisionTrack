import os
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    app_name: str = Field(default="VisionTrack API", alias="APP_NAME")
    api_key: str = Field(default="dev-secret-key", alias="API_KEY")
    database_url: str = Field(default="sqlite:///./visiontrack.db", alias="DATABASE_URL")
    env: str = Field(default="dev", alias="ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    jira_url: str = os.getenv("JIRA_URL", "")
    jira_user: str = os.getenv("JIRA_USER", "")
    jira_api_token: str = os.getenv("JIRA_API_TOKEN", "")
    model_config = {
        "env_file": ".env",
        "case_sensitive": False
    }

settings = Settings()
