from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    app_name: str = Field(default="VisionTrack API", alias="APP_NAME")
    api_key: str = Field(default="dev-secret-key", alias="API_KEY")
    database_url: str = Field(default="sqlite:///./visiontrack.db", alias="DATABASE_URL")
    env: str = Field(default="dev", alias="ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    jira_url: str = " https://prateeky22159.atlassian.net/"
    jira_user: str = " prateeky22159@gmail.com"
    jira_token: str = "ATATT3xFfGF0EIJRyfA-L-etmLoBvkRj5Oo-BZ0M3ns5-oAgXD--z2dsdhdpbdy9wNkC3RupUobxpZKDK7v8DdiRUrghhjXHAne6YfSRaKj9ZtMVAl6ZcpMbV1f8BX9voofGoKIoWitUdPpGWwu74YdRiKzoWHlN1Z_HcOzmkeaZp5TFrLYmyQ8=0231BE55"
    model_config = {
        "env_file": ".env",
        "case_sensitive": False
    }

settings = Settings()
