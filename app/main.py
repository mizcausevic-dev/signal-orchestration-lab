from fastapi import FastAPI

from app.config import settings
from app.routes import health, orchestration

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description=(
        "Python orchestration backend for signal routing, dependency mapping, "
        "escalation planning, and action sequencing."
    ),
)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": settings.app_name,
        "status": "ok",
        "docs": "/docs",
    }


app.include_router(health.router)
app.include_router(orchestration.router)
