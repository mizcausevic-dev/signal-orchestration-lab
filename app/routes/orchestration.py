from fastapi import APIRouter, HTTPException

from app.models import DashboardSummary, GraphResponse, OrchestrationInput, OrchestrationResponse
from app.sample_data import SAMPLE_ORCHESTRATIONS
from app.services.orchestrator import build_dashboard_summary, build_graph, build_orchestration

router = APIRouter(prefix="/api", tags=["orchestration"])


@router.get("/orchestrations")
def list_orchestrations() -> list[dict]:
    return [
        {
            "orchestration_id": item.orchestration_id,
            "scenario_name": item.scenario_name,
            "environment": item.environment,
            "node_count": len(item.nodes),
        }
        for item in SAMPLE_ORCHESTRATIONS
    ]


@router.get("/orchestrations/{orchestration_id}", response_model=OrchestrationInput)
def get_orchestration(orchestration_id: str) -> OrchestrationInput:
    for item in SAMPLE_ORCHESTRATIONS:
        if item.orchestration_id == orchestration_id:
            return item
    raise HTTPException(status_code=404, detail="Orchestration not found")


@router.get("/dashboard/summary", response_model=DashboardSummary)
def dashboard_summary() -> DashboardSummary:
    return build_dashboard_summary(SAMPLE_ORCHESTRATIONS)


@router.post("/analyze/orchestration", response_model=OrchestrationResponse)
def analyze_orchestration(payload: OrchestrationInput) -> OrchestrationResponse:
    return build_orchestration(payload)


@router.post("/analyze/graph", response_model=GraphResponse)
def analyze_graph(payload: OrchestrationInput) -> GraphResponse:
    return build_graph(payload)


@router.post("/analyze/escalation", response_model=OrchestrationResponse)
def analyze_escalation(payload: OrchestrationInput) -> OrchestrationResponse:
    return build_orchestration(payload)

