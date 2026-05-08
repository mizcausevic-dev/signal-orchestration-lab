from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Signal Orchestration Lab"
    app_env: str = "development"
    app_port: int = 8000


settings = Settings()

